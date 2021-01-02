#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 22 14:12:17 2020

@author: alisha
"""
import all_import_data, funcs, rr_check_data, lt_orderAns, lt_count
import pandas as pd

def mean_and_std(r1, r2):
    
    '''calculate mean diff and std of 2 rounds'''
    
    df_concat = pd.concat((r1, r2))
    by_row_index = df_concat.groupby(df_concat.index)
    df_means = by_row_index.mean()
    df_std = by_row_index.std()
    
    return df_means, df_std

def longterm(df2, sess1, sols, conds, worperro):
    
    '''get long-term results'''
    
    
    ids2, lt_ans, lt_sols = all_import_data.import_lt_data(df2, sess1.numWords)
    
    #find matching indeces
    #this yields (position ID2, ID1)
    matchingind = funcs.find_matching_index(sols.loc[:,'sub_id'], ids2)
    
    #check longterm answers
    lt_ans, _ = rr_check_data.check_data(sess1.numWords, lt_ans, 0, lt_sols,
                                        longterm = True)
    
    #get ids2 in an ordered fashion 
    ids2_ordered = lt_orderAns.order_ids(matchingind, ids2)
    
    #rearange answers in the order from sess1
    ordered_ans = lt_orderAns.orderAns(lt_ans, sols, lt_sols, matchingind, 
                           sess1.numWords, worperro)
    
    #count correct answers per cond (lt1 and lt2 are longterm answers per round)
    results_lt, results_lt1, results_lt2 = lt_count.splitndcount(
            ordered_ans, conds, 6, matchingind, ids2_ordered)
    
    mean_lt_results, std_lt_results = mean_and_std(results_lt1, results_lt2)
    
    return results_lt, results_lt1, results_lt2, ids2_ordered, mean_lt_results, std_lt_results
