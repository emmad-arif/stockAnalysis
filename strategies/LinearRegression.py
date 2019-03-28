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
        df = df[i-window+1:i+1]
        df = df.reset_index()
        priceToday = df.iloc[-1]["close"]
        model = linear_model.LinearRegression().fit(df[["index"]], df[['close']])
        m = model.coef_[0]
        c = model.intercept_
        tomorrowPrediction = model.predict([[i+1]])[0][0]
        if tomorrowPrediction > priceToday:
            return 1
        else:
            return 0

    def historicAccuracy(self, df, window, nextNDays):
        count = len(df)
        upwardCorrectCount = 0
        downwardCorrectCount = 0
        upwardPredictionCount = 0
        downwardPredictionCount = 0
        for i in range(window, count-nextNDays):
            priceToday = df.iloc[i]['close']
            heur = self.heuristic(df, window, i)
            if heur == 1: # Predicting downward move soon
                downwardPredictionCount += 1
                for j in range(i+1, i+1+nextNDays):
                    if (1-config.PERCENT_CHANGE)*priceToday > df.iloc[j]['close']:
                        downwardCorrectCount += 1
                        break
            elif heur == 0:
                upwardPredictionCount += 1
                for j in range(i+1, i+1+nextNDays):
                    if (1+config.PERCENT_CHANGE)*priceToday <= (df.iloc[j]['close']):
                        #print("HERE " + priceToday + " " + df.iloc[j]['close'])
                        upwardCorrectCount +=1
                        break
        upwardCorrectPct = 100*(upwardCorrectCount/(upwardPredictionCount))
        downwardCorrectPct = 100*(downwardCorrectCount/(downwardPredictionCount))
        return round(upwardCorrectPct, 2), round(downwardCorrectPct, 2)
