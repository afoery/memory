#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 25 13:58:44 2020

@author: alisha
"""
import matplotlib.pyplot as plt
import statsmodels.api as sm
import numpy as np
from matplotlib import rcParams
import scipy.stats as stats
import pylab
import seaborn as sns



# customized settings
params = {  # 'backend': 'ps',
    'font.family': 'serif',
    'font.serif': 'Latin Modern Roman',
    'font.size': 15,
    'axes.labelsize': 'small',
    'axes.titlesize': 'small',
    'legend.fontsize': 'medium',
    'xtick.labelsize': 'small',
    'ytick.labelsize': 'small',
    'savefig.dpi': 150,
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

def qq_plot(diffs_mean, recall, rt = False):
    
    sns.set_style('white')
    
    t = 'recall'
    t1 = ''
    
    if not recall:
        t = 'recog'
        
    if rt:
        t1 = '_rt'
    t = t+t1
          
    fig2, axs = plt.subplots(1,3, sharex = False)
    fig2.add_subplot(111, frameon = False)
    
    plt.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)
    plt.xlabel("Theoretical Quantiles")
    plt.ylabel("Sample Quantiles")
    
    title = ['Rest', 'Video', 'Game']
    axs = axs.ravel()
    
    for i in range(3):
        
        sm.qqplot(np.array(diffs_mean.iloc[:,i]), line='s', ax = axs[i])
        
        axs[i].get_lines()[0].set_markersize(5)
        axs[i].get_lines()[0].set_markeredgewidth(0.3)
        axs[i].get_lines()[0].set_markerfacecolor(colors[i])
        axs[i].get_lines()[0].set_markeredgecolor('gray')
        axs[i].get_lines()[1].set_color('gray')
        
        axs[i].set_xlabel('')
        axs[i].set_ylabel('')
        
        
        
        axs[i].set_title(title[i])
        
        axs[i].set_xlim(-2,2)

    
    plt.tight_layout()    
    plt.savefig(F'qq-plot{t}',dpi = 300)
    
    
def pdf(diffs_mean, recall, rt = False):
    
    t = 'recall'
    t1 = ''
    
    if not recall:
        t = 'recog'
        
    if rt:
        t1 = '_rt'
    
    t = t+t1
          
    fig2, axs = plt.subplots(1,3)
    fig2.add_subplot(111, frameon = False)
    
    plt.tick_params(labelcolor='none', top=False, bottom=False, left=False, 
                    right=False)
    plt.xlabel("Difference Memory Scores")
    plt.ylabel("Probability Density")
    
    title = ['Rest', 'Video', 'Game']
    axs = axs.ravel()
    
    for i in range(3):
        
        n, bins, patches = axs[i].hist(np.array(diffs_mean.iloc[:,i]), 40, 
                              color = colors[i], density=1)
        

        
        axs[i].set_xlabel('')
        axs[i].set_ylabel('')
        
        axs[i].set_title(title[i])
    
    plt.tight_layout()    
    plt.savefig(F'pdf_{t}',dpi = 300)
  
    
    
def shapiro(data):
    
    '''
    >plot qq plot and pdf
    > shapiro wilk test for normality
    '''
    
    #qq plot
    sm.qqplot(np.array(data), line='45')
    pylab.show()
    
    #pdf
    fig, ax = plt.subplots()
    n, bins, patches = ax.hist(data, 40, density=1)
    
    #shapiro wilk test
    print('shapiro test', stats.shapiro(data))
    
    
    
    
    
    
    
    
    
    
    