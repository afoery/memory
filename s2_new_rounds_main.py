#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 22 15:22:23 2020

@author: alisha
"""
import all_import_data, rr_check_data, rr_count

def new_learning_s2(df2, sess2, numRo2, worperro):
    
    #get results of new learning rounds in sess2
    #extract relevant data
    ids2, ans_imm2, ans_del2, sols2, conds2, feels2 = all_import_data.import_basicdataS2(
                df2, sess2.numWords)
        
    #check data
    ans_imm2, ans_del2 = rr_check_data.check_data(sess2.numWords,ans_imm2, ans_del2, 
                                                sols2, sess2 = True)
    
    #calculate how many correct answers per condition  
    imm3, _ = rr_count.splitndcount(ans_imm2, conds2, numRo2, ids2,  worperro)
    
    del3, _ = rr_count.splitndcount(ans_del2, conds2, numRo2, ids2, worperro)
    
    return imm3, del3