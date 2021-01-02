#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 20 16:05:56 2020

@author: alisha
"""
import rr_count, rr_anova, rr_plot,rr_calc,rr_mean_diff
import pandas as pd

def recall_recog(ans_imm, ans_del, conds,numRo1, inf, ids, worperro,
                 recall,control):
    
    #calculate how many correct ans per cond
    c_imm1, c_imm2 = rr_count.splitndcount(ans_imm, conds,numRo1 , ids, worperro)
    c_del1, c_del2 = rr_count.splitndcount(ans_del, conds, numRo1, ids, worperro)
    
    #calculate mean difference (delayed - immediate) for each sub for each cond
    diff_mean, diff_std, mean_imm, std_imm, mean_del, std_del, diff1,diff2 = rr_mean_diff.mean_diff(
            c_imm1, c_del1,c_imm2, c_del2)
    
    #calculate group mean per condition
    group_mean = pd.DataFrame(diff_mean.mean()).T
    group_std = pd.DataFrame(diff_mean.iloc[:,[x for x in range(6)]].std()).T
    rr_plot.plot_means_sep(group_mean, group_std)
    
    #get infos about language and edit df so that we can use it for ANOVA
    diff1, diff2 = rr_anova.get_infos(inf, diff1, diff2)
    
    
    #add recall and recog performance together
    diff1_tog = rr_calc.add_recall_regoc(diff1)
    diff2_tog = rr_calc.add_recall_regoc(diff2)
    
    #calculate average of both rounds of recall/recog
    mean_bothrounds = rr_calc.mean_bothrounds(diff1,diff2, recall)
    
    #plot mean of recall and 0.5* recog together
    group_mean_bothrounds = pd.DataFrame(mean_bothrounds.mean()).T
    group_mean_bothrounds.iloc[:,[x for x in range(3)]].plot.bar(
            title = 'recall and 0.5*recog togeter - session 1')
    
    #plot mean differences
    rr_plot.plot_mean_diff_per_sub(diff_mean,diff_std, recall = recall)
    
    #plot performance of each subject 
    rr_plot.plot_performance(mean_imm, mean_del, std_imm, std_del, control, 'Sess 1', 
                           recall = recall)
    
    #1-way-rm anova-type diff_tog if we wanna run Anova on regoc and recall together
    within_factors = ['cond']
    d1,d2, diffs_for_anova = rr_anova.anova(diff1, diff2, recall = recall, 
                             within_factors = within_factors)
    
    return c_imm1,c_imm2, c_del1, c_del2,mean_bothrounds, group_mean,diff1,diff2
    
    
