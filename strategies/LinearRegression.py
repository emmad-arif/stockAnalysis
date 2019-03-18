import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import linear_model
from datetime import datetime
import pandas as pd
import utilities as util
import math, sys
import tradeUtilities as tradeUtil
import config

class LinearRegression:

    def heuristic(self, df, window, i=-1):
        if i == -1:
            i = len(df)-1
        #print(df)
        df = df[i-window+1:i+1]
        #print(ser)
        #df = df.drop(df.index[pd.Series()])
        df = df.reset_index()

        #print(df)
        #exit()
        priceToday = df.iloc[-1]["close"]
        model = linear_model.LinearRegression().fit(df[["index"]], df[['close']])
        m = model.coef_[0]
        c = model.intercept_

        tomorrowPrediction = model.predict([[i+1]])[0][0]

        if tomorrowPrediction > priceToday:
            #print("UP")
            return 1
        else:
            #print("DOWN")
            return 0

    def historicAccuracy(self, df, window, nextNDays):
        count = len(df)
        correctCount = 0
        predictionCount = 0
        for i in range(window, count-nextNDays):
            priceToday = df.iloc[i]['close']
            heur = self.heuristic(df, window, i)
            if heur == 1: # Predicting downward move soon
                predictionCount += 1
                for j in range(i+1, i+1+nextNDays):
                    if (1-config.PERCENT_CHANGE)*priceToday > df.iloc[j]['close']:
                        correctCount += 1
                        break
            elif heur == 0:
                predictionCount += 1
                for j in range(i+1, i+4):
                    if (1+config.PERCENT_CHANGE)*priceToday <= (df.iloc[j]['close']):
                        #print("HERE " + priceToday + " " + df.iloc[j]['close'])
                        correctCount += 1
                        break
        correctPct = 100*(correctCount/(predictionCount))
        return round(correctPct, 2)
