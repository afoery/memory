#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 17 09:59:45 2020

@author: Alisha Föry
"""

import funcs, all_import_data, rr_check_data, rt_main, s2_new_rounds_main
import rr_main,lt_orderAns, rr_normality, lt_main, lt_mean, lt_plot
import rr_mean_diff, wl_main
from scipy.stats import friedmanchisquare
import scipy.stats as stats
import scikit_posthocs as sp

#import variables of both sessions        
sess1 = funcs.session(6, 'data5')
sess2 = funcs.session(3, 'data_sess2')
numRo1 = 6
numRo2 = 3
worperro = 9

#keep control subject?
control = False

#recall or recog?
recall = True   

#import data s1
df = all_import_data.import_df(sess1.datapath, control, onlyFem = False, 
                               onlyMen = False, pos_rest = False,
                               onlyEnglish = False, onlyForeign = False,
                               only_gamers = False)

#extract relevant data
ids, ans_imm, ans_del, sols, conds, inf, fb = all_import_data.import_basicdata(
        df, sess1.numWords)


#check data
ans_imm, ans_del = rr_check_data.check_data(sess1.numWords,ans_imm, ans_del, 
                                            sols)

#statistical analyses of recall and recog data
imm1,imm2, del1, del2, diffs_mean, group_mean,d1,d2= rr_main.recall_recog(ans_imm, 
                                                                    ans_del, 
                                                         conds,numRo1, inf, 
                                                         ids, worperro, 
                                                         recall,control)

#friedman test (non-parametrical test)
def friedman(data):
    stat, p = friedmanchisquare(data.iloc[:,0], data.iloc[:,1], 
                                data.iloc[:,2])

    print('Friedmann=%.3f, p=%.3f' % (stat, p))




# stats analysis of reaction times for recall data
rt_recall = rt_main.rt(df, sess1, ans_imm, ans_del, numRo1, worperro, conds, 
                       ids, control,recog = False)

#analysis of reaction times for recog data
rt_recog = rt_main.rt(df, sess1, ans_imm, ans_del, numRo1, worperro, conds, 
                      ids, control,recog = True)




friedman(diffs_mean)

nemeny_p= (sp.posthoc_nemenyi_friedman(rt_recog.iloc[:,[0,1,2]])).round(3)
  

#------------------------------SESSION 2--------------------------------------

print('------------SESSION2----------')


#LONGTERM
#import data from sess2
df2 = all_import_data.import_df2(sess2.datapath, control)

#get long-term results
_, lt1, lt2, ids2_ordered, lt_res_mean, lt_res_std =  lt_main.longterm(
        df2, sess1, sols, conds, worperro)

#calculate differences between longterm and immediate trials
imm1_in2 = lt_orderAns.resultsS1_Sub_in_S2(imm1, ids2_ordered)
imm2_in2 = lt_orderAns.resultsS1_Sub_in_S2(imm2, ids2_ordered)

diffs_mean_lt, _, _, _, _, _, diff1, diff2 = rr_mean_diff.mean_diff(imm1_in2, lt1, 
                                                                    imm2_in2, lt2)


lt_shapiro = stats.shapiro(diffs_mean_lt.iloc[:,[0,1,2]])

#get results of new learning rounds in sess2
imm3, del3 = s2_new_rounds_main.new_learning_s2(df2, sess2, numRo2, worperro)

#calculate differences in recall/recog for each round from both sess1 & 2
all3rounds_mean_imm, all3rounds_mean_del,all3rounds_std_imm,all3rounds_std_del  = lt_orderAns.subs_in_bothsess(
        imm1, imm2, imm3, del1, del2, del3, ids2_ordered)

#plot performance over time
lt_plot.plot_overtime(all3rounds_mean_imm, all3rounds_mean_del,
                      lt_res_mean, all3rounds_std_imm, all3rounds_std_del,
                      lt_res_std, recall)

#calculate mean of performance of all subjects for each condition 
mean_overtime, std_overtime = lt_mean.mean_over_time(
        all3rounds_mean_imm, all3rounds_mean_del, lt_res_mean)

#plot group means over time
#lt_plot.plot_mean_overtime(mean_overtime, std_overtime,recall)






#QQ PLOTS AND PDF

    
#test normality of data
# QQ plot
rr_normality.qq_plot(diffs_mean, recall)
rr_normality.qq_plot(rt_recog, recall, rt = True)

#probability density function
rr_normality.pdf(diffs_mean, recall)
rr_normality.pdf(rt_recog, recall, rt = True)


rr_normality.qq_plot(diffs_mean_lt,recall)
rr_normality.pdf(diffs_mean_lt, recall)





#----------------------------------------------------------------------

#WORDLIST TASK

wl_ans, wl_sol, wl_diff,wl_means = wl_main.wordlist(df, numRo1, conds)


rr_normality.qq_plot(wl_means,recall)









