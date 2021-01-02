#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 16:24:40 2020

@author: alisha
"""
import pandas as pd

def plot_mean_diff_per_sub(df_mean, recog):
    
    t = 'recall'
    
    if recog:
        t = 'recog'
    #colors
    r = [250/255, 103/255, 80/255]
    lb = [167/255, 198/255, 250/255]
    b = [14/255, 72/255, 173/255]
    
    sel = ['rest','video','game']
    ax = df_mean.loc[:,sel].plot.bar(
            title = F'Mean Differences Per Subject -{t} (Reaction times, Session 1)',
            color = [r,lb,b])
    
    ax.set_xlabel('Subjects')
    ax.set_ylabel('Mean differences in time [delayed - immediate]')
    

def plot_groupmean(means, recog):
    
    t = 'recall'
    
    if recog:
        t = 'recog'
    
    #calculate and plot average of group
    group_mean = pd.DataFrame({'rest': [means['rest'].mean()],
                               
                               'video':[means['video'].mean()],
                               'game': [means['game'].mean()]})
    group_std = pd.DataFrame({'rest': [means['rest'].std()],
                               
                               'video':[means['video'].std()],
                               'game': [means['game'].std()]})
    
    #colors
    r = [250/255, 103/255, 80/255]
    lb = [167/255, 198/255, 250/255]
    b = [14/255, 72/255, 173/255]
        
    ax = group_mean.plot.bar(
            title = F'Mean Differences - {t} (Reaction times, Session 1)',
            yerr = group_std, capsize = 8, 
            color = [r,lb,b])
    
    ax.set_xlabel('Conditions')
    ax.set_ylabel('Mean differences [delayed - immediate]')
#    ax.text(0.3,0.3, F'P = {p}')