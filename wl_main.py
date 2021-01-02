#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 17:37:26 2020

@author: alisha
"""

import wl_check, all_import_data, box_plot
import pandas as pd

def wordlist(df, numRounds, conds):

    #wl data
    wl_ans, wl_sol = all_import_data.import_wl(df, numRounds)
    
        
    #calculate difference of freely recalled words [del-imm] 
    wl_diff_withoutorder,wl_ans = wl_check.checkWordList(wl_sol, wl_ans, numRounds, 
                                                      strict = True,
                                                      count_similar_meaning = False)
    
    
    
    #Wordlists: order the diffs and calculate them per condition
    wl_diff_tog, wl_diff_1, wl_diff_2 = wl_check.orderEM(wl_diff_withoutorder,
                                                          conds)
    
    #calculate mean per condition 
    df_concat = pd.concat((wl_diff_1, wl_diff_2))
    by_row_index = df_concat.groupby(df_concat.index)
    df_means = by_row_index.mean()
    


    

    return wl_ans, wl_sol, wl_diff_tog, df_means











