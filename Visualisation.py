# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 10:48:08 2020

@author: yan
"""

import networkx as nx
import matplotlib.pyplot as plt
import community as community_louvain
import matplotlib.cm as cm
import collections

def subject_level(node, input_subject, dfinfo):
    
    if input_subject =='Maths' or input_subject == 'Reading':
        subject_dict = dfinfo.set_index('Student')[input_subject].to_dict()
        IDlabel = node.split('_')[1].strip('0')  
        if IDlabel in subject_dict:
            nodelvl = subject_dict[IDlabel]
        else:
            nodelvl = 'None'
    else:
        nodelvl = 'None'      
    return nodelvl

def networkgraph(df_proxemicsLabels,EnumtoIdDct):
    
    #create a empty graph
    G1 = nx.Graph()
    G2 = nx.Graph()
    
    
    
    
    #assign nodes and create edge between each pair if label occurred at least once
    for col in df_proxemicsLabels.columns[1:]:
        a,b = [EnumtoIdDct[int(k)] for k in col.split('_')]
                    
        interaction_time = (df_proxemicsLabels[col] == 1).sum()
        collocation_time = (df_proxemicsLabels[col] == 2).sum()
        
        Time_missing = df_proxemicsLabels[col].isna().sum()
        Total_time = len(df_proxemicsLabels)
        Time_present = Total_time - Time_missing
                
        if Time_present/Total_time > 0.2:
        #Graph for 1m and 15mins
            if interaction_time > 900:         
                G1.add_edge(a, b)   
            else:
                G1.add_nodes_from([a,b])
        
        #Graph for 5m and 40mins
            if collocation_time > 2400:         
                G2.add_edge(a, b)   
            else:
                G2.add_nodes_from([a,b])               
        
    colormapG1 = []
    for node in G1:
        if "Teacher" in node:
            colormapG1.append('deepskyblue')

        else:
            colormapG1.append('red')
    
    colormapG2 = []
    for node in G2:
        if "Teacher" in node:
            colormapG2.append('deepskyblue')

        else:
            colormapG2.append('red')

    return G1, G2, colormapG1, colormapG2

def draw_graph(G1, colormapG1, filename, criteria):
    #using spring layout to draw the network graph
    pos = nx.spring_layout(G1,k=1.5,iterations=30)
    #adjust the node size based on node degree
    d = dict(G1.degree)
    edges = G1.edges()
    
    plt.figure(figsize=(12,12))
    
    if criteria == 'C1':
        w = 10
    else:
        w = 5
    
    
    nx.draw(G1, 
            pos, 
            edges=edges,
            edge_color = 'tab:gray', 
            node_color = colormapG1, 
            node_size=[(50+v * w) for v in d.values()])
    #nx.write_gexf(G, "{id}.gexf".format(id=(filename[:10] + '_' + day + '_' + input_subject)))
    #Gdf = nx.to_pandas_edgelist(G)
    #print(Gdf.head())
    
    plt.savefig('F:\Research Assitant\COVID-19 Positioning\Data Analysis\Figures\{}.png'.format(filename[2:10] + '_' + criteria))
    plt.show()

    degree_sequence = sorted([d for n, d in G1.degree()], reverse=True)  # degree sequence
    degreeCount = collections.Counter(degree_sequence)
    deg, cnt = zip(*degreeCount.items())
    cnt = [100*x/sum(cnt) for x in list(cnt)]

    fig, ax = plt.subplots(figsize=(8,4))
    plt.bar(deg, cnt, width=0.8, color="deepskyblue")

    plt.ylabel("Precentage of nodes",fontsize=14)
    plt.xlabel("Degree",fontsize=14)
    plt.xlim([0, 100])
    plt.ylim([0,14])
    
    plt.savefig('F:\Research Assitant\COVID-19 Positioning\Data Analysis\Figures\{}.png'.format(filename[2:10] + '_' + criteria + '_DD'))
    plt.show()

