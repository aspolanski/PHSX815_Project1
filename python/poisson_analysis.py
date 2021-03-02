#!/usr/bin/env python3

import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.special import factorial
from scipy.stats import ks_2samp
from signal_noise_generator import generator
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,AutoMinorLocator)
import os
from datetime import datetime, timezone
from tqdm import tqdm


#get date/time for figure names
date =  str(datetime.now().astimezone())[0:19].replace(' ','_')



if __name__ == "__main__":

    if '-sky' in sys.argv:
        p = sys.argv.index('-sky')
        sky = int(sys.argv[p+1])
    if '-read' in sys.argv:
        p = sys.argv.index('-read')
        read = int(sys.argv[p+1])
    if '-Nexp' in sys.argv:
        p = sys.argv.index('-Nexp')
        num_exp = int(sys.argv[p+1])


    sig = np.arange(5, (sky+9))
        

    # Initialize lists for the p-vals from the KS test and signal/noise samples

    ks_scores = []

    signals = []

    noises = []
    
    print("Calculating p-values...\n")

    for n in tqdm(range(1000)):
        #initiate a list for a trial of KS tests with varying signal rates
        ks_sub = []
        sigs_sub = []
        noises_sub =[]


        for i in sig:
            signal, noise = generator(num_exp,sky,read,i)
            
            sigs_sub.append(signal[0])
            noises_sub.append(noise[0])
            ks_sub.append(ks_2samp(signal[0],noise[0])[1])

        #append the trial to the full KS results list
        ks_scores.append(ks_sub)
        signals.append(sigs_sub)
        noises.append(noises_sub)

    ks_scores = np.array(ks_scores)

    print("\nDone!\n")

    # Store the signals/noises/p-values in CSV files

    # Create a relevant data directory
    dir_name = f"../results_Nexp{num_exp}_Sky{sky}_{date}"

    os.mkdir(dir_name)

    np.savetxt(f"{dir_name}/p-vals.csv",np.array(ks_scores),delimiter=',')

    # Note that #D arrays cannot be saved to text, so we lose one dimension, namely signals/noises generated for each signal rate step are merged. 

    print(np.shape(np.array(signals).reshape(np.array(signals).shape[0],-1)))


    np.savetxt(f"{dir_name}/signals.csv",np.array(signals).reshape(np.array(signals).shape[0],-1),delimiter=',')
    np.savetxt(f"{dir_name}/noises.csv",np.array(noises).reshape(np.array(noises).shape[0],-1),delimiter=',')

    
    #PLot results    

    fig, ax1 = plt.subplots(figsize=(10,5))
    minor_locator = AutoMinorLocator(5) 
    ax1.set_xticks(sig)    
    ax1.set_xlim(sig[0]-1,sig[-1])
    ax1.errorbar(sig,np.mean(ks_scores,axis=0), yerr=3*np.std(ks_scores,axis=0),ls='none',marker='o')
    ax1.hlines(0.05,xmin=-1,xmax=ax1.get_xlim()[1],linestyles='dashed',colors='black')
    ax1.set_ylabel("p-value",fontsize=22)
    ax1.set_xlabel("$\lambda_{sig}$", fontsize=22)
    ax1.yaxis.set_minor_locator(minor_locator)
    ax1.tick_params(axis='both', which='both', direction = 'in',labelsize=20)
    ax1.tick_params(axis='both', which='major', direction = 'in',labelsize=20,length=7,width=2)
    ax1.tick_params(axis='both', which='minor', direction = 'in',labelsize=20,length=4,width=2) 
    ax1.text(0.65,0.75, '$N_{exp}$='+f'{num_exp}', transform=ax1.transAxes, fontsize=29)
    ax1.text(sig[-1]-3,0.08,"p-value 0.05", fontsize=18)
    
    fig_name = f"result.pdf" 

    fig.savefig(f"{dir_name}/{fig_name}",format='pdf')

    

