#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 29 18:58:50 2020

@author: alisha
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import rcParams
import numpy as np
import rr_normality
from scipy.stats import levene, bartlett
from scipy import stats
from statsmodels.stats.anova import AnovaRM
import scikit_posthocs as sp

    # customized settings
params = {  # 'backend': 'ps',
    'font.family': 'serif',
    'font.serif': 'Latin Modern Roman',
    'font.size': 16,
    'axes.labelsize': 'large',
    'axes.titlesize': 'large',
    'legend.fontsize': 'small',
    'xtick.labelsize': 'small',
    'ytick.labelsize': 'small',
    'savefig.dpi': 300,
    'text.usetex': True}
# tell matplotlib about your params
rcParams.update(params)

# set nice figure sizes
fig_width_pt = 300    # Get this from LaTeX using \showthe\columnwidth
golden_mean = (np.sqrt(5.) - 1.) / 2.  # Aesthetic ratio
ratio = golden_mean
inches_per_pt = 1. / 72.27  # Convert pt to inches
fig_width = fig_width_pt * inches_per_pt  # width in inches
fig_height = fig_width * ratio  # height in inches
fig_size = [fig_width, fig_height]
rcParams.update({'figure.figsize': fig_size})
#colors
r = [250/255, 103/255, 80/255]
lb = [167/255, 198/255, 250/255]
b = [14/255, 72/255, 173/255]
colors = [r,lb,b]

diffs_mean_recall = pd.read_csv('diffs_mean_recall.csv')
diffs_mean_recog = pd.read_csv('diffs_mean_recog.csv')

lt_diffs_recall =  pd.read_csv('lt_diffs_recall.csv')
lt_diffs_recog =  pd.read_csv('lt_diffs_recog.csv')

rt_recall = pd.read_csv('rt_recall.csv')
rt_recog = pd.read_csv('rt_recog.csv')

ids = diffs_mean_recall['sub_id']
lt_diffs_recall['sub_id'] = ids
lt_diffs_recog['sub_id'] = ids




wordlist = pd.read_csv('wl_means.csv')
wordlist['sub_id'] = ids


all_data = [diffs_mean_recall, diffs_mean_recog, 
            rt_recall, rt_recog,
            lt_diffs_recall, lt_diffs_recog, 
            wordlist]



def levene_test(data):
    s1,p1 = levene(data.iloc[:,0], data.iloc[:,1], data.iloc[:,2])
    s2,p2 = bartlett(data.iloc[:,0], data.iloc[:,1], data.iloc[:,2])
    
    res = [s1, p1, s2, p2]
    res = [round(x,2) for x in res]
    
    return res



results = []
for i in range(len(all_data)):
    res= levene_test(all_data[i])
    results.append(res)

results = pd.DataFrame(results)

results.columns = ['test statistic','p-value','test statistic','p-value']
results.index =  ['recall_8', 'recog_8',
                  'rt_recall_8', 'rt_recog_8',
                  'recall_lt','recog_lt',
                  'wordlist']


def shapiro(data):
    res = []
    
    for i in range(3):
        t,p = stats.shapiro(data.iloc[:,i])
        
        t = round(t,2)
        p = round(p,2)
    
        res.append([t,p])
    return res


shapiro_l = []
for i in range(len(all_data)):
    res1 = shapiro(all_data[i])
    shapiro_l.extend(res1)

shapiro_l = pd.DataFrame(shapiro_l)



rt_recog = rt_recog[rt_recog.loc[:,'sub_id'] != 62753]

def friedman(data):
    res = []
    t,p = stats.friedmanchisquare(data.iloc[:,0], data.iloc[:,1], 
                                data.iloc[:,2])
    t = round(t,2)
    p = round(p,2)
    res.append([t,p])
    return res



friedman_l = []
for i in range(len(all_data)):
    res2 = friedman(all_data[i])
    friedman_l.extend(res2)

friedman_l = pd.DataFrame(friedman_l)


friedman_recog = friedman(rt_recog)
rr_normality.qq_plot(rt_recog,recall = True)
nemeny_recog = sp.posthoc_nemenyi_friedman(rt_recog.iloc[:,[0,1,2]])
print('-----------',friedman_recog,nemeny_recog,'-------')



def anova(data):
    
    data = pd.melt(data,id_vars = 'sub_id',  var_name = 'cond',
                   value_name = 'performance')
    
#    #perform anova
    anovarm = AnovaRM(data, 'performance', 'sub_id', within = ['cond'])
    res = anovarm.fit()
    
    #rounded p value
    p = round(res.anova_table['Pr > F'][0],2)
    F = round(res.anova_table['F Value'][0],2)
#    print(F'ANOVA ON DIFFERENCES in memory performance - {r}', res)
    print(F,p)
    
    res2 = [[F,p]]
    
    return res2
    
    

    

anova_l = []
for i in range(len(all_data)):
    res2 = anova(all_data[i])
    anova_l.extend(res2)

anova_l = pd.DataFrame(anova_l)
    
    
    
    
    
    
    
    
    
    
    
    
    
    




