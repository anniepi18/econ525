"""Annie Pi 730502223 ECON 493 Assignment: Feb 28 2025"""
import statsmodels.api as sm
import matplotlib.pyplot as plt
import pandas as pd

#with time series we use AIC to measure goodness of fit over R-squared

def run_fama_french_regressions(crsp_file, ff_file):
    crsp = pd.read_excel(crsp_file)
    crsp = crsp.iloc[:, 1:]
    crsp.rename(columns={"Names Date": "date", "Ticker Symbol": "TICKER", "Returns": "RET"}, inplace=True)
    crsp["date"] = pd.to_datetime(crsp["date"], format="%m/%d/%y")
    crsp["year_month"] = crsp["date"].dt.strftime("%Y-%m")
    ff = pd.read_excel(ff_file, skiprows=3, header=None, usecols=[0,1,2,3,4])
    ff.columns = ["raw_ym", "Mkt-RF", "SMB", "HML", "RF"]
    ff["raw_ym"] = ff["raw_ym"].apply(lambda x: str(int(x)) if pd.notnull(x) else None)
    ff["raw_ym"] = pd.to_datetime(ff["raw_ym"], format="%Y%m")
    ff["year_month"] = ff["raw_ym"].dt.strftime("%Y-%m")
    merged = pd.merge(crsp, ff, on="year_month", how="inner")
    #data cleaning is so annoying 
    for t in ["AAPL", "WMT", "MCD"]:
        df = merged[merged["TICKER"] == t].copy()
        for col in ["RET", "Mkt-RF", "SMB", "HML", "RF"]:
            df[col] = pd.to_numeric(df[col], errors="coerce")
        #doing the /100 to convert to decimal from percent 
        df["Mkt_RF"] = df["Mkt-RF"] / 100
        df["SMB"] = df["SMB"] / 100
        df["HML"] = df["HML"] / 100
        df["RF"] = df["RF"] / 100
        df["excess_ret"] = df["RET"] - df["RF"]
        X = sm.add_constant(df[["Mkt_RF", "SMB", "HML"]])
        y = df["excess_ret"]
        model = sm.OLS(y, X).fit()
        print(t)
        print(model.summary())

if __name__ == "__main__":
    crsp_file = "/Users/anniepi/Documents/UNC Work/econ525/wmt_aapl_mcd.xlsx"
    ff_file = "/Users/anniepi/Documents/UNC Work/econ525/FAMA French 3 Factors monthly 2020.xlsx"
    run_fama_french_regressions(crsp_file, ff_file)


