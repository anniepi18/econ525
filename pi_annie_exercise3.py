import pandas as pd

# combining iorb stuff
df1 = pd.read_excel("IOER.xlsx", sheet_name="Daily, 7-Day")
df2 = pd.read_excel("IORB.xlsx", sheet_name="Daily, 7-Day")
df1 = df1.rename(columns={"IOER": "IORB"})

iorb_df = pd.concat([df1, df2])
iorb_df = iorb_df.sort_values("observation_date").drop_duplicates("observation_date", keep="last")
iorb_df = iorb_df[["observation_date", "IORB"]].reset_index(drop=True)

fedfunds_df = pd.read_excel("fedfundsrate.xlsx", sheet_name="Daily, 7-Day")
fedfunds_df = fedfunds_df[["observation_date", "DFF"]]

discount_df = pd.read_excel("discountrate.xlsx", sheet_name="Daily")
discount_df = discount_df[["observation_date", "DPCREDIT"]]

#reverse repo
reverserepo_df = pd.read_excel("reversereporates.xlsx", sheet_name="Daily")

# Merge all on observation_date
combined_df = iorb_df.merge(fedfunds_df, on="observation_date", how="inner")
combined_df = combined_df.merge(discount_df, on="observation_date", how="inner")
combined_df = combined_df.merge(reverserepo_df, on="observation_date", how="left")
combined_df["RRPONTSYAWARD"] = combined_df["RRPONTSYAWARD"].fillna("N/A")

#saving it
combined_df.to_excel("pi_annie_exercise3.xlsx", index=False)

#print(combined_df.head())

