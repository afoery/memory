#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 17:15:26 2020

@author: alisha
"""

from statsmodels.stats.anova import AnovaRM
import pandas as pd

def anova_group(means, recog):
 
    t = 'recall'
    
    if recog:
        t = 'recog'
        
        
    #melt df
    means = pd.melt(means,id_vars = 'sub_id',
                           var_name = 'cond', 
                           value_name = 'performance')
    
    
    
    anovarm = AnovaRM(means, 'performance', 'sub_id', within = ['cond'])
    res = anovarm.fit()
    
    p = round(res.anova_table['Pr > F'][0],4)
    
    print(F'reaction times anova ({t})', res)
    
    return p