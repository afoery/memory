#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 17:13:31 2020

@author: alisha
"""

import all_correct_spell_dic



def checkRecog(numWords, data, sess2 = False):
    
    ''' this function checks the recognition answers. futhermore it corrects
    the spelling of the recall
    '''
    corr_reco= '${e://Field/answer%d0}'
    
    if sess2:
        corr_reco = '${e://Field/2answer%d0}'
        
        
    #check which recognition answers are correct
    for i in range(numWords):
        data = data.replace({corr_reco%i : 'recogCorrect'})
        
    #repace 'nan' because we can't have float object for replace function later
    data.fillna('',inplace = True)
    
    #remove all whitespaces
    data = data.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    
    #replace misspelled answers from participants
    replaceDic = all_correct_spell_dic.corr_spell_dic()    
    data.replace(replaceDic, inplace = True)
    
    return data
   
    

def checkRecall(data,solutions,numWords, original):
    '''this function checks the recall answers. In case the answers are not
    correct it prints them. to check whether we need to correct for them. 
    '''
    
    for i in range(len(data)):
        for j in range(0,numWords):
            
            #make capital letters to compare answers to solution words
            data.loc[i,((j*2))] = data.loc[i,((j*2))].title()
            
            #check whether correct
            if data.loc[i,((j*2))] == solutions.loc[i][j]:
                data.loc[i,((j*2))] = 'recallCorrect'
            
            if (data.loc[i,((2*j))] != 'recallCorrect'):
                print(i,(j*2), original.loc[i,((2*j))], solutions.loc[i][j] )
    return data




def check_data(numWords,immediateAns, delayedAns, solutions, longterm = False,
               sess2 = False):
    """
    This function checks the answers of the participants and returns
    2 dataframes (immediate and delay responses) which include the strings
    "recallCorrect" and "recogCorrect" for answers that are correct
    """
    
    #check imm answers
    immAns = checkRecog(numWords, immediateAns, sess2 = sess2)
    immAns = checkRecall(immAns, solutions, numWords, immediateAns)
    
    #check delayed ans if applicable
    if not longterm:
	    delAns = checkRecog(numWords, delayedAns, sess2 = sess2)
	    delAns = checkRecall(delAns, solutions, numWords, delayedAns)
    else:
        delAns = 0
        
    return immAns, delAns
