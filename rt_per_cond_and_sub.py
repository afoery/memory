#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 10:18:41 2020

@author: alisha
"""

import funcs
import numpy as np
import pandas as pd
import math

def set_mean0_ifNan(mean):
    '''this is just for the control subject.'''
    
    if math.isnan(mean):
        mean = 0
    
    return mean
    

def rt_perCondSub(rt, numRounds, wordsperround, conds, control):
    
    means = []
    
    #split it into blocks of 9 and then assign it to respective cond
    for i in range(len(rt)):
        
        #get individual data (per subject)
        rt_indiv = rt.iloc[i,:].values.flatten().tolist()
        
        #split data into chunks of seven
        rt_indiv = list(funcs.chunks(rt_indiv, wordsperround))
        
        #initiate some lists where we can store data
        closed = []
        video = []
        game = []
        
        #alocate data to respective condition
        for j in range(numRounds):
            
            if conds.loc[i][j] == 'closed':
               
                
                closed = closed+ rt_indiv[j]
            
            elif conds.loc[i][j] == 'video':
                
                video = video + rt_indiv[j]
                
            else: 
    
                game = game + rt_indiv[j]        
                
        #calculate average difference in RT per subject
        mean_closed  = np.nanmean(closed)
        mean_video = np.nanmean(video)
        mean_game = np.nanmean(game)
        
        if control:
            mean_closed = set_mean0_ifNan(mean_closed)
            mean_video = set_mean0_ifNan(mean_video)
            mean_game = set_mean0_ifNan(mean_game)
        
        #append means to one list
        means.append([mean_closed, mean_video, mean_game])
    
    means = pd.DataFrame(means)
    means.columns= ['rest','video','game']
    
    return means


