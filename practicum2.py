"""Jan 24, 2025"""
import numpy as np
import statsmodels.api as sm

test = np.log(2)
x = [[0.0, 1., 2., 3., 4.], [1,2,3,4,5]]
y = np.array(x) #this is a lists of lists

base2 = np.zeros(4) # you get a vector of 1 dimension of all 0
#base2 = np.zeros((1,4)) would give you 2 dimensions
base = np.ones((4,4)) #makes a new vector/array of tuples of all 1. in a 4 by 4 matrix (2 dimensions) row first then columns syntaxtically
#you can add arrays if they have the same dimension
print("number of dimensions in Y are " + str(y.ndim))

y_new = np.concatenate((y, base2), axis =1) #axis = 0 is by row, axis 1 is by columns
#y_new2 = y+base
print(y[:,1:]) # idk what this does 

randomtest = np.random.normal(3,2,(10,1))
randomtest2 = np.random.normal(0,1,(10,1))

randomfull = np.concatenate((randomtest, randomtest2), axis=1)

g = randomfull.mean()
gprime = randomfull.mean(axis=0)




