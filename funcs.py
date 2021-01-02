#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 12 15:47:43 2020


just some functions

@author: alisha
"""
import pandas as pd
import os

#check which words have been auto corrected
def returnNotMatches(a, b):
    return [[x for x in a if x not in b], [x for x in b if x not in a]]



def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]
        
        
        
def correctRecall(answers, solutions, numWords, session):
    if session ==1:
        e = 'english'
    if session == 2:
        e = '2english'
    
    for i in range(len(answers)):
        for j in range(numWords):
            answers[i][2*j] = answers[i][2*j].title() #capital letters
            
            #check which words are correct
            
            if answers[i][2*j] == solutions.loc[i][F'{e}%d'%j]:
                answers[i][2*j] = 'recallCorrect'
    
    return answers


def autolabel(rects,ax):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = round(rect.get_height())
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')
        

def find_matching_index(list1, list2):

    inverse_index = { element: index for index, element in enumerate(list1) }

    return [(index, inverse_index[element])
        for index, element in enumerate(list2) if element in inverse_index]
    

def deleteFirstTwoColumns (df):
    
    try:
        df = df.drop(0)
        df = df.drop(1)
    except KeyError:
        pass
    
    df.index = range(len(df))
    return df



def relevant_data(df, columns , length, create_cols = True):
    '''
    this function extract the important columns of the qualtrics csv file
    '''
    if create_cols:
        columns = [columns+ str(i) for i in range(length)]
        
    extracted = df[columns]
    
    #rename columns
    if isinstance(extracted, pd.DataFrame):
        extracted.columns = [x for x in range(extracted.shape[1])]

    return extracted


def get_data_in_parentDic(data):
    
    #get path to data file
    path = os.getcwd()
    path_parent = os.path.abspath(os.path.join(path, os.pardir))
    path_data = path_parent + F'/{data}.csv'
    
    return path_data


#get basic variables
class session:
    
    wordsperround = 9
    
    def __init__(self, rounds, file):
        self.numWords = rounds* session.wordsperround
        self.datapath = get_data_in_parentDic(file)

