import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt
import numpy as np
import sys
from scripts.indicators import rsi
import datetime
import utilities as util
import config
class RandomForest:


    def __init__(self, df, pastDays):

        if 'rsi14' not in df.columns:
            df = rsi.appendRSI(df, 14, False)

        keepColumns = ['close']
        PAST_DAYS = pastDays
        for i in range(1, len(df)):
            for j in range(1, PAST_DAYS+1):
                keepColumns.append('close' + str(j))
                df['close' + str(j)] = df.close.shift(j+PAST_DAYS-1)
                #df['prevRSI14' + str(j)] = df.rsi14.shift(j+PAST_DAYS-1)
        new_features = []
        for j in range(1, PAST_DAYS+1):
            new_features.append(df.close[len(df)-j])
        keepColumns = util.removeDuplicates(keepColumns)
        #print(keepColumns)
        #exit()
        #df = df.drop(['timestamp', 'open', 'high', 'low', 'volume', 'rsi14'], axis=1)
        df = df[keepColumns]
        df = df.dropna()
        #print(df.head())
        #exit()
        labels = np.array(df['close'])
        features = df.drop('close', axis=1)

        feature_list = list(features.columns)
        features = np.array(features)
        #print(feature_list)
        #exit()
        train_features, test_features, train_labels, test_labels = train_test_split(features, labels, test_size = 0.2, shuffle=True)

        rf = RandomForestRegressor(n_estimators = 1000)

        rf.fit(train_features, train_labels)
        predictions = rf.predict(test_features)

        self.upwardCorrectCount = 0
        self.downwardCorrectCount = 0
        self.upwardPredictionCount = 0
        self.downwardPredictionCount = 0


        for i in range(0, len(predictions)):
            lastKnownClose = test_features[i][0]
            pred = predictions[i]
            actualClose = test_labels[i]
            if pred > lastKnownClose: # Predicting upward move soon
                self.upwardPredictionCount += 1
                if actualClose > (1+config.PERCENT_CHANGE)*lastKnownClose:
                    #print("CORRECT as " + str(actualClose) + " > " + str(lastKnownClose) + " and " + str(pred) + " > " + str(lastKnownClose))
                    self.upwardCorrectCount += 1

            elif pred < lastKnownClose:
                self.downwardPredictionCount += 1
                if actualClose < (1-config.PERCENT_CHANGE)*lastKnownClose:
                    #print("CORRECT as " + str(actualClose) + " < " + str(lastKnownClose) + " and " + str(pred) + " < " + str(lastKnownClose))
                    self.downwardCorrectCount += 1


        # New prediction for last day available
        rows, cols = (1, PAST_DAYS)
        arr = [[0]*cols]*rows
        for i in range(0, PAST_DAYS):
            arr[0][i] = new_features[i]
        #print(arr)
        #print(str(rf.predict(arr)[0]))
        #print(str(arr[0]))
        #exit()
        if (rf.predict(arr))[0] > arr[0][0]:
            self.currentPrediction = 1
        else:
            self.currentPrediction = 0

    def heuristic(self):
        return self.currentPrediction

    def historicAccuracy(self):
        upwardCorrectPct = 100*(self.upwardCorrectCount/(self.upwardPredictionCount))
        downwardCorrectPct = 100*(self.downwardCorrectCount/(self.downwardPredictionCount))
        return round(upwardCorrectPct, 2), round(downwardCorrectPct, 2)
