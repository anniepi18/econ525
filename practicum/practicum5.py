"""Jan 31 2025"""

import numpy as np
import statsmodels.api as sm 
import matplotlib.pyplot as plt 

#initializing some stuff
sample = 50
burnin=150
iteration = 10000
alpha = 2
theta = 3
rho = 0.5
beta0=1

#plt.hist(betas,bins=50,density = True) to make a histogram 