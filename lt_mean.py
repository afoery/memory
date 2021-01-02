#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 11:09:34 2020

@author: alisha
"""
import pandas as pd

def mean_over_time(all3rounds_mean_imm, all3rounds_mean_del, lt_res_mean):
    
    #calculate mean of performance of all subjects for each condition 
    mean_overtime = pd.DataFrame({
            'imm': all3rounds_mean_imm.mean(),
            'del': all3rounds_mean_del.mean(),
            'lt':  lt_res_mean.mean()})
    mean_overtime = mean_overtime.drop(['sub_id']).T
    
    std_overtime = pd.DataFrame({
            'imm': all3rounds_mean_imm.std(),
            'del': all3rounds_mean_del.std(),
            'lt':  lt_res_mean.std()})
    std_overtime = std_overtime.drop(['sub_id']).T
    
    return mean_overtime, std_overtime