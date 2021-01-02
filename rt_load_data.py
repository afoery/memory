#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 10:54:30 2020

@author: alisha
"""

import pandas as pd
import numpy as np

def get_RT_data(numWords, df, acronym_q, recog):
    
    #define which columns we are looking for
    #even numbers = recall data
    cols_to_find = [F'{acronym_q}%d'%i for i in range(numWords*2) if i%2 == 0]
    
    if recog: 
        #define which columns we are looking for
        #uneven numbers is where recognition is located
        cols_to_find = [F'{acronym_q}%d'%i for i in range(numWords*2) if i%2 != 0]        

    #get position of answers
    loc = [df.columns.get_loc(col) for col in cols_to_find]

    #get the position of the submit columns (add 3)
    loc_submit = [(i+3) for i in loc]

    #create df with submit values
    df_submit = df.iloc[:,loc_submit]

    #rename columns
    df_submit.columns = [i for i in range(numWords)]

    #covert all values to floats
    df_submit = df_submit.apply(pd.to_numeric)
    
    return df_submit


def get_RT_from_corrAns(ans, rt, numWords):
    
    '''this function outputs a dataframe for the RTs of answers
    that were correct
    '''
    
    #select recall data (only every 2nd)
    recall = ans[[x for x in range(numWords*2) if x%2 == 0]]
    
    #if recall was incorrect, replace RT with NaN
    for i in range(len(rt)):
        for j in range(numWords):
            
            if recall.iloc[i,j] != 'recallCorrect':
                rt.iloc[i,j] = np.NaN
                
    return rt
    










    