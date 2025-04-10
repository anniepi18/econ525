"""PS3 Computional: Annie Pi 730502223"""
import pandas as pd 
import numpy as np 
import statsmodels.api as sm
from statsmodels.formula.api import ols

#df = pd.read_excel("/Users/anniepi/Documents/UNC Work/econ525/problemsets/Moderna_Pfizer Event Study.xlsx")
df = pd.read_excel(
    "/Users/anniepi/Documents/UNC Work/econ525/problemsets/PS3_IhateExcel.xlsx",
    converters={'PFE': lambda x: pd.to_numeric(x, errors='coerce')})
df.columns = df.columns.str.strip()  #get rid of extra spaces
df['PFE'] = pd.to_numeric(df['PFE'], errors='coerce')      # Changed: Ensure PFE is numeric
df['RF'] = pd.to_numeric(df['RF'], errors='coerce')          # Changed: Ensure RF is numeric
df['MRNA'] = pd.to_numeric(df['MRNA'], errors='coerce')      # Changed: Ensure MRNA is numeric
df['Mkt-RF'] = pd.to_numeric(df['Mkt-RF'], errors='coerce')
#df = df.rename(columns={'Mkt-RF': 'Mkt_RF'})
# i literally almost shot myself in the face trying to fix the excel sheet 
df['Date'] = pd.to_datetime(df['Names Date'])
#df = df.sort_values('Date')
#print(df[['PFE', 'RF']].head())
#print(df[['PFE', 'RF']].dtypes)

est_start_pfizer = pd.to_datetime("2019-01-02") # did Jan 2 because no trading on Jan 1
est_end_pfizer   = pd.to_datetime("2020-12-03")

est_window_pfizer = df[(df['Date'] >= est_start_pfizer) & (df['Date'] <= est_end_pfizer)].copy()
num_observations = len(est_window_pfizer)
print("Number of observations in Pfizer estimation window:", num_observations)

# CAPM regression = pfe return minus rf
est_window_pfizer['PFE_excess'] = est_window_pfizer['PFE'] - est_window_pfizer['RF']
X_pfe = sm.add_constant(est_window_pfizer['Mkt-RF'])
#print(X_pfe)
y_pfe = est_window_pfizer['PFE_excess']
#print(y_pfe)
model_pfe = sm.OLS(y_pfe, X_pfe).fit()
#model_pfe= ols('PFE_excess ~ Q("Mkt-RF")', data=est_window_pfizer).fit()
print("\nPfizer CAPM Regression :)")

print(model_pfe.summary())

est_end_mrna = pd.to_datetime("2020-12-10")
# We select the last "num_obs" observations ending at Dec 10, 2020.
est_window_mrna = df[df['Date'] <= est_end_mrna].sort_values('Date').tail(num_observations).copy()
print("\nModerna estimation window from:",
      est_window_mrna['Date'].iloc[0].strftime('%Y-%m-%d'),
      "to",
      est_window_mrna['Date'].iloc[-1].strftime('%Y-%m-%d'))
est_window_mrna['MRNA_excess'] = est_window_mrna['MRNA'] - est_window_mrna['RF']

X_mrna = sm.add_constant(est_window_mrna['Mkt-RF'])
y_mrna = est_window_mrna['MRNA_excess']

model_mrna = sm.OLS(y_mrna, X_mrna).fit()
print("\nModerna CAPM Regression :)")
print(model_mrna.summary())

#doing abnormal returns in event windwo
event_start_pfe = pd.to_datetime("2020-12-04")
event_window_pfe = df[df['Date'] >= event_start_pfe].sort_values('Date').head(20).copy()


event_window_pfe['PFE_excess'] = event_window_pfe['PFE'] - event_window_pfe['RF']
event_window_pfe['predicted_PFE_excess'] = (model_pfe.params['const'] +
                                            model_pfe.params['Mkt-RF'] * event_window_pfe['Mkt-RF'])
event_window_pfe['abnormal_PFE'] = event_window_pfe['PFE_excess'] - event_window_pfe['predicted_PFE_excess']

print("\nHead of Pfizer abnormal returns in the event window:")
print(event_window_pfe[['Date', 'abnormal_PFE']].head())

# Event window for Moderna
event_start_mrna = pd.to_datetime("2020-12-11")
event_window_mrna = df[df['Date'] >= event_start_mrna].sort_values('Date').head(20).copy()

event_window_mrna['MRNA_excess'] = event_window_mrna['MRNA'] - event_window_mrna['RF']
event_window_mrna['predicted_MRNA_excess'] = (model_mrna.params['const'] +
                                             model_mrna.params['Mkt-RF'] * event_window_mrna['Mkt-RF'])
event_window_mrna['abnormal_MRNA'] = event_window_mrna['MRNA_excess'] - event_window_mrna['predicted_MRNA_excess']

print("\nHead of Moderna abnormal returns in the event window:")
print(event_window_mrna[['Date', 'abnormal_MRNA']].head())

windows = [5, 10, 15, 20]
cumulative_abnormal_pfe = {}
cumulative_abnormal_mrna = {}

for w in windows:
    cumulative_abnormal_pfe[w] = event_window_pfe['abnormal_PFE'].head(w).sum()
    cumulative_abnormal_mrna[w] = event_window_mrna['abnormal_MRNA'].head(w).sum()

print("\nCumulative Abnormal Returns (CAR) for Pfizer:")
for w in windows:
    print(f"CAR for first {w} days: {cumulative_abnormal_pfe[w]:.4f}")

print("\nCumulative Abnormal Returns (CAR) for Moderna:")
for w in windows:
    print(f"CAR for first {w} days: {cumulative_abnormal_mrna[w]:.4f}")
