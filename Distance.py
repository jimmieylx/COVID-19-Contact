# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 10:16:26 2020

This approach calculate distance and asign proxemics in one step

@author: yan
"""
import numpy as np
import pandas as pd
#to calculate the distances the first step we made is to pivote the table
#it could be done other way.. if we change this, the calculation of distances might change
def pivot_table(df):
    df_pivot = df.pivot_table(
        index=['TIME'],
        columns='enumeration',
        values=["X", "Y"]).reset_index()
    df_pivot.reset_index(level=0, inplace=True)
    return df_pivot


#filling in missing data using linear interpolation
def fillmissing(df_pivoted):
    df_pivoted['X']=df_pivoted['X'].interpolate(method='linear',axis=0, limit = 60, limit_direction = 'both', limit_area = 'inside')
    df_pivoted['Y']=df_pivoted['Y'].interpolate(method='linear',axis=0, limit = 60, limit_direction = 'both', limit_area = 'inside')
    return df_pivoted

'''One-step process to calculate the proximity matrix'''
#Input: pivoted dataframe, number of tracker
#Output: proximity matrix

def proxemicsLabelssimple(df_pivoted, numberOfTrackers):
    df_proxemics = pd.DataFrame(columns = ['TIME'])
    df_proxemics['TIME'] =  df_pivoted['TIME']
    for x in range(1, numberOfTrackers):
        for i in range(x + 1, numberOfTrackers + 1):
            PLables_column_name = str(x) + '_' + str(i)
            df_proxemics[PLables_column_name] = (np.sqrt((df_pivoted['X', i] - df_pivoted['X', x]) ** 2 + (
                        df_pivoted['Y', i] - df_pivoted['Y', x]) ** 2)).map(lambda x: proxemics(x))
    #df_pivoted.drop(['X', 'Y',], axis=1, level = 0, inplace = True)
    #df_pivoted.columns= df_pivoted.columns.droplevel(level = 1)    
    return df_proxemics

'''Two-step process to calculate the proximity matrix'''
#Input: pivoted dataframe, number of tracker
#Output: distance matrix, proximity matrix

def distancesBetweenTrackers(df_pivoted, numberOfTrackers):
    for x in range(1, numberOfTrackers):
        for i in range(x + 1, numberOfTrackers + 1):
            PLables_column_name = 'D_' + str(x) + '_' + str(i)
            df_pivoted[PLables_column_name] = (np.sqrt((df_pivoted['X', i] - df_pivoted['X', x]) ** 2 + (
                        df_pivoted['Y', i] - df_pivoted['Y', x]) ** 2))
    df_pivoted.drop(['X', 'Y',], axis=1, level = 0, inplace = True)
    df_pivoted.columns= df_pivoted.columns.droplevel(level = 1)    
    return df_pivoted

def proxemicsLabels(df_distancesBetTrackers):
    columns = list(df_distancesBetTrackers)[2:]
    for col in columns:
        df_distancesBetTrackers[col] = df_distancesBetTrackers[col].map(lambda x: proxemics(x))
    return df_distancesBetTrackers

#assign proximity label to the distance
#distance are choosen based on the findings of two papers
    #Hall, E. T. (1966). The hidden dimension. New York, NY: Doubleday.
    #Sorokowska, A., Sorokowski, P., Hilpert, P., Cantarero, K., Frackowiak, T., Ahmadi, K., ... & Blumen, S. (2017). Preferred interpersonal distances: a global comparison. Journal of Cross-Cultural Psychology, 48(4), 577-592.
def proxemics(x):
    # 0=intimate, 1=personal, 2=social, 3=public, 999=other values
    if 1.5>= x >= 0:
        x = 1
    elif 5 >= x > 1.5:
        x = 2
    elif x > 5:
        x = 0
    else:
        x = np.NaN
    return x