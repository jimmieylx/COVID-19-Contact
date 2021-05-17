# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 16:57:04 2020
This script contain all the functions that required to prepare the data for
calculate the proximity matrix
@author: yan
"""
#calculate the number of unique IDs
def numberTrackers(df):
    tracker = df.ID.unique()
    return len(tracker)

#assign an number to each ID starting from 1 to the total number of unique IDs
def enumerate_trackers(df):
    df_trackers = df.groupby(['ID'], as_index=False)['TIME'].count()
    df_trackers = df_trackers[['ID']].set_index('ID')
    prev_index = '-1'
    cont = 0
    enumeration = []
    for index, track in df_trackers.iterrows():
        if (index != prev_index):
            cont = cont + 1
        else:
                cont = 1
        enumeration.append(cont)
        prev_index = index
    df_trackers['enumeration'] = enumeration
    df_trackers.reset_index(level=0, inplace=True)      
    return df_trackers

#assign the enumtrackers to the whole df
def asignEnumTrackers(df, enum_trackers):
    #create a dict that contains all the mapping ID:Enumeration
    IdtoEnumDct = enum_trackers.set_index('ID')['enumeration'].to_dict()
    #create an enumeration from mapping ID to the dict
    df['enumeration'] = df['ID'].map(IdtoEnumDct)
    return df
