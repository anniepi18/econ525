"""Jan 31 2025"""
import numpy as np 
import statsmodels as sm
x=6.4
y=3.2
"""
if(x<=6.4) & (y==0.5*x):
    print("Good morning")
else:
    print("Go UNC!")

print("Econ 493 is so much fun")
"""
z= range(0,5)
epsilon = np.random.normal(0,1,(100,1))
x = np.random.normal(5,4,(100,1))
y=3+10*x +epsilon

xregress = sm.add_constant(x)
mod = sm.OLS(y, xregress)
results = mod.fit()
#results.resids to get residuals
print("WAKE UP!!!")