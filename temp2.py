import linear
import pandas as pd
from scripts import plot
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv("data/raw/TSLA.csv")
df.iloc[:] = df.iloc[::-1].values
df = linear.RSI(df)

df = df[['timestamp', 'close', 'RSI']]


fig, ax = plt.subplots()
ax.plot(df.index, df.close, df.RSI)

ax.set(xlabel='time (days)', ylabel='close price ($)',
       title='TSLA')
ax.grid()

plt.axhline(y=30, color='r', linestyle='-')
plt.axhline(y=70, color='r', linestyle='-')
fig.savefig("test.png")
plt.show()
