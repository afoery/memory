#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 16:06:58 2020

@author: alisha
"""
import pandas as pd
import funcs

class count:
    
    def __init__(self, data):
        
        self.recall1 = data[0:18].count('recallCorrect')
        self.recall2 = data[18:36].count('recallCorrect')
        
        self.recog1 = data[0:18].count('recogCorrect')
        self.recog2 = data[18:36].count('recogCorrect')

def rearange(data, ids):
    '''transform data into df, add ids, and sort
    '''
    data = pd.DataFrame(data) #df
    data['sub_id'] = ids #add id column
    data = data.sort_values('sub_id') #sort according id
    data.index = [x for x in range(len(data))] #reset indeces

    return data


def splitndcount(answers, conds, nuRou, ids, wordsperro):
    
    counts, counts_sep1, counts_sep2 = ([] for i in range(3))

    for i in range(len(answers)):
        
        #get individual data (per subject)
        data_indiv = answers.loc[i].values.flatten().tolist()
        
        #split data into chunks as presented in study (different rounds)
        data_indiv = list(funcs.chunks(data_indiv,wordsperro*2))
        
        #initialize some lists
        closed, video, game = ([] for i in range(3))
        
        #assign trials to individual conditions
        for j in range(nuRou):
            
            #select individual data
            ans = data_indiv[j]
            
            if conds.loc[i][j] == 'closed':
                closed += ans
                
            elif conds.loc[i][j] == 'video':
                video += ans
            
            else:
                game += ans
        
        #count correctly answered trials
        count_r = count(closed)
        count_v = count(video)
        count_g = count(game)
        
        counts_sep1.append(
                [count_r.recall1, count_v.recall1, count_g.recall1, 
                 count_r.recog1, count_v.recog1, count_g.recog1])
        counts_sep2.append(
                [count_r.recall2, count_v.recall2, count_g.recall2, 
                 count_r.recog2, count_v.recog2, count_g.recog2])

    #transform into df, add ids, and sort according to ids
    counts_sep1 = rearange(counts_sep1, ids)
    counts_sep2 = rearange(counts_sep2, ids)
    

    return counts_sep1, counts_sep2
            
         