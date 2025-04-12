"""Research Project First Draft Code"""
"""Annie Pi and Urvi Kode"""
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px  

def event_study(boycott_file, stock_file, factors_file):

    boycott = pd.read_excel(boycott_file)
    stock = pd.read_excel(stock_file)
    stock.drop(columns=["PERMNO"], inplace=True)
    stock.rename(columns={
        "Names Date": "Date", 
        "Ticker Symbol": "Ticker", 
        "Price or Bid/Ask Average": "Price", 
        "Returns": "Return"
    }, inplace=True)
    stock["Date"] = pd.to_datetime(stock["Date"])
    
    factors = pd.read_excel(factors_file)
    factors["Date"] = pd.to_datetime(factors["Date"])
    stock = pd.merge(stock, factors[["Date", "Mkt-RF", "RF"]], on="Date", how="left")
    stock["ExcessReturn"] = stock["Return"] - stock["RF"]
    boycott["Event_Date"] = pd.to_datetime(boycott["Event_Date"])

    # Estimation window: from event date minus 120 days to event date minus 20 days.
    estimation_days_back = (120, 20)
    
    #Each window always starts at (event_date - 5).
    window_lengths = [10, 15, 30, 60, 90, 120]
    
    #aggregating AR time series per event window
    event_results_list = []
    ar_agg = {w: {} for w in window_lengths}
    
    # looping over each boycott for each firm
    for i, event in boycott.iterrows():
        tkr = event["Ticker"]
        event_date = event["Event_Date"]
        df_tkr = stock[stock["Ticker"] == tkr].copy()
        if df_tkr.empty:
            continue
        
        #estimation windows for capm
        est_start = event_date - pd.Timedelta(days=estimation_days_back[0])
        est_end   = event_date - pd.Timedelta(days=estimation_days_back[1])
        df_est = df_tkr[(df_tkr["Date"] >= est_start) & (df_tkr["Date"] <= est_end)]
        #double checking there are enough observations to do it 
        if len(df_est) < 20:
            continue
        
        # capm regression
        # ExcessReturn = alpha + beta*(Mkt-RF)
        X_est = sm.add_constant(df_est["Mkt-RF"])
        y_est = df_est["ExcessReturn"]
        capm_model = sm.OLS(y_est, X_est).fit()
        alpha = capm_model.params["const"]
        beta = capm_model.params["Mkt-RF"]
        
        # Create summary record 
        event_summary = {"Ticker": tkr, "Event_Date": event_date}
        
        # Loop through each defined event window length.
        for win_length in window_lengths:
            window_start = event_date - pd.Timedelta(days=5)
            window_end = event_date + pd.Timedelta(days=(win_length - 5))
            
            df_window = df_tkr[(df_tkr["Date"] >= window_start) & (df_tkr["Date"] <= window_end)].copy()
            if df_window.empty:
                event_summary[f"CAR_{win_length}d"] = None
                continue
            
            X_window = sm.add_constant(df_window["Mkt-RF"])
            df_window["PredictedExcess"] = alpha + beta * df_window["Mkt-RF"]
            
            # Compute AR on each day.
            df_window["AR"] = df_window["ExcessReturn"] - df_window["PredictedExcess"]
            CAR = df_window["AR"].sum()
            event_summary[f"CAR_{win_length}d"] = CAR
            
            for _, row_w in df_window.iterrows():
                rel_day = (row_w["Date"] - event_date).days  # days relative to event (negative = before, positive = after)
                ar_agg[win_length].setdefault(rel_day, []).append(row_w["AR"])
                
        event_results_list.append(event_summary)
    
    results_df = pd.DataFrame(event_results_list)
    print("Summary of Cumulative Abnormal Returns (CAR) for each boycott event:")
    print(results_df)
    car_cols = [f"CAR_{w}d" for w in window_lengths]
    print("\nMean CAR across boycott events by event window:")
    print(results_df[car_cols].mean())
    
    # Fig 1 is a boxplot of CAR by window 
    plt.figure(figsize=(10, 6))
    car_data = results_df[car_cols].melt(var_name="Event_Window", value_name="CAR")
    sns.boxplot(x="Event_Window", y="CAR", data=car_data)
    plt.title("Distribution of Cumulative Abnormal Returns (CAR) by Event Window")
    plt.xlabel("Event Window")
    plt.ylabel("CAR")
    plt.show()
    
    # Fig 2:  AR Time Series for a window
    # chose 30 day window arbitrarily 
    chosen_window = 30
    if chosen_window in ar_agg:
        avg_ar = {}
        for rel_day, ar_list in ar_agg[chosen_window].items():
            avg_ar[rel_day] = sum(ar_list) / len(ar_list) if len(ar_list) > 0 else 0
        
        # Order the relative days
        sorted_days = sorted(avg_ar.keys())
        avg_ar_values = [avg_ar[day] for day in sorted_days]
        
        plt.figure(figsize=(10, 6))
        plt.plot(sorted_days, avg_ar_values, marker='o')
        plt.title(f"Average Abnormal Return (AR) Time Series for 30-Day Event Window")
        plt.xlabel("Relative Day (Days from Event Date)")
        plt.ylabel("Average AR")
        plt.axvline(x=0, color='red', linestyle='--', label='Event Date')
        plt.legend()
        plt.show()

if __name__ == "__main__":
    boycott_file = "/Users/anniepi/Documents/UNC Work/econ525/boycottresearch/boycott_dates.xlsx"
    stock_file = "/Users/anniepi/Documents/UNC Work/econ525/boycottresearch/boycott_firms_stockdata.xlsx"
    factors_file = "/Users/anniepi/Documents/UNC Work/econ525/boycottresearch/filtered_Daily_Factors_2015_2024.xlsx"
    
    event_study(boycott_file, stock_file, factors_file)
