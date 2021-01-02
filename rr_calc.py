#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 20 15:40:23 2020

@author: alisha
"""

def add_recall_regoc(diff):
    
    sub_id = diff.loc[:,'sub_id'].copy()
    
    '''add recog and 0.5*recall performance'''
    recall = diff.loc[:,[0,1,2]]
    recog = diff.loc[:,[3,4,5]]
    
    recog.columns = [0,1,2]
    
    together = recall.add(0.5*recog)
    
    together['sub_id'] = sub_id
    
    return together


def mean_bothrounds(diff1, diff2,recall):
    
    sel = [0,1,2]
    
    if not recall:
        sel = [3,4,5]
    
    #calculate average of both rounds of recall/recog
    mean_bothrounds = diff1.loc[:,sel].add(diff2.loc[:,sel])
    mean_bothrounds = mean_bothrounds.div(2)
    mean_bothrounds['sub_id'] = diff1['sub_id']
    
    return mean_bothrounds