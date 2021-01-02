#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 10:42:11 2020

@author: alisha
"""
import pandas as pd


def mean(data1, data2, ids):
    
    ''' calculate the mean and std of 2 dfs'''
    
    #calculate mean & std of both rounds      
    df_concat = pd.concat((data1, data2))
    by_row_index = df_concat.groupby(df_concat.index)
    df_means = by_row_index.mean()
    df_means['sub_id']= ids
    df_std = by_row_index.std()
    df_std['sub_id']= ids
    
    return df_means, df_std
    
    
def mean_diff(sep_1_imm, sep_1_del, sep_2_imm, sep_2_del):
    
    ids = sep_1_del.loc[:,'sub_id']
    
    #calculate difference between immediate and delayed answers
    diff1 = sep_1_del - sep_1_imm
    diff2 = sep_2_del - sep_2_imm
    #add ids
    diff1['sub_id'] = ids
    diff2['sub_id'] = ids
    
    #calculate mean and std of diff1 and diff2
    df_diff_mean, df_diff_std = mean(diff1,diff2, ids)
    
    #calculate mean of immediate and delayed responses
    df_imm_mean, df_imm_std = mean(sep_1_imm,sep_2_imm, ids)
    df_del_mean, df_del_std = mean(sep_1_del,sep_2_del, ids)
    
    
    return df_diff_mean, df_diff_std, df_imm_mean, df_imm_std, df_del_mean, df_del_std, diff1, diff2