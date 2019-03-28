import pandas as pd
import utilities as util
import math, sys
import tradeUtilities as tradeUtil
import config
from datetime import timedelta

class SMALSCrossover:
    def __init__(self):
        self.balance = self.startingBalance = 1000000
        self.unitsAvailable = 0
        self.stopLoss = sys.maxsize
        self.takeProfit = sys.maxsize
        self.lastBuyIndex = -1
        self.saved = 0
        self.buyDates = []
        self.sellDates = []

    """ Runs backtest """
    def runBacktest(self, path, longWindow, shortWindow, display):
        dataframe = pd.read_csv(path)
        count = len(dataframe)

        for i in range(1, count):

            heuristicResult = self.heuristic(dataframe, longWindow, shortWindow, i)
            lastPrice = dataframe.iloc[i]["close"]
            date = dataframe.iloc[i]["timestamp"]

            if heuristicResult == 1 and not self.isLong():

                """ Executing ORDINARY BUY order """
                self.balance, self.unitsAvailable, self.stopLoss, self.takeProfit = tradeUtil.ordinaryBuyMax(dataframe.iloc[i]["timestamp"], self.balance, dataframe.iloc[i]["close"], self.unitsAvailable, display)
                self.lastBuyIndex = i
                self.buyDates.append(pd.to_datetime(date))

            elif self.isLong() and (lastPrice < self.stopLoss or lastPrice > self.takeProfit):
                if lastPrice < self.stopLoss:

                    """ Executing STOP LOSS SELL order """
                    self.balance, self.unitsAvailable = tradeUtil.stopLossSell(dataframe.iloc[i]["timestamp"], self.balance, self.stopLoss, self.unitsAvailable, display)
                    diff1 = dataframe.iloc[i-1]["close"] - dataframe.iloc[i]["close"]
                    diff2 = dataframe.iloc[i-1]["close"] - self.stopLoss
                    frac = (diff2/diff1)*24
                    self.sellDates.append(pd.to_datetime(date)-timedelta(hours=24-frac))

                elif lastPrice > self.takeProfit:

                    """ Executing TAKE PROFIT SELL order """
                    self.balance, self.unitsAvailable = tradeUtil.takeProfitSell(dataframe.iloc[i]["timestamp"], self.balance, dataframe.iloc[i]["close"], self.unitsAvailable, display)
                    self.sellDates.append(pd.to_datetime(date))

                """ Transferring excess funds from balance to savings """
                if self.balance > self.startingBalance:
                    self.saved += self.balance - self.startingBalance
                    self.balance = self.startingBalance

        """ If last BUY order has no corresponding SELL order, do not include it in profit/loss calculations. """
        if self.isLong():
            if display:
                print("NOTE: Last BUY entry printed above was not closed, and is not factored in Profit/Loss calculation.")
            self.buyDates = self.buyDates[:-1]
            self.balance += dataframe.iloc[self.lastBuyIndex]["close"] * self.unitsAvailable

        self.balance = self.balance + self.saved
        returnPercentage = 100*((self.balance-self.startingBalance)/self.startingBalance)
        period = util.periods(path)/365

        avgReturnPercentage = round(returnPercentage/period, 2)
        period = round(period, 2)
        returnPercentage = round(returnPercentage, 2)
        self.balance = round(self.balance, 2)

        print("\nReturn: " + str(returnPercentage) + "% over a period of " + str(period) + " years (" + str(avgReturnPercentage) + "% per annum)")
        sys.stdout.flush()
        return self.buyDates, self.sellDates

    """ Returns true if you position == long i.e. already bought this stock"""
    def isLong(self):
        if self.unitsAvailable > 0:
            return True
        return False

    """ Returns >0.5 if current state signals BUY and <0.5 if SELL """
    def heuristic(self, df, longWindow, shortWindow, i=-1):
        if i == -1:
            i = len(df)-1
        longSMAColumn = "sma" + str(longWindow)
        shortSMAColumn = "sma" + str(shortWindow)
        if (df.iloc[i][shortSMAColumn] > df.iloc[i][longSMAColumn]):
            return 1
        else:
            return 0

    """ Returns % of time stocks upward/downward predictions are correct """
    def historicAccuracy(self, df, longWindow, shortWindow, nextNDays):
        count = len(df)
        upwardCorrectCount = 0
        downwardCorrectCount = 0
        upwardPredictionCount = 0
        downwardPredictionCount = 0
        for i in range(0, count-nextNDays):
            priceToday = df.iloc[i]['close']
            heur = self.heuristic(df, longWindow, shortWindow, i)
            if heur == 0: # Predicting downward move soon
                downwardPredictionCount += 1
                for j in range(i+1, i+1+nextNDays):
                    if (1-config.PERCENT_CHANGE)*priceToday > df.iloc[j]['close']:
                        downwardCorrectCount += 1
                        break
            elif heur == 1:
                upwardPredictionCount += 1
                for j in range(i+1, i+1+nextNDays):
                    if (1+config.PERCENT_CHANGE)*priceToday <= (df.iloc[j]['close']):
                        #print("HERE " + priceToday + " " + df.iloc[j]['close'])
                        upwardCorrectCount += 1
                        break
        upwardCorrectPct = 100*(upwardCorrectCount/(upwardPredictionCount))
        downwardCorrectPct = 100*(downwardCorrectCount/(downwardPredictionCount))
        return round(upwardCorrectPct, 2), round(downwardCorrectPct, 2)
