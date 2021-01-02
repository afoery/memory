#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 20 17:27:49 2020

@author: alisha
"""

import rt_load_data, rt_per_cond_and_sub, rt_plot, rt_anova

def rt(df, sess1, ans_imm, ans_del, numRo1, worperro, conds, ids, control,recog):
    
    #get the reaction times for the imm and del recall
    df_submit_imm = rt_load_data.get_RT_data(sess1.numWords, df, 'i', recog)
    df_submit_del = rt_load_data.get_RT_data(sess1.numWords, df, '', recog)
    
    #subsract immmediate from delayed RTs
    df_submit_diff = df_submit_del - df_submit_imm
    
    #get RTs from correct answers, replace rest with NaN
    rt = rt_load_data.get_RT_from_corrAns(ans_imm, df_submit_diff, sess1.numWords)
    rt = rt_load_data.get_RT_from_corrAns(ans_del, df_submit_diff, sess1.numWords)
    
    #calculate means for each subject per condition
    ids.index = [x for x in range(len(ids))]
    means = rt_per_cond_and_sub.rt_perCondSub(rt, numRo1, worperro, conds, 
                                              control)
    means['sub_id'] = ids
    
    #plot data per subject
    rt_plot. plot_mean_diff_per_sub(means, recog)
    rt_plot.plot_groupmean(means, recog)
    
    #group analysis
    #calculate anova for group
    p_group = rt_anova.anova_group(means, recog)
    
    return means