import pandas as pd
import utilities as util
import math, sys
import tradeUtilities as tradeUtil
import config

class EMACrossover:
    balance = startingBalance = 1000000
    unitsAvailable = 0
    stopLoss = sys.maxsize
    lastBuyIndex = -1

    def runBacktest(self, path, window):
        dataframe = pd.read_csv(path)
        count = len(dataframe)

        for i in range(0, count):
            heuristicResult = self.heuristic(dataframe, window, i)

            if heuristicResult == 1 and not self.isLong() :
                self.balance, self.unitsAvailable, self.stopLoss = tradeUtil.ordinaryBuyMax(dataframe.iloc[i]["timestamp"], self.balance, dataframe.iloc[i]["close"], self.unitsAvailable)
                self.lastBuyIndex = i

            elif heuristicResult == 0 and self.isLong():
                self.balance, self.unitsAvailable = tradeUtil.ordinarySellMax(dataframe.iloc[i]["timestamp"], self.balance, dataframe.iloc[i]["close"], self.unitsAvailable)

        # Make sure last buy was closed --- fix this
        if self.isLong():
            print("NOTE: Last BUY entry printed above is invalid. Please ignore.")
            self.balance += dataframe.iloc[self.lastBuyIndex]["close"] * self.unitsAvailable

        returnPercentage = 100*((self.balance-self.startingBalance)/self.startingBalance)
        period = util.periods(dataframe)/365

        avgReturnPercentage = round(returnPercentage/period, 2)
        period = round(period, 2)
        returnPercentage = round(returnPercentage, 2)
        self.balance = round(self.balance, 2)

        print("\nReturn: " + str(returnPercentage) + "% over a period of " + str(period) + " years (" + str(avgReturnPercentage) + "% per annum)")
        print("--------------------")
        sys.stdout.flush()

    def isLong(self):
        if self.unitsAvailable > 0:
            return True
        return False

    def heuristic(self, df, window, i=-1):
        if i == -1:
            i = len(df)-1
        price = df.iloc[i]["close"]
        ema = df.iloc[i]["ema" + str(window)]
        if (price > ema):
            return 1
        else:
            return 0

    def historicAccuracy(self, df, window, nextNDays):
        count = len(df)
        correctCount = 0
        predictionCount = 0
        emaColumn = "ema" + str(window)
        for i in range(0, count-nextNDays):
            priceToday = df.iloc[i]['close']
            emaValue = df.iloc[i][emaColumn]
            if priceToday < emaValue: # Predicting downward move soon
                predictionCount += 1
                for j in range(i+1, i+1+nextNDays):
                    if (1-config.PERCENT_CHANGE)*priceToday > df.iloc[j]['close']:
                        correctCount += 1
                        break
            elif priceToday > emaValue:
                predictionCount += 1
                for j in range(i+1, i+4):
                    if (1+config.PERCENT_CHANGE)*priceToday <= (df.iloc[j]['close']):
                        #print("HERE " + priceToday + " " + df.iloc[j]['close'])
                        correctCount += 1
                        break
        correctPct = 100*(correctCount/(predictionCount))
        return round(correctPct, 2)
