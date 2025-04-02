"""Annie Pi 730502223 ECON 525: Problem Set 2"""
import pandas as pd
import numpy as np 
import statsmodels.api as sm 
#importing stuff

def fama_mcbeth_regression(file):
    df = pd.read_excel(file)
    df['Date'] = pd.to_datetime(df['Date'])
    portfolio_cols = df.columns[1:26]
    betas = []
    avg_excess_returns = []
    for col in portfolio_cols: #time series regression for each portfolio 
        excess_return = df[col] - df['RF']
        X = df[['Mkt-RF', 'CPIAUCSL_PCH', 'PCE_PCH']]
        X = sm.add_constant(X) #i think you need to do this? 
        model = sm.OLS(excess_return, X).fit()
        betas.append([model.params['Mkt-RF'], model.params['CPIAUCSL_PCH'], model.params['PCE_PCH']])
        avg_excess_returns.append(excess_return.mean())
        #we're finding the estimated betas and the avg excess returns for each port
        #the dependent var is the excess return 
        #independent vars are the market risk premium ,inflation, and consumption 
    betas_df = pd.DataFrame(betas, columns=['beta_mkt','beta_inf','beta_pce'], index=portfolio_cols)
    avg_returns_df = pd.DataFrame(avg_excess_returns, columns=['avg_excess_return'], index=portfolio_cols)
    stage2_data = betas_df.join(avg_returns_df)
    X_stage2 = stage2_data[['beta_mkt','beta_inf','beta_pce']]
    X_stage2 = sm.add_constant(X_stage2)
    y_stage2 = stage2_data['avg_excess_return']
    #cross-sectional reg on the 25 portfolios
    #dependent var is the average excess return for each
    #independent vars are the corresponding betas estimated prior
    stage2_model = sm.OLS(y_stage2, X_stage2).fit()
    print(stage2_model.summary())

if __name__ == "__main__":
    fama_mcbeth_regression("/Users/anniepi/Documents/UNC Work/econ525/FAMA_Mcbeth.xlsx")
