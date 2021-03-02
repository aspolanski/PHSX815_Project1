## PHSX815_Project1: Signal and Noise in CCD Astronomy

This package compares photon rates sampled from Poisson distributions representing noise (sky-background and read noise) and signal. It attempts to find the lowest signal rate one can make reliably detect given some read noise and sky-background photon rates.

# Descriptions of Included Scripts:

* *signal_noise_generator.py*: This script contains the function "generator" which takes as input the number of exposures (num_exp), sky photon rate (rate),. read noise rate (read), and the signal photon rate (sig).
It calls the Poisson instance of the *Random* class to generate two arrays of size (1,num_exp) representing the signal and noise samples.

* *poisson_analysis.py* This script is the only one that takes user input. It takes as input the number of exposures (-Nexp), sky photon rate (-sky), read noise rate (-read). The script then calls *signal_noise_generator.py* and calculates p-vals for each pair signal/noise sample pairs. The result is creation of a directory specific to the run that contains text files of the p-values, signals, and noises along with a PDF that plots p-values as a function of signal rate. 

* *Random.py* Random class which generates random samples; includes Poisson instance used in this package.
# Usage:

```python
python poisson_analysis -Nexp 10 -read 1 -sky 5
```

# Dependencies 

This code requires:

* Python 3.7.3
* Scipy v1.6.0
* Numpy v1.19.2
* MatplotLib v3.3.2
* TQDM v4.56.0

