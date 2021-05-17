# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 11:53:44 2020

@author: yan
"""

import numpy as np 
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt  
from matplotlib.ticker import PercentFormatter

def unique(list1): 
  
    # intilize a null list 
    unique_list = [] 
      
    # traverse for all elements 
    for x in list1: 
        # check if exists in unique_list or not 
        if x not in unique_list: 
            unique_list.append(x) 
    return unique_list

# do the whole things separately for index students and teachers

results = []

# this comes from your contact data

weekly_list = [[55.24,41.15,58.60,66.41,24.02],
               [2.27,	1.63,	2.71,	2.28,	1.12],
               [54.25,	39.50,	65.00,	53.25,	25.75],
               [2.00,	2.50,	1.50,	1.50,	1]]



# from the Lancet paeds paper - risk of infection per contact (interaction)

ci = [[0.0000082,	0.0002274],
      [0.0001000,	0.0268094],
      [0.0001371,	0.0006230],
      [0.0105093,	0.0528047]]

ci1 = [[0.001371,	0.002516],
[0.007528,	0.102671],
[0.001415,	0.002597],
[0.008851,	0.119662],]


label_list = ['S-S','S-T','T-S','T-T'] 
sns.set_context('paper') 
sns.set(rc={'figure.figsize':(4,3),"font.size":20,"axes.titlesize":20,"axes.labelsize":20},style="white")

ylim=0,100
xlim=-0.5,2.5
for i in range(4):
    lower_ci, upper_ci = ci1[i]
    weekly_contacts = weekly_list[i]
    label = label_list[i]
# loop over plausible values to get distribution of secondary infections in classroom 

    for i in range(1000):
        for i_contact in weekly_contacts: 
            for i_risk_per_interaction in np.linspace(lower_ci, upper_ci, 20):
                result = np.random.binomial(i_contact, i_risk_per_interaction)
                results.append(result)

# plot  
    df = pd.DataFrame(dict(x=results))
    plot = plt.figure()
    ax = plot.add_subplot()
    ax = sns.barplot(x="x", y="x", data=df, estimator=lambda x: len(x) / len(df) * 100, palette=("Blues_d"))
    ax.set(ylim=ylim,ylabel="")  
    ax.set(xlim=xlim,xlabel="")
    ax.set_title(label)
    plot.savefig('F:\Research Assitant\COVID-19 Positioning\Data Analysis\Figures\{}.png'.format('Set_2_{}'.format(label)))
    plt.show()
    
    
    
    unique_list = unique(results)
    for n in unique_list:
        proportion  = len([x for x in results if x == n])/len(results)
        print(n, proportion)
    
# =============================================================================
# plot = plt.figure()
# axis = plot.add_subplot(111)
# axis.hist(results, weights=np.ones(len(results)) / len(results))
# =============================================================================
