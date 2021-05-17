# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 15:18:43 2020
This script includes all the functions to transform raw log data into formated csv files.

The input filename must organised in the following format: 
    yyyymmdd; eg. 20200312_A, 20200312_1
@author: yan
"""
import os
import re
import csv
import pandas as pd
from datetime import datetime

# change the extension of the file to csv
def extensiontocsv (indir):
    
    os.chdir(indir)
    # change file extension to csv
    for file in os.listdir(indir):
        file_splitext = os.path.splitext(file)
        os.rename(file, file_splitext[0] + '.csv')

# transform data from wide to long, with each row only contains a datapoint for one ID, instead containing data for multiple ID
def stackingcolumns (filename):
    
    with open(filename, 'r') as f:
        # skip first three rows
        for _ in range(3):
            next(f)
        # Store all the tags as delimiters
        delim = next(csv.reader(f))
        if "all" in delim[0]: # check if ID tags are listed
              print("Specific Tag ID Missing")
              exit()
        delim[0] = delim[0][6:] # remove #tags= from the first delim
        delim = "|".join(delim) # transform delim into a string so it can be used in re.split
        # Store each lines in a list
        rows = [l.rstrip('\n') for l in f.readlines()]
        # Split each line with delim and store in a new list
        newrows =[]
        for line in rows:
            newline = re.split(delim,line)
            newrows.append(newline)
        #stack many columns into fewer long ones
        stackList = []
        for row in newrows:
            timestamp = row[0].rstrip(',')
            for i in row[1:]:
                entry = timestamp+i.rstrip(',')
                section = entry.split(",")
                stackList.append(section) 
    #Convert the stacked list into df, drop unnecessary rows
    df = pd.DataFrame(stackList)
    df.drop([2,5,6,7,8,9], axis=1, inplace=True)
    df.columns= ['TIME','ID','X','Y','SPACE']
    return df

def converttime(df):
    #Convert time from unix to datetime format: dd/mm/yy hh:mm:ss.000, and adjust for timezone
    df['TIME'] = pd.to_datetime(df['TIME'],unit='ms', dayfirst=True)
    df['TIME'] = df['TIME'].dt.tz_localize("GMT").dt.tz_convert('Australia/Melbourne').dt.tz_localize(None)
    df[["X","Y"]] = df[["X","Y"]].apply(pd.to_numeric)
    return df

def cleanlabel(df):
    #Clean up teachers' tracker with consistant label
    teacher_dict = {'Teacher_6A':'Teacher_0004', 
                    'Teacher_6B':'Teacher_0001',
                    'Teacher_6C':'Teacher_0005',
                    'Teacher_6D':'Teacher_0002',
                    'Teacher_6E':'Teacher_0006',
                    'Teacher_6F':'Teacher_0003'}
    unassigned_dict = {'Unassigned_0001':'Student_0090',
                       'Unassigned_0002':'Unassigned_0002',
                       'Unassigned_0003':'Unassigned_0003',
                       'Unassigned_0004':'Unassigned_0004',
                       'Unassigned_0005':'Student_0080',
                       'Unassigned_0006':'Unassigned_0006',
                       'Unassigned_0007':'Student_0052',
                       'Unassigned_0008':'Unassigned_0008',
                       'Unassigned_0009':'Unassigned_0009',
                       'Unassigned_0010':'Unassigned_0010',
                       'Unassigned_0011':'Unassigned_0011',}
    df['ID'] = df['ID'].map(lambda x: teacher_dict[x] if 'Teacher_6' in x else x)
    df['ID'] = df['ID'].map(lambda x: unassigned_dict[x] if 'Unassigned' in x else x)
    return df

# remove data outside of school hours
def segmentation(df, start = '09:00:00.000',end = '15:20:00.000'):
    
    df.loc[:,'TIME'] = df['TIME'].astype(str)
    time = df['TIME'].str[11:]
    segdf = df[(time >= start) & (time <= end)]
    
    return segdf

# transform data to one datapoint per second by averaging every 200ms
def normalisation (segdf):
    segdf.loc[:,'TIME'] = segdf.loc[:,'TIME'].str[:19]
    normdf = segdf.groupby(["TIME", "ID",'SPACE'],as_index=False)[["X","Y"]].mean()
    
    return normdf

# insert a day of week column, where 0:Monday 1:Tuesday ... 6:Sunday
def dayofweek(normdf):
    day = pd.to_datetime(normdf.loc[:,'TIME'].str[:10]).dt.dayofweek
    normdf.insert(1, "Day_of_Week", day, True)
    
    return normdf

def formtingtime (df_schedule):
    df_schedule['Start'] = df_schedule['Start'].map(lambda x: datetime.strptime(x, '%H:%M').time())
    df_schedule['Start'] = df_schedule['Start'].map(lambda x: x.strftime("%H:%M:%S"))
    df_schedule['End'] = df_schedule['End'].map(lambda x: datetime.strptime(x, '%H:%M').time())
    df_schedule['End'] = df_schedule['End'].map(lambda x: x.strftime("%H:%M:%S"))
    return df_schedule

def schedule (df, df_schedule, input_subject):
    
    dayofweek_dict = {0:'Monday', 1:'Tuesday', 2:'Wednesday', 3:'Thursday', 4:'Friday'}
    df['Day_of_Week'] = df['Day_of_Week'].map(lambda x: dayofweek_dict[x])
    day = df['Day_of_Week'][0]
    df_subject = df_schedule[(df_schedule['Subject'] == input_subject) & (df_schedule['Day'] == day)]
    
    return df_subject, day

def subjectseg (df_subject, df):
    
    if len(df_subject) != 1 and df_subject['Start'].unique()[-1] != df_subject['End'].unique()[0]:
            
            starttime1 = df_subject['Start'].unique()[0]
            endtime1 = df_subject['End'].unique()[0]
            df1 = segmentation(df,starttime1,endtime1)
            
            starttime2 = df_subject['Start'].unique()[-1]
            endtime2 = df_subject['End'].unique()[-1]
            df2 = segmentation(df,starttime2,endtime2)
            
            df = pd.concat([df1,df2])
            
    else:  
        starttime = df_subject['Start'].unique()[0]
        endtime = df_subject['End'].unique()[-1]
        df = segmentation(df,starttime,endtime)
    
    return df

def subjectlist(df_schedule):
    df_schedule['Room'].fillna('Outside',inplace = True)
    df_schedule = df_schedule[df_schedule['Room'] != 'Outside']
    subject_list = list(df_schedule.Subject.unique())
    return subject_list, df_schedule