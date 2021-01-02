#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 09:44:21 2020

@author: alisha
"""
import math
import matplotlib.pyplot as plt

#colors
r = [250/255, 103/255, 80/255]
lb = [167/255, 198/255, 250/255]
b = [14/255, 72/255, 173/255]

def plot_overtime(imm, del8, lt, std_imm, std_del, std_lt, recall):
    
    numSubs = len(imm)
    
    #calculate how many rows and cols we need 
    cols = int(math.ceil(numSubs/2))
    rows = 2
    
    #calculate how many subplots need to be dropped
    num_plots = cols*rows
    del_plots = num_plots - numSubs
    
    sel = [0,1,2] #recall
    title = 'Recall over time'
    
    #recognition
    if not recall:
        sel = [3,4,5]
        title = 'Recognition over time'
        
    #new figure
    fig, axs = plt.subplots(rows, cols, sharex = True, sharey = True)
    
    #delete unnecessary subplots
    num = 0
    for i in range(del_plots):
        col = cols - num
        
        fig.delaxes(axs[rows-1, col-1])
        num += 1
    
    axs = axs.ravel()
    
    #x axis
    x = [1,2,3]
    
    for i in range(numSubs):
        #define y-values
        y_r = [imm.loc[i,sel[0]], del8.loc[i,sel[0]], lt.loc[i,sel[0]]]
        y_v = [imm.loc[i,sel[1]], del8.loc[i,sel[1]], lt.loc[i,sel[1]]]
        y_g = [imm.loc[i,sel[2]], del8.loc[i,sel[2]], lt.loc[i,sel[2]]]

        #define std
        std_r = [std_imm.loc[i,sel[0]], std_del.loc[i,sel[0]], std_lt.loc[i,sel[0]]]
        std_v = [std_imm.loc[i,sel[1]], std_del.loc[i,sel[1]], std_lt.loc[i,sel[1]]]
        std_g = [std_imm.loc[i,sel[2]], std_del.loc[i,sel[2]], std_lt.loc[i,sel[2]]]
        
    
        #plot data
        cp = 5
        axs[i].errorbar(x,y_r, yerr = std_r, capsize = cp, fmt = '--', color= r,label = 'rest')
        axs[i].errorbar(x,y_v, yerr = std_v, capsize = cp, fmt =  '-', color = lb, label = 'video')
        axs[i].errorbar(x,y_g, yerr = std_g, capsize = cp, fmt = '-.', color = b,label = 'game')
        
        axs[i].set_xticks([1,2,3])
        axs[i].set_xticklabels(['0', '8 min', '7 days'])
        axs[i].set_title(i+1)
        
    plt.legend()
#    fig.text(0.5,0.04,'Time after encoding', ha = 'center')
#    fig.text(0.04, 0.5,'Memory performance (max = 9)', va='center', rotation='vertical')
    fig.suptitle(title)
    plt.show()
    
    
    
def plot_mean_overtime(means, std,recall):
    
    sel = [0,1,2] #recall
    title = 'Mean recall over time'
    
    #recognition
    if not recall:
        sel = [3,4,5]
        title = 'Mean recognition over time'
        
    #x axis
    x = [1,2,3]
    
    #define y-values
    y_r = [means.loc['imm',sel[0]], means.loc['del',sel[0]], means.loc['lt',sel[0]]]
    y_v = [means.loc['imm',sel[1]], means.loc['del',sel[1]], means.loc['lt',sel[1]]]
    y_g = [means.loc['imm',sel[2]], means.loc['del',sel[2]], means.loc['lt',sel[2]]]
    
    #define std
    std_r = [std.loc['imm',sel[0]], std.loc['del',sel[0]], std.loc['lt',sel[0]]]
    std_v = [std.loc['imm',sel[1]], std.loc['del',sel[1]], std.loc['lt',sel[1]]]
    std_g = [std.loc['imm',sel[2]], std.loc['del',sel[2]], std.loc['lt',sel[2]]]
    
    
    #new figure
    fig, axs = plt.subplots(sharex = True, sharey = True)

    #plot data
    cp = 5
    axs.errorbar(x,y_r, yerr = std_r, capsize = cp, fmt = '--', color= r,label = 'rest')
    axs.errorbar(x,y_v, yerr = std_v, capsize = cp, fmt =  '-', color = lb, label = 'video')
    axs.errorbar(x,y_g, yerr = std_g, capsize = cp, fmt = '-.', color = b,label = 'game')
    
    axs.set_xticks([1,2,3])
    axs.set_xticklabels(['0', '8 min', '7 days'])
        
    plt.legend()
#    fig.text(0.5,0.04,'Time after encoding', ha = 'center')
#    fig.text(0.04, 0.5,'Memory performance (max = 9)', va='center', rotation='vertical')
    fig.suptitle(title)
    plt.show()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    