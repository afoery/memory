#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 09:48:51 2020

@author: alisha
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import rcParams
import numpy as np

    # customized settings
params = {  # 'backend': 'ps',
    'font.family': 'serif',
    'font.serif': 'Latin Modern Roman',
    'font.size': 22,
    'axes.labelsize': 'medium',
    'axes.titlesize': 'small',
    'legend.fontsize': 'small',
    'xtick.labelsize': 'medium',
    'ytick.labelsize': 'medium',
    'savefig.dpi': 300,
    'text.usetex': True}
# tell matplotlib about your params
rcParams.update(params)

# set nice figure sizes
fig_width_pt = 300    # Get this from LaTeX using \showthe\columnwidth
golden_mean = (np.sqrt(5.) - 1.) / 2.  # Aesthetic ratio
ratio = golden_mean
inches_per_pt = 1. / 72.27  # Convert pt to inches
fig_width = fig_width_pt * inches_per_pt  # width in inches
fig_height = fig_width * ratio  # height in inches
fig_size = [fig_width, fig_height]
rcParams.update({'figure.figsize': fig_size})
#colors
r = [250/255, 103/255, 80/255]
lb = [167/255, 198/255, 250/255]
b = [14/255, 72/255, 173/255]
colors = [r,lb,b]

diffs_mean_recall = pd.read_csv('diffs_mean_recall.csv')
diffs_mean_recog = pd.read_csv('diffs_mean_recog.csv')

lt_diffs_recall =  pd.read_csv('lt_diffs_recall.csv')
lt_diffs_recog =  pd.read_csv('lt_diffs_recog.csv')

rt_recall = pd.read_csv('rt_recall.csv')
rt_recog = pd.read_csv('rt_recog.csv')


wordlist = pd.read_csv('wl_means.csv')

#diffs_mean_recall.iloc[:,[0,1,2]].boxplot()
#diffs_mean_recog.iloc[:,[0,1,2]].boxplot()

#rt_recall.iloc[:,[0,1,2]].boxplot()
#rt_recog.iloc[:,[0,1,2]].boxplot(color = colors)

#sns.set_theme() #default theme of seaborn
sns.set_style("darkgrid", {"axes.facecolor": "0.955"})

def boxplot(data):
    
    data = data.iloc[:,[0,1,2]]
    
    ax = sns.boxplot(data = data, color = 'w')
    
    
    medians = data.median().round(1)
    
    for xtick in ax.get_xticks():
#        ax.text(xtick,medians[xtick] + 0.05, medians[xtick],
#                horizontalalignment='center',size='x-small',color='w',
#                weight=1000)
        
        ax.set_ylabel('Mean Differences')
        print(xtick)
        
        r = 0.05
        x = [xtick + np.random.normal(-r,r) for x in range(len(data))]
        ax.scatter(x, data.iloc[:,xtick], color = colors[xtick], alpha = 0.7,
                   s = 11)
        
        print(x)
    ax = sns.boxplot(data = data, color = 'w')
    ax.set_xticklabels(['Rest','Video','Game'])
    

    for i,artist in enumerate(ax.artists):

        # Each box has 6 associated Line2D objects (to make the whiskers, fliers, etc.)
        # Loop over them here, and use the same colour as above
        n = 6
        for j in range(i*n+4,i*n+(n)):
            
            line = ax.lines[j]
            line.set_color('black')


    return medians


medians = boxplot(lt_diffs_recog)












