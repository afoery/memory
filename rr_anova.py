#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 10:05:01 2020

@author: alisha
"""

import pandas as pd
from statsmodels.stats.anova import AnovaRM

def get_infos(inf, diff1, diff2):
    
    '''extract and edit infos df so that it can be used later in ANOVA'''
    
    infos = inf.loc[:,['gender','nativeLang', 'sub_id']]
    infos = infos.rename(columns = {'sub_id': 'id_control'})
    english = ['English', 'english']
    dic_replace = dict(zip(english, ['e']*2))
    infos = infos.replace(dic_replace)
    infos.loc[~infos["nativeLang"].isin(['e']), "nativeLang"] = "other"
    
    #add infos to df for anova
    diff1 = pd.concat([diff1, infos], axis = 1)
    diff2 = pd.concat([diff2, infos], axis = 1)
    
    return diff1, diff2


def rearange(diffs, time, within_factors, recall = True):
    
    '''rearange df so that we can feed it into anova function'''
    
    #determine whethr we wanna look on recall or recog
    if recall:
        sel = [0,1,2,'sub_id']
    else:
        sel = [3,4,5,'sub_id']

    diffs = diffs.loc[:,sel]
    
    #melt df
    diffs = pd.melt(diffs,id_vars = ['sub_id'],
                           var_name = 'cond', 
                           value_name = 'performance')
    
    #add  information about time
    diffs['time'] = [time for x in range(len(diffs))]
    
    return diffs
    

def anova(diff1, diff2, recall, within_factors):
    
    r = 'recall'
    
    if not recall:
        r = 'recognition'
    
    diff1 = rearange(diff1, 'short', within_factors = within_factors,
                     recall = recall)
    diff2 = rearange(diff2, 'short', within_factors = within_factors, 
                     recall = recall)
    
    diffs_for_anova = pd.concat([diff1,diff2])
    
    #perform anova
    anovarm = AnovaRM(diffs_for_anova, 'performance', 'sub_id', 
                      within = within_factors, aggregate_func = 'mean')
    res = anovarm.fit()
    
    #rounded p value
    p = round(res.anova_table['Pr > F'][0],4)
    
    print(F'ANOVA ON DIFFERENCES in memory performance - {r}', res)
    
    return  diff1, diff2, diffs_for_anova

