#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 14:48:55 2020

@author: alisha
"""
import pandas as pd
import funcs 

def orderAns(lt_ans, sols, sols2, matchingind, nuWor, worperro):
    
    sols1 = sols.loc[:,[x for x in range(54)]].copy()
    
    list_ans = []
    
    for i in range(len(matchingind)):
        
        #get index of subject in sess1 & 2
        num1 = matchingind[i][1]
        num2 = matchingind[i][0]
        
        #extract recall and recog answers of individual subject
        recall = lt_ans.loc[num2,[x for x in range(0,nuWor*2,2)]].tolist()
        recog = lt_ans.loc[num2,[x for x in range(1,nuWor*2,2)]].tolist()
        
        #create df with 2 rows: recall & recog
        df = pd.DataFrame([recall, recog])
        #name columns with correct words
        df.columns=sols2.loc[num2]
        
        #rearange df with order of sess1
        df = df[sols1.loc[num1].tolist()]
        
        #create lists
        recall = df.loc[0].values.flatten().tolist()
        recog = df.loc[1].values.flatten().tolist()
        
        #combine lists in alternatig fashion
        orderedAns = [item for pair in zip(recall, recog) for item in pair]
        
        #split into chunks as they were presented in 1th session      
        #append chunked lists to one big list
        list_ans.append(list(funcs.chunks(orderedAns,worperro*2)))
      
    return list_ans


def order_ids(matchingind, ids2):
    
    #get list of ids2 in an ordered fashion
    ids2_ordered = []
    for i in range(len(matchingind)):
        num = matchingind[i][0]
        ids2_ordered.append(ids2[num])
        
    return ids2_ordered


def resultsS1_Sub_in_S2(data,ids2):
    
    #get a new df for sess1 with only subs from sess2
    new = data['sub_id'].isin(ids2)
    data_new = data[new]
    
    #sort df according ids
    data_new = data_new.sort_values('sub_id')
    
    #set indeces correctly
    data_new.index = [x for x in range(len(data_new))]
    
    return data_new

def mean_and_std(r1, r2,r3):
    
    '''calculate mean diff and std of all 3 rounds'''
    
    df_concat = pd.concat((r1, r2,r3))
    by_row_index = df_concat.groupby(df_concat.index)
    df_means = by_row_index.mean()
    df_std = by_row_index.std()
    
    return df_means, df_std

def subs_in_bothsess(imm1, imm2, imm3, del1, del2, del3, ids2_ordered):
    
    ''' 
    1) function ouputs the data of subjects who participated in BOTH sessions
    2) calculates differences between imm and del answers of all 3 rounds
    3) calculates mean of these 3 rounds
    '''
    
    ids = imm1['sub_id'].copy()

    #prepare data so that we can compare sess1 & sess2
    #get dfs of sess1 but only with subs that participated in session 2
    imm1 = resultsS1_Sub_in_S2(imm1, ids2_ordered)
    imm2 = resultsS1_Sub_in_S2(imm2, ids2_ordered)
    imm3 = resultsS1_Sub_in_S2(imm3, ids2_ordered)
    del1 = resultsS1_Sub_in_S2(del1, ids2_ordered)
    del2 = resultsS1_Sub_in_S2(del2, ids2_ordered)
    del3 = resultsS1_Sub_in_S2(del3, ids2_ordered)
    
    #substract immediate performane from delayed --> differences
    diff1 = del1 - imm1
    diff2 = del2 - imm2
    diff3 = del3 - imm3
    
    #add subject id
    diff1['sub_id'] = ids
    diff2['sub_id'] = ids
    diff3['sub_id'] = ids
    
    #calculate mean and std of differences and of imm & del ans alone
    diff_means, diff_std = mean_and_std(diff1, diff2, diff3)
    imm_means, imm_std = mean_and_std(imm1, imm2, imm3)
    del_means, del_std = mean_and_std(del1, del2, del3)
    
    
    return imm_means, del_means, imm_std, del_std






















