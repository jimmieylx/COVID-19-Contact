# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 18:42:00 2020
Run this script and input the path of a file to calculate a proximity matrix for the data
@author: yan
"""
import os
import pandas as pd
import glob
import Transformation as tf
import Enumeration as et
import Distance as dt
import Metrics
import Visualisation as Vs
import networkx as nx
import statistics as st

indir = 'F:\Research Assitant\PROJECT_Position Data\Data_Processing\Data_Files\Clean20190722-0913'
outfile = 'F:\Research Assitant\COVID-19 Positioning\Data Analysis\COVID19_ContactData_{}.csv'
os.chdir(indir)

#Data file
filelist = ['Ex20190826.csv',
            'Ex20190827.csv',
            'Ex20190828.csv',
            'Ex20190829.csv',
            'Ex20190830.csv']

'''Creating the final df for analysis metrics'''

df_analysis = pd.DataFrame(columns = ['Node'])
list_tracker =[]
date_interactions = {}
date_list = []
contact_list =[[],[]]
Density_G1 = []
Density_G2 = []
'''Iterate over all data files'''
for filename in filelist:
    print(filename)
    #DataFrame
    date = filename[2:10]
    date_list.append(date)
    df = pd.read_csv(filename, delimiter=",")
    df = tf.cleanlabel(df) #clean some teacher and unassigned trackers
    #print(df.head())
        
    ''' Data Manipulation'''
    
    #Number of trackers
    numberOfTrackers = et.numberTrackers(df)
    
    # Call the function that enumerates trackers
    df_trackers = et.enumerate_trackers(df)
    list_tracker = Metrics.tracker_list(df_trackers, list_tracker)
    
    #create a dict that change enumeration back to ID
    EnumtoIdDct = df_trackers.set_index('enumeration')['ID'].to_dict()
    #print(df_trackers)
    
    # Asign tracker number to the whole dataset
    df=et.asignEnumTrackers(df, df_trackers)
    #print (df.head())
    
    # DISTANCES in pivot format
    df_pivoted = dt.pivot_table(df)
    #print (df_pivoted)
    
    # fill in the missing value 
    df_pivoted = dt.fillmissing(df_pivoted)
    #print (df_pivoted.head())
    #df_pivoted.to_csv(outfile.format(id='PL'), index = None)

    #One-step process to calculate the proximity matrix
    df_proxemicsLabels = dt.proxemicsLabelssimple(df_pivoted,numberOfTrackers)
    print(df_proxemicsLabels.head())
    
    #Draw social network
    G1, G2, colormapG1, colormapG2 = Vs.networkgraph(df_proxemicsLabels,EnumtoIdDct)
    
    #Calculate density for each SN
    Density_G1.append(nx.density(G1))
    Density_G2.append(nx.density(G2))
    
    Vs.draw_graph(G1, colormapG1,filename,'C1')
    Vs.draw_graph(G2, colormapG2,filename,'C2')

    # dict_list, contact_list = Metrics.interaction_instances(df_proxemicsLabels, EnumtoIdDct, contact_list)
    
    # date_interactions[date] = dict_list
    
# df_analysis['Node'] = list_tracker
# df_analysis = Metrics.metrcis_table(df_analysis,date_list,date_interactions,list_tracker)
# df_analysis, metric_list = Metrics.table_format(df_analysis, date_list)
# df_analysis = Metrics.summative(df_analysis, metric_list)

#df_analysis.to_csv(outfile.format('20190826to30_Close_Contacts'))

