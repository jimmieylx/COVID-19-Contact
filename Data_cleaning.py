# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 14:59:58 2020
Run this script and type in the Path of dataset folder.
The cleaned data will outputed into the same folder with EX infornt of the dates as filename
e.g. input 20190908.log, output EX20190908.csv
@author: yan
"""
import Transformation as tf
import pandas as pd
import glob

indir = input("indicate Path of dataset folder: ")
outfile = indir + '\EX{id}.csv'

#change file extension to .csv
tf.extensiontocsv (indir)

#create a list containing all the filename in the folder
fileList=glob.glob("*.csv")
date = fileList[0][:8]
dfList = []
for filename in fileList:
    #transform data from many columns into fewer columns but many rows
    df = tf.stackingcolumns (filename)
    df = tf.converttime(df)
    df = tf.cleanlabel(df)
    #append the df if filename are in the same data
    if filename[:8] == date:
            dfList.append(df)
    # Otherwise, export the current list to a CSV file
    else:
            concatDf=pd.concat(dfList,axis=0)
            #segment school times only
            segconcatDf = tf.segmentation(concatDf)
            #normalise to 1 datapoint per second
            normconcatDf = tf.normalisation (segconcatDf)
            #include a day of week column
            concatDf = tf.dayofweek(normconcatDf)
            concatDf.to_csv(outfile.format(id=date), index = None)
            print(concatDf.head())
            # Empty the list, append the df to the new list, and set date as the current file
            dfList=[]
            dfList.append(df)
            date = filename[:8]
#export the final list into a csv file
concatDf=pd.concat(dfList,axis=0)
segconcatDf = tf.segmentation(concatDf)
normconcatDf = tf.normalisation (segconcatDf)
concatDf = tf.dayofweek(normconcatDf)
concatDf.to_csv(outfile.format(id=date), index = None)
print(concatDf.head())