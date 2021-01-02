#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 13 10:52:17 2020

@author: alisha
"""
import matplotlib.pyplot as plt
import math
import matplotlib.patches as mpatches
from matplotlib import rcParams
import numpy as np

    # customized settings
params = {  # 'backend': 'ps',
    'font.family': 'serif',
    'font.serif': 'Latin Modern Roman',
    'font.size': 19,
    'axes.labelsize': 'small',
    'axes.titlesize': 'small',
    'legend.fontsize': 'small',
    'xtick.labelsize': 'medium',
    'ytick.labelsize': 'medium',
    'savefig.dpi': 300,
    'text.usetex': True}
# tell matplotlib about your params
rcParams.update(params)

# set nice figure sizes
fig_width_pt = 300    # Get this from LaTeX using \showthe\columnwidth
golden_mean = (np.sqrt(5.) - 1.) / 2.  # Aesthetic ratio
ratio = golden_mean
inches_per_pt = 1. / 72.27  # Convert pt to inches
fig_width = fig_width_pt * inches_per_pt  # width in inches
fig_height = fig_width * ratio  # height in inches
fig_size = [fig_width, fig_height]
rcParams.update({'figure.figsize': fig_size})

#colors
r = [250/255, 103/255, 80/255]
lb = [167/255, 198/255, 250/255]
b = [14/255, 72/255, 173/255]

colors = [r,lb,b]
 
def plot_mean_diff_per_sub(df_mean, df_std, recall = True):
    
 
    
    include = [0,1,2]
    
    if not recall:
        include = [3,4,5]
    
    ax = df_mean.loc[:, include].plot.bar(
            title = 'Mean Differences Per Subject (Session 1)',
            yerr = df_std.iloc[:,[0,1,2]].values.T, capsize = 8, 
            color = [r,lb,b])
    
    ax.set_xlabel('Subjects')
    ax.set_ylabel('Mean differences [delayed - immediate scores]')


def plot_performance(immediate, delayed, std_imm, std_del, control, title, recall = True):


    
    amountSub = len(immediate)
    
        
    cols = int(math.ceil(amountSub/2))
    rows = int(math.ceil(amountSub/cols))

    #calculate how many subplots we need to delete
    num_plots = cols*rows
    diff = num_plots - amountSub
        
    
    #determine at which columns programm needs to look at
    if recall:
        rangee = [0,1,2]
    else:
        rangee = [3,4,5]
        
            
    fig, axs = plt.subplots(rows, cols, sharex = True, sharey = True)

    #delete unnecessary subplots
    num = 0
    for i in range(diff):
        col = cols - num
        
        fig.delaxes(axs[rows-1, col-1])
        num += 1
        
    axs = axs.ravel()
        
    x = [1,2]
    
    for i in range(amountSub):
        

        rest_y = [immediate.loc[i, rangee[0]], delayed.loc[i, rangee[0]]]

        video_y = [immediate.loc[i, rangee[1]], delayed.loc[i, rangee[1]]]

        game_y = [immediate.loc[i, rangee[2]], delayed.loc[i, rangee[2]]]
        
        #standard deviation
        rest_std = [std_imm.loc[i, rangee[0]], std_del.loc[i, rangee[0]]]

        video_std = [std_imm.loc[i, rangee[1]], std_del.loc[i, rangee[1]]]

        game_std = [std_imm.loc[i, rangee[2]], std_del.loc[i, rangee[2]]]
        
        #plot data
        cp = 5
        axs[i].errorbar(x,rest_y,yerr = rest_std,capsize=cp, fmt = '-', 
           marker = 'o',color= r,label = 'Rest')
        
        axs[i].errorbar(x,video_y,yerr = video_std,capsize=cp, fmt = '--',
           marker = 'x',color = lb, label = 'Video')
        
        axs[i].errorbar(x,game_y, yerr = game_std,capsize=cp, fmt = '-.',
           marker = '.',color = b,label = 'Game')
        
        axs[i].set_xticks([1,2])
        axs[i].set_xticklabels(['0', '8'])
        
        axs[i].set_yticks([0,2,4,6,8,10])
        
        
    plt.legend(bbox_to_anchor=(1.2, 1.05), frameon = False)  
    
    # add a big axis, hide frame
    fig.add_subplot(111, frameon=False)
    # hide tick and tick label of the big axis
    plt.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)
    plt.xlabel("Time after Encoding [min]")
    plt.ylabel("Memory Performance (max = 9)")
    

#    fig.suptitle(title + F' (n = {amountSub})')
    plt.show()
    
    
    
def pdf(diffs_mean, num, cond, ax):
    x = diffs_mean.loc[:,num]
    num_bins = 50
    mu = diffs_mean.loc[:,num].mean()
    print('mu',mu)
    # the histogram of the data
    n, bins, patches = ax[num].hist(x, num_bins, density=1)
    # add a 'best mean' line
    ax[num].axvline(mu,color='r')

    ax[num].set_title(F'Histogram - {cond}')
    
    #manually add legend
    red_patch = mpatches.Patch(color='red', label='Mean')
    plt.legend(handles=[red_patch])   
    
    
def plot_pdf(diffs_mean):
    
    #plot probability density functions of recall/recog performance
    fig, ax = plt.subplots(3,1, sharex = True, sharey = True)
    
    # add a big axis, hide frame (for common x and y label)
    fig.add_subplot(111, frameon=False)
    # hide tick and tick label of the big axis
    plt.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)
    plt.xlabel("Mean Difference")
    plt.ylabel("Probability density")
    
    pdf(diffs_mean, 0,'rest', ax)
    pdf(diffs_mean, 1, 'video', ax)
    pdf(diffs_mean, 2, 'game', ax)


    
    
def plot_means_sep(group_mean, group_std):
    
        # customized settings
    params = {  # 'backend': 'ps',
        'font.family': 'serif',
        'font.serif': 'Latin Modern Roman',
        'font.size': 10,
        'axes.labelsize': 'small',
        'axes.titlesize': 'small',
        'legend.fontsize': 'small',
        'xtick.labelsize': 'medium',
        'ytick.labelsize': 'medium',
        'savefig.dpi': 300,
        'text.usetex': True}
    # tell matplotlib about your params
    rcParams.update(params)
    
    # set nice figure sizes
    fig_width_pt = 300    # Get this from LaTeX using \showthe\columnwidth
    golden_mean = (np.sqrt(5.) - 1.) / 2.  # Aesthetic ratio
    ratio = golden_mean
    inches_per_pt = 1. / 72.27  # Convert pt to inches
    fig_width = fig_width_pt * inches_per_pt  # width in inches
    fig_height = fig_width * ratio  # height in inches
    fig_size = [fig_width, fig_height]
    rcParams.update({'figure.figsize': fig_size})

    fig, ax = plt.subplots()
    
    group_mean.iloc[:,[x for x in range(6)]].plot.bar(
            color = colors,
            yerr = group_std, capsize = 5, ax = ax, legend = False)
#    ax.legend(['Rest','Video','Game'], loc = (0.8,0.51), frameon= False)
    
    #hide parts of the box
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)   
    
    #set ylim
    ax.set_ylim(-3,3)
    ax.set_xlim(-0.3,0.3)
    
    # label recall/ recog with bracket
    x = 0.28
    y = 0.9
    ax.annotate('Recall', xy=(x, y), xytext=(x, y+0.1), xycoords='axes fraction', 
                fontsize=11, ha='center', va='bottom',
                arrowprops=dict(arrowstyle='-[, widthB=3.8, lengthB=1', lw=0.8))
    x2 = x +0.44
    ax.annotate('Recognition', xy=(x2, y), xytext=(x2, y+0.1), xycoords='axes fraction', 
                fontsize=11, ha='center', va='bottom',
                arrowprops=dict(arrowstyle='-[, widthB=3.8, lengthB=1', lw=0.8))
    
    ax.set_xticks([])
    fig.tight_layout()
    
    ax.set_ylabel('Mean Memory Difference Scores')
    
    
    
    
    
    