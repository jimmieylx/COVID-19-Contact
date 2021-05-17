# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 14:04:14 2020

@author: yan
"""
import pandas as pd
import numpy as np
import math
import re
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.cm as cm

def tracker_list(df_trackers, list_tracker):
    
    present_tracker = list(df_trackers['ID'].values)
    
    for tracker in present_tracker:
        if 'Student' in tracker and tracker not in list_tracker:
            list_tracker.append(tracker)
        if 'Teacher' in tracker and tracker not in list_tracker:
            list_tracker.append(tracker)
    
    return list_tracker


def interaction_instances(df_proxemicsLabels, EnumtoIdDct, contact_list):
    
    dict_student_contact = {}
    dict_teacher_contact = {}
    dict_student_collocation = {}
    dict_teacher_collocation = {}
    
    dict_list = [dict_student_contact, dict_teacher_contact, dict_student_collocation, dict_teacher_collocation]
    
    for col in df_proxemicsLabels.columns[1:]:
        a,b = [EnumtoIdDct[int(k)] for k in col.split('_')]  
        for dict_n in dict_list:
            if a not in dict_n:
                dict_n[a] = 0
            if b not in dict_n:
                dict_n[b] = 0
                
        interaction_time = (df_proxemicsLabels[col] == 1).sum()
        
        if interaction_time >= 900:
            #if (a,b) not in contact_list[0]:
            if 'Student' in b:
                dict_student_contact[a] += 1
            else:
                dict_teacher_contact[a] += 1
                
            if 'Student' in a:
                dict_student_contact[b] += 1
            else:
                dict_teacher_contact[b] += 1
                
            #contact_list[0].append((a,b))             
        
        collocation_time = (df_proxemicsLabels[col] == 2).sum()
        
        if collocation_time >= 2400:
            #if (a,b) not in contact_list[1]:
            if 'Student' in b:
                dict_student_collocation[a] += 1
            else:
                dict_teacher_collocation[a] += 1
                
            if 'Student' in a:
                dict_student_collocation[b] += 1
            else:
                dict_teacher_collocation[b] += 1
            #contact_list[1].append((a,b))  
    
    return dict_list, contact_list
            
def metrcis_table(df_analysis,date_list,date_interactions,list_tracker):
    
    for date in date_list:
        
        
        df_analysis[date+'_'+'student15'] = df_analysis['Node'].map(lambda x: 
                                                             date_interactions[date][0][x] 
                                                             if x in date_interactions[date][0] else 0)
        df_analysis[date+'_'+'teacher15'] = df_analysis['Node'].map(lambda x: 
                                                             date_interactions[date][1][x] 
                                                             if x in date_interactions[date][1] else 0)
        df_analysis[date+'_'+'student40'] = df_analysis['Node'].map(lambda x: 
                                                             date_interactions[date][2][x] 
                                                             if x in date_interactions[date][2] else 0)
        df_analysis[date+'_'+'teacher40'] = df_analysis['Node'].map(lambda x: 
                                                             date_interactions[date][3][x] 
                                                             if x in date_interactions[date][3] else 0)
        df_analysis[date+'_'+'studentAll'] = df_analysis[date+'_'+'student15'] + df_analysis[date+'_'+'student40']
        df_analysis[date+'_'+'teacherAll'] = df_analysis[date+'_'+'teacher15'] + df_analysis[date+'_'+'teacher40']
    
    return df_analysis

def table_format(df_analysis, date_list):
    
    metric_list =  []
    date_list = []
    
    df_analysis.set_index('Node',inplace = True)

    for colname in df_analysis.columns:
        date,metric = colname.split('_')
        if date not in date_list:
            date_list.append(date)
        if metric not in metric_list:
            metric_list.append(metric)

    df_analysis.columns = pd.MultiIndex.from_product([date_list, metric_list])
    
    return df_analysis, metric_list

def summative(df_analysis, metric_list):
    
    for metric in metric_list:
        
        df_analysis['Summative',metric] = df_analysis.iloc[:, df_analysis.columns.get_level_values(1)==metric].sum(axis=1)
        
    return df_analysis