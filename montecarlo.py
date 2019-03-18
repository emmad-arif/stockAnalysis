import pandas as pd
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style

style.use('ggplot')

df = pd.read_csv("data/raw/TSLA.csv")

df.iloc[:] = df.iloc[::-1].values

prices = df[['close']]
prices = df.close
returns = prices.pct_change()
last_price = prices[len(prices)-1]
#print(last_price)
#Number of Simulations
num_simulations = 1000
num_days = 252

simulation_df = pd.DataFrame()

for x in range(num_simulations):
    count = 0
    daily_vol = returns.std()

    price_series = []

    price = last_price * (1 + np.random.normal(0, daily_vol))
    price_series.append(price)

    for y in range(num_days):
        if count == 251:
            break
        price = price_series[count] * (1 + np.random.normal(0, daily_vol))
        price_series.append(price)
        count += 1

    simulation_df[x] = price_series

for i in range(0,252):

    print(np.mean(simulation_df.iloc[i]))
fig = plt.figure()
fig.suptitle('Monte Carlo Simulation')
plt.plot(simulation_df)
plt.axhline(y = last_price, color = 'r', linestyle = '-')
plt.xlabel('Day')
plt.ylabel('Price')
plt.show()
#------------------------------------------------------------------------------------#

"""
5     319.770
4     295.390
3     326.090
2     316.130
1     333.870
0     332.800

"""
