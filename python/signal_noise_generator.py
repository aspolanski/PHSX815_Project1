#!/usr/bin/env python3

import numpy as np
import sys
import pandas as pd
from Random import Random
    
def generator(num_exp,sky,read,sig):
    
    #############################################
    # Generator of Signal and Noise Distributions
    # Parameters:
    # num_exp = Number of exposures taken 
    # sky = photon rate of the sky-background
    # read = photon rate of the read noise
    # sig = photon rate of the signal
    #############################################

    num_meas = 1    
    
    # Calculate the total noise and signal rates

    tot_rate = sky + sig + read*num_exp
    tot_noise_rate = sky + read*num_exp 

    
    noise_array = []

    signal_array = []

    #Initialize random class

    R=Random()

    #Get the samples for the different distributions

    noise = R.Poisson(lam=tot_noise_rate,size=(num_meas,num_exp))

    signal = R.Poisson(lam=tot_rate,size=(num_meas,num_exp))
    
    return(signal,noise)

