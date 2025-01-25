"""Annie Pi 730502223 Practicum 2 for Econ 493"""
import numpy as np
# 1
poisson_sample = np.random.poisson(lam=10, size=1000)

poisson_mean = np.mean(poisson_sample)
print(f"The mean of the Poisson sample = {poisson_mean:.4f}")

# 2
chisq_sample = np.random.chisquare(df=35, size=(1000, 2))

# std dev of each column
std_col1 = np.std(chisq_sample[:, 0])
std_col2 = np.std(chisq_sample[:, 1])
print(f"Chi-square, standard dev of col 1 = {std_col1:.4f}")
print(f"Chi-square, standard dev of col 2 = {std_col2:.4f}")

# 3 , making new array
Y = 10 * poisson_sample + chisq_sample[:, 0]

# std dev and mean
Y_mean = np.mean(Y)
Y_std = np.std(Y)
print(f"The mean of Y = {Y_mean:.4f}")
print(f"The standard dev of Y = {Y_std:.4f}")
