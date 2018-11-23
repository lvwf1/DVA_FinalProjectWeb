import pandas as pd

df1 = pd.read_csv("csv/Seasons_Stats.csv")
df2 = pd.read_csv("csv/label.csv")
merged = df1.merge(df2, on=["Player", "Year"], how="outer").fillna("")
merged.to_csv("merged.csv", index=False)