#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 09:39:37 2020

@author: alisha
"""
import pandas as pd
import funcs

def import_df(path, control, sess2 = False, onlyFem = False, onlyMen = False,
              pos_rest = False, onlyEnglish = False, onlyForeign = False,
              only_gamers = False):
    '''this function imports the csv file of session 1 and drops selected 
    subjects and control if wanted
    '''
    
    #import csv file 
    df = pd.read_csv(path, index_col = None, header = 0)
    
    #drop certain subjects
    df = df[df.RandomID != '87965'] #technical errors
    df = df[df.RandomID != '29385'] #technical errors (ce)
    
#    df = df[df.RandomID != '62753'] #unusual reaction times - recog
    
    
    
    df = df[df.Q505 != 'No'] #did subjects do their best?
    
    #delete control subjects if we want
    if not control: 
        df = df[df.RandomID != '31734']
        df = df[df.RandomID != '11418']
        
    #in case we only wanna look at one gender
    if onlyFem:
        df = df[df.Q507 != 'Male']
    if onlyMen:
        df = df[df.Q507 != 'Female']
    
    #in case we wanna exclude those who did not like rest
    if pos_rest:
        df = df[df.Q974 != 'Negative']
     
    english = ['English', 'english']
    if onlyEnglish:
        df = df[df['Q467'].isin(english)]
    
    if onlyForeign:
        df = df[~df['Q467'].isin(english)]
        
    if only_gamers:
        df = df[df.Q975 != 'No']
        
        
    #delete first two columns as we don't need them
    df = funcs.deleteFirstTwoColumns(df)
    
    return df
    
def import_df2(path, control):
    
    '''import data for session 2'''
    
    #import csv file 
    df = pd.read_csv(path, index_col = None, header = 0)

    #delete control subjects if we want
    if not control: 
        df = df[df.Q827 != '31734']
        df = df[df.Q827 != '11418']
 
    df = df[df.Q827 != '51884'] #technical issues at the end... lt performance is ok
    
    #delete first two columns as we don't need them
    df = funcs.deleteFirstTwoColumns(df)

    
    return df


def relevant_data(df, columns , length, create_cols = True):
    '''
    this function extract the important columns of the qualtrics csv file.
    function is used below in 'import_data'
    '''
    if create_cols:
        columns = [columns+ str(i) for i in range(length)]
      
    extracted = df[columns]
    
    #rename columns
    if isinstance(extracted, pd.DataFrame):
        extracted.columns = [x for x in range(extracted.shape[1])]

    return extracted



def import_basicdata(df, numWords):

    '''create individual dfs for basic variables
    '''    	
    
    #extract subjcts IDs, answers, solutions
    ids = relevant_data(df, 'RandomID', 0, create_cols = False)
    ids = pd.to_numeric(ids, errors='coerce')
    
    #create individual dfs for each desired variable
    ans_imm = relevant_data(df, 'i' , numWords*2)    
    
    ans_del = relevant_data(df, '' , numWords*2)
    
    sols = relevant_data(df, 'english' , numWords)
    sols['sub_id'] = ids
    
    conds = relevant_data(df, 'cond' , 6)
    #no need to know exact game/video
    replace = {'swingTriangle' : 'game', 
               'yeti': 'game',
               'videoYeti': 'video',
               'videoTriangle': 'video'}
    conds.replace(replace, inplace = True)
    
    #how subjects were feeling during the different conds
    infos = pd.DataFrame({'rest': df.loc[:,'Q974']})
    infos['video']= df.loc[:,'Q972']
    infos['game'] = df.loc[:,'Q973']
    
    #infos
    infos['gender'] = df.loc[:,'Q507']
    infos['nativeLang'] = df.loc[:,'Q467']
    infos['sub_id'] = df.loc[:,'RandomID']
    infos['age'] = df.loc[:,'Q508']
    infos = infos.sort_values('sub_id')
    infos.index = [x for x in range(len(infos))]
        
    #what did they do during conds
    cols = ['Q522', 'Q573', 'Q576', 'Q762','Q765', 'Q768']
    feedback = relevant_data(df, cols, 0, create_cols = False)
    feedback.loc[:,'sub_id'] = ids.loc[:]
    
    return ids, ans_imm,ans_del, sols, conds, infos, feedback

def import_basicdataS2(df, numWords):
    '''create individual dfs for basic variables of session2
    '''    	    
    
    #extract subjcts IDs, answers, solutions
    ids = relevant_data(df, 'Q827', 0, create_cols = False)
    ids = pd.to_numeric(ids, errors='coerce')
    
    #create individual dfs for each desired variable
    ans_imm = relevant_data(df, 'imm' , numWords*2)    
    
    ans_del = relevant_data(df, '' , numWords*2)
    
    sols = relevant_data(df, '2english' , numWords)
    
    conds = relevant_data(df, 'cond' , 6)
    #no need to know exact game/video
    replace = {'soccer' : 'game', 
               'videoSoccer': 'video'}
    conds.replace(replace, inplace = True)
    
    #how subjects were feeling during the different conds
    feels = pd.DataFrame({'rest': df.loc[:,'Q1184']})
    feels['video']= df.loc[:,'Q1182']
    feels['game'] = df.loc[:,'Q1183']

    
    return ids, ans_imm,ans_del, sols, conds, feels


def import_wl(df, amountCond):
    '''create dfs for wordlist data
    '''
    wl = relevant_data(df, 'e', amountCond*2)
    wl_sols = relevant_data(df, 'word', amountCond*9)
    
    return wl, wl_sols

    
    
    
    
    
def import_lt_data(df, numWords):
    '''create individual dfs for basic variables
    '''
    
    #extract subjcts IDs, answers, solutions
    ids = relevant_data(df, 'Q827', 0, create_cols = False)
    ids = pd.to_numeric(ids, errors='coerce')
    
    #create individual dfs for each desired variable
    lt_ans = relevant_data(df, 'i' , numWords*2)    
    
    
    sols = relevant_data(df, 'english' , numWords)
    
    
    return ids, lt_ans, sols
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
