#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 11:02:11 2020

@author: alisha
"""
import random, math
random.seed(0)

import pandas as pd

numSub = 10
numWo = 54

ids = [random.randint(1000,2000) for x in range(numSub)]


gender = ['Male' for x in range(numSub)]
gender[math.ceil(numSub/2):numSub] = ['Female' for x in range(math.ceil(numSub/2),numSub)]

language= ['English' for x in range(numSub)]
language[math.ceil(numSub/2):numSub] = ['german' for x in range(math.ceil(numSub/2),numSub)]

feels = ['Positive' for x in range(numSub)]
age  = ['20' for x in range(numSub)]

#create headers
imm = ['i%d'%x for x in range(numWo*2)]
del_ans = [str(x) for x in range(numWo*2)]
sols = ['english%d'%x for x in range(numWo)]
conds = ['cond%d'%x for x in range(6)]
fb =  ['Q522', 'Q573', 'Q576', 'Q762','Q765', 'Q768']

feedback = pd.DataFrame(columns = fb)

#create data
#recall
sub = ['Nkjd' for x in range(numWo)]
imm_data = [sub for x in range(numSub)]
cols = [x for x in range(0,numWo*2,2)]
df_imm0 = pd.DataFrame(imm_data, columns = cols)


#sols
solutions = df_imm0.copy()
solutions.columns = sols




#recog
sub1 = ['${e://Field/answer%d0}'%x for x in range(numWo)]
imm_data1 = [sub1 for x in range(numSub)]
cols1 = [x for x in range(1,numWo*2,2)]
df_imm1 = pd.DataFrame(imm_data1, columns = cols1)



#concat recall and recog to one df
df_imm = pd.concat([df_imm0, df_imm1], axis = 1)
df_imm = df_imm[[x for x in range(numWo*2)]]
df_imm.columns = imm

df_del = df_imm.copy()
df_del.columns = del_ans


#change some values so that we get some false responses
df_imm.iloc[9,:] = ['false' for x in range(len(df_imm.columns))]

#conditions
sub2 = ['closed','video','game','closed','video','game']
conditions = [random.sample(sub2, len(sub2)) for x in range(numSub)]
conditions = pd.DataFrame(conditions, columns = conds)

dic = {'RandomID': ids, 'Q507': gender, 'Q467':language, 'Q972': feels, 
       'Q973':feels, 'Q974': feels, 'Q508': age}

df = pd.DataFrame(dic)





#put everything together
data = pd.concat([df, solutions, df_imm, df_del, conditions, feedback], axis = 1)

def add_row(df):
    df.loc[-1] = ['n' for x in range(len(df.columns))]  # adding a row
    df.index = df.index + 1  # shifting index
    df = df.sort_index()  # sorting by index
    return df

data = add_row(data)
data = add_row(data)

data.to_csv('control_data.csv')


'''muss noch conds hinzufügen'''







