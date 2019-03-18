from scripts import plot
import pandas as pd

df1 = pd.read_csv("data/enriched/MSFT.enriched.csv")

df2 = pd.read_csv("data/enriched/new.MSFT.enriched.csv")

for i in range(0, len(df1)):
    print(df1.ix[i]['sma100'] - df1.ix[i]['sma100'])
