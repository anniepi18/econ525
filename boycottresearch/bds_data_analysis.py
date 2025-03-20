"""Research Project First Draft Code"""
"""Annie Pi and Urvi Kode"""

import pandas as pd
import statsmodels.api as sm

def event_study(boycott_file, stock_file):
    boycott = pd.read_excel(boycott_file)
    stock = pd.read_excel(stock_file)
    stock.drop(columns=["PERMNO"], inplace=True)
    stock.rename(columns={"Names Date": "Date", "Ticker Symbol": "Ticker", "Price or Bid/Ask Average": "Price", "Returns": "Return"}, inplace=True)
    stock["Date"] = pd.to_datetime(stock["Date"])
    if "MarketReturn" not in stock.columns:
        market_returns = stock.groupby("Date")["Return"].mean().reset_index().rename(columns={"Return": "MarketReturn"})
        stock = stock.merge(market_returns, on="Date", how="left")
    boycott["Event_Date"] = pd.to_datetime(boycott["Event_Date"])
    boycott["Window_Start"] = pd.to_datetime(boycott["Window_Start"])
    boycott["Window_End"] = pd.to_datetime(boycott["Window_End"])
    results = []
    for i, row in boycott.iterrows():
        tkr = row["Ticker"]
        event_date = row["Event_Date"]
        est_start = event_date - pd.Timedelta(days=120)
        est_end = event_date - pd.Timedelta(days=20)
        window_start = row["Window_Start"]
        window_end = row["Window_End"]
        df_tkr = stock[stock["Ticker"] == tkr].copy()
        df_est = df_tkr[(df_tkr["Date"] >= est_start) & (df_tkr["Date"] <= est_end)]
        if len(df_est) < 20:
            continue
        X_est = sm.add_constant(df_est["MarketReturn"])
        y_est = df_est["Return"]
        capm = sm.OLS(y_est, X_est).fit()
        alpha = capm.params["const"]
        beta = capm.params["MarketReturn"]
        df_window = df_tkr[(df_tkr["Date"] >= window_start) & (df_tkr["Date"] <= window_end)].copy()
        df_window["Predicted"] = alpha + beta * df_window["MarketReturn"]
        df_window["AR"] = df_window["Return"] - df_window["Predicted"]
        CAR = df_window["AR"].sum()
        results.append([tkr, event_date, window_start, window_end, CAR])
    results_df = pd.DataFrame(results, columns=["Ticker", "Event_Date", "Window_Start", "Window_End", "CAR"])
    print(results_df)
    print("Mean CAR:", results_df["CAR"].mean())

if __name__ == "__main__":
    boycott_file = "/Users/anniepi/Documents/UNC Work/econ525/boycottresearch/boycott_dates.xlsx"
    stock_file = "/Users/anniepi/Documents/UNC Work/econ525/boycottresearch/boycott_firms_stockdata.xlsx"
    event_study(boycott_file, stock_file)



