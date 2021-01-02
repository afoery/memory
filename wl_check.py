#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 10:48:40 2020

@author: alisha
"""

import re
import numpy as np
import funcs
import pandas as pd

def checkWordList(wordlistSol, wordlistAns, amountCond, strict = True, 
                  count_similar_meaning = False):   
    '''
    this function outpusts a list which renders a list for each subject
    with the differences of the number of correctly recalled words
    
    these lists of differences has the order of how they had been presented
    to the participant
    
    output: list with the lengths of the amount of participant consisting
    of lists with the length of amountCond (=6)
    '''
    
    #replace nan in dataframe
    wordlistAns = wordlistAns.replace(np.nan, '', regex = True)    
    
    for i in range(len(wordlistAns)):
        for j in range(amountCond*2):
            
            #split so that each word is one string
            wordlistAns.loc[i,j] = re.sub("[^\w]", " ",  
                            wordlistAns.loc[i,j] ).split() 

            for k in range(len(wordlistAns.loc[i][j])):
                
                #make everything uppercase so that it matches solutions
                wordlistAns.loc[i,j][k] = wordlistAns.loc[i,
                                j][k].upper()
                
                #correct spelling if needed
                if wordlistAns.loc[i,j][k] == 'THOUGH':
                    wordlistAns.loc[i,j][k] = 'TOUGH'
                    
                if wordlistAns.loc[i,(j)][k] == 'BLYING':
                    wordlistAns.loc[i,(j)][k] = 'LYING'
             
                if wordlistAns.loc[i,(j)][k] == 'MOUND':
                    wordlistAns.loc[i,(j)][k] = 'BOUND'
               
                if wordlistAns.loc[i,(j)][k] == 'OCEANM':
                    wordlistAns.loc[i,(j)][k] = 'OCEAN'
    
            #in case we wanna count "almost" correct answers as true
            if not strict:
        
                replace_dic = {'MAJOR':'MAYOR', 'NAVY':'NAVAL','BAKE':'BAKER',
                               'CHOOSE':'CHOSE','BAKERY':'BAKER','DRINK':'DRUNK',
                               'GUILT':'GUILTY','PROCH':'PORCH','SHEARS':'SHEAR'}
                wordlistAns.loc[i,j] = [replace_dic.get(n,n) for n in wordlistAns.loc[i,j]]
                
            if count_similar_meaning:
                
                replace_dic1 = {'MESSAGE':'REPLY','ALARM':'ALERT','PRISON':'CRIME',
                                'JAIL':'CRIME','TRASH':'WASTE','CONFESS':'ADMIT',
                                'DRUGS':'JOINT','DRUG':'JOINT','BEACH':'OCEAN',
                                'BOAT':'OCEAN'}
                wordlistAns.loc[i,j] = [replace_dic1.get(n,n) for n in wordlistAns.loc[i,j]]
            
    
    #split sols into chunks how they had been presented to individual subjects
    diffAll = []
    for i in range(len(wordlistSol)):
        chunkedSols = list(funcs.chunks(wordlistSol.loc[i].to_list(),9))  
        
        diffpersubject = []
        
        #let's compare solutions to answers to see how many correctly recalled words
        for j in range(amountCond*2):
            
            #answer of subjects
            answer = wordlistAns.loc[i,(j)]
            
            if not (j%2): #even numbers = immediate free recall
                
                #solution
                solution = chunkedSols[int(j/2)]
                
                #matches and notmatches between answers and solution
                match = set(answer) & set(solution)     
                notmatches = list(set(answer).difference(solution)) 
                
                #number of correctly recalled words
                numRecalledImm = len(match)
                
            else: #delayed recall
                
                #solution
                solution = chunkedSols[int((j-1)/2)]
                
                #matches and notmatches between answers and solution
                match = set(answer) & set(solution)     
                notmatches = list(set(answer).difference(solution))    
                
                #number of correctly recalled words
                numRecallDel = len(match)
                
                #calculate difference between delayed and immediate
                diff = numRecallDel - numRecalledImm
                print('imm:', numRecalledImm, ', del:', numRecallDel,'---------------------')
                diffpersubject.append(diff)
               
            
            #check nomatches
            if  notmatches:
                print(i,j,'sol', solution)
                print('nomatch', notmatches)
        
        diffAll.append(diffpersubject)
        
                
    return  diffAll, wordlistAns


def orderEM(diffsEM, conditions):
    '''
    This function computes the difference between 
    [delayed - immediate recall] and outputs a list with the length of 
    numbr of participants
    
    diffsOrdered = [rest, video, game]
    '''
    
    diffsOrdered = [] #both rounds together
    diffs_1 = [] #first round
    diffs_2 = [] #second round
    
    for i in range(len(diffsEM)):
        closed = 0
        video = 0
        game = 0
        
        #initialize flags to determine whether we are in 1th or 2nd round
        flag_c = 0
        flag_v = 0
        flag_g = 0
        
        for j in range(6):
        
            if conditions.loc[i, (j)] == 'closed':
                
                #if closed is not empty (= second round)
                if flag_c:
                    closed_2 = diffsEM[i][j]
                 
                #first round
                else:
                    closed_1 = diffsEM[i][j]
                
                #both rounds together
                closed += diffsEM[i][j]
                flag_c = 1

            if conditions.loc[i, (j)] == 'video':
                
                if flag_v:
                    video_2 = diffsEM[i][j]
                    
                else:
                    video_1 = diffsEM[i][j]
                    
                video += diffsEM[i][j]
                flag_v = 1

            if conditions.loc[i, (j)] == 'game':
                
                if flag_g:
                    game_2 = diffsEM[i][j]
                
                else:
                    game_1 = diffsEM[i][j]
                    
                game += diffsEM[i][j]
                flag_g = 1
        
        diffsOrdered.append([closed,video, game])
        diffs_1.append([closed_1, video_1, game_1])
        diffs_2.append([closed_2, video_2, game_2])
    
    #put it into a dataframe
    diffsOrdered = pd.DataFrame(diffsOrdered)
    diffsOrdered.columns = ['rest','video','game']
    
    diffs_1 = pd.DataFrame(diffs_1)
    diffs_1.columns = ['rest','video','game']
    
    diffs_2 = pd.DataFrame(diffs_2)
    diffs_2.columns = ['rest','video','game']
    #plot
    ax = diffsOrdered.plot.bar(title = 'Wordlist Differences Immediate & Delayed (Del-Imm)')
    
    return  diffsOrdered, diffs_1, diffs_2