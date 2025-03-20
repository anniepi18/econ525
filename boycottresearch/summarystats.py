import pandas as pd

def stock_summary_table(stock_file):
    stock = pd.read_excel(stock_file)
    stock.drop(columns=["PERMNO"], inplace=True)
    stock.rename(columns={
        "Names Date": "Date",
        "Ticker Symbol": "Ticker",
        "Price or Bid/Ask Average": "Price",
        "Returns": "Return"
    }, inplace=True)
    summary_df = stock.groupby("Ticker").agg(
        count_price=("Price","count"),
        mean_price=("Price","mean"),
        std_price=("Price","std"),
        count_return=("Return","count"),
        mean_return=("Return","mean"),
        std_return=("Return","std")
    ).reset_index()
    print(summary_df)


if __name__ == "__main__":
    stock_summary_table("/Users/anniepi/Documents/UNC Work/econ525/boycottresearch/boycott_firms_stockdata.xlsx")
