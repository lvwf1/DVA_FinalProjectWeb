import pandas as pd

df1 = pd.read_csv("csv/Playoffs_Stats.csv")
df2 = pd.read_csv("csv/Playoffs_Stats_adv.csv")
merged = df1.merge(df2, on=["Player","Year","Age","Tm"], how="outer").fillna("")
merged.to_csv("merged.csv", index=False)