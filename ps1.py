"""Problem Set 1 Part 2 : Annie Pi"""

import numpy as np
import statsmodels.api as sm

def dickey_fuller_montecarlo(num_iterations=10000,    
                             T=75,                   
                             deletions=150,     #deleting these ones only keeping last 75       
                             mu=0.25,                # drift 
                             seed=42):               

    np.random.seed(seed)
    deltas = []

    for _ in range(num_iterations):
        epsilons = np.random.randn(T + deletions)
        y_full = np.zeros(T + deletions)  # Allocationg space
        for t in range(1, T + deletions):
            y_full[t] = mu + y_full[t - 1] + epsilons[t]
        y = y_full[deletions:]  

        # create first difference vector
        delta_y = np.diff(y)  
        # lagged y vector, now we have the 2 vectors both of size 74
        y_lagged = y[:-1]  # length is T-1
        X = sm.add_constant(y_lagged) 
        model = sm.OLS(delta_y, X)
        results = model.fit()
        delta_est = results.params[1]  # 1 because 0 is the constant
        deltas.append(delta_est)
    # converting 
    deltas = np.array(deltas)
    critical_val = np.percentile(deltas, 5)
    mean_delta = np.mean(deltas)

    return critical_val, mean_delta

if __name__ == "__main__":
    critical_5pct, mean_delta = dickey_fuller_montecarlo(
        num_iterations=10000,
        T=75,
        burn_in=150,
        mu=0.25,
        seed=42
    )
    print("The estimated 5% CV of delta is ", critical_5pct)
    print("The mean of the delta distribution is", mean_delta)
