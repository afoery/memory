#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 15:50:30 2020

@author: alisha
"""
import pandas as pd

class count:
    
    def __init__(self, data):
        
        '''count correct recall and recog trials'''
        
        #all trials together per condition
        self.recall = data.count('recallCorrect')
        self.recog = data.count('recogCorrect')
        
        #in session 1, we had 2 rounds of each condition
        #here we have the counts divided into counts per round
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


def splitndcount(lt_ans, conds, nuRou, matchind, ids):
    
    counts, counts_sep1, counts_sep2 = ([] for i in range(3))

    for i in range(len(lt_ans)):
        
        #get index of subject from sess1
        num1 = matchind[i][1]
        
        #initialize some lists
        closed, video, game = ([] for i in range(3))
        
        #assign trials to individual conditions
        for j in range(nuRou):
            
            #select individual data
            ans = lt_ans[i][j]
            
            if conds.loc[num1][j] == 'closed':
                closed += ans
                
            elif conds.loc[num1][j] == 'video':
                video += ans
            
            else:
                game += ans
        
        #count correctly answered trials
        count_r = count(closed)
        count_v = count(video)
        count_g = count(game)
        
        #append to one big list
        counts.append([count_r.recall, count_v.recall, count_g.recall,
                       count_r.recog, count_v.recog, count_g.recog])   
    
        counts_sep1.append(
                [count_r.recall1, count_v.recall1, count_g.recall1, 
                 count_r.recog1, count_v.recog1, count_g.recog1])
        counts_sep2.append(
                [count_r.recall2, count_v.recall2, count_g.recall2, 
                 count_r.recog2, count_v.recog2, count_g.recog2])

    #transform into df, add ids, and sort according to ids
    counts = rearange(counts, ids)
    counts_sep1 = rearange(counts_sep1, ids)
    counts_sep2 = rearange(counts_sep2, ids)

    return counts, counts_sep1, counts_sep2
            
         
