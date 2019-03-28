import pullAndEnrich
import utilities as util
from scripts import plot as plt
import predict, sys, os
from strategies import EMACrossover, SMACrossover, SMALSCrossover, RSI, LinearRegression, randomStrategy, RandomForest
import datetime # linear
import pandas as pd
import config

PERCENT_CHANGE = config.PERCENT_CHANGE
SMAC_WINDOW = config.SMAC_WINDOW
EMAC_WINDOW = config.EMAC_WINDOW
LR_WINDOW = config.LR_WINDOW
RSI_WINDOW = config.RSI_WINDOW # implement dynamic enrichment logic
TIME_HORIZON = config.TIME_HORIZON
SMALSC_LONG_WINDOW = config.SMALSC_LONG_WINDOW
SMALSC_SHORT_WINDOW = config.SMALSC_SHORT_WINDOW

if len(sys.argv) < 2:
    file = open("adviceHelp.txt", "r")
    print (file.read())
    exit()

if "-h" in sys.argv or "-H" in sys.argv:
    file = open("adviceHelp.txt", "r")
    print (file.read())
    exit()


ticker = sys.argv[1][1:].upper()
enrichedPath = "data/enriched/" + ticker + ".enriched.csv"
rawPath = "data/raw/" + ticker + ".csv"

indicators = ["rsi" + str(RSI_WINDOW), "sma" + str(SMAC_WINDOW), "sma" + str(SMALSC_LONG_WINDOW), "sma" + str(SMALSC_SHORT_WINDOW), "ema" + str(EMAC_WINDOW)]
indicators = util.removeDuplicates(indicators)

plot = False
forcePull = False
if "-plot" in sys.argv:
    plot = True

if "-forcepull" in sys.argv or "-forcePull" in sys.argv:
    forcePull = True


if forcePull and os.path.isfile(rawPath):
    os.unlink(rawPath)

if os.path.isfile(enrichedPath):
    os.unlink(enrichedPath)

""" Pull and/or Enrich pricing data """
pullAndEnrich.pullAndEnrich(ticker, "full", rawPath, enrichedPath, indicators)
df = pd.read_csv(enrichedPath)

print("\n** Note pertaining to the historical accuracies presented below **")
print("Historic predictions are considered successful if the stock moved at least " + str(PERCENT_CHANGE*100) + "% in the direction predicted, within a " + str(TIME_HORIZON) + " day period.")
print("For example, a \"Historical Accuracy of Upward Predictions\" value of 60% means that 60% of the time the strategy predicted an upward\nmove, the stock gained " + str(PERCENT_CHANGE*100) + "% within the next " + str(TIME_HORIZON) + " days." )
print("\nAll predictions are relative to " + ticker + " stock's last quoted price of $" + str(df.iloc[len(df)-1]['close']) + " on " + df.iloc[len(df) - 1]['timestamp'])
print("I.e. An upward prediction is predicting that the stock will gain at least " + str(PERCENT_CHANGE*100) + "% within the next " + str(TIME_HORIZON) + " days.")
print("A downward prediction is predicting that the stock will lose at least " + str(PERCENT_CHANGE*100) + "% within the next " + str(TIME_HORIZON) + " days.")

print("\nYou may change these parameters, in config.py")

""" Run RSI """

strat = RSI.RSI()
result = strat.heuristic(df, RSI_WINDOW)
historicAccuracyUp, historicAccuracyDown = strat.historicAccuracy(df, RSI_WINDOW, TIME_HORIZON)

print("\n** " + str(RSI_WINDOW) + " day RSI **")

if result >= 0.7:
    print("Prediction: Upward move")
elif result <= 0.3:
    print("Prediction: Downard move")
else:
    print("Prediction: Uncertain")
print("Historical Accuracy of Upward Predictions: " + str(historicAccuracyUp) + "%")
print("Historical Accuracy of Downward Predictions: " + str(historicAccuracyDown) + "%")
sys.stdout.flush()


""" Run SMA Crossover """

strat = SMACrossover.SMACrossover()
result = strat.heuristic(df, SMAC_WINDOW)
historicAccuracyUp, historicAccuracyDown = strat.historicAccuracy(df, SMAC_WINDOW, TIME_HORIZON)

print("\n** " + str(SMAC_WINDOW) + " day SMA Crossover **")

if result == 1:
    print("Prediction: Upward move")
elif result == 0:
    print("Prediction: Downward move")
else:
    print("Prediction: Uncertain")
print("Historical Accuracy of Upward Predictions: " + str(historicAccuracyUp) + "%")
print("Historical Accuracy of Downward Predictions: " + str(historicAccuracyDown) + "%")
sys.stdout.flush()

""" Run SMA Long Short Crossover """

strat = SMALSCrossover.SMALSCrossover()
result = strat.heuristic(df, SMALSC_LONG_WINDOW, SMALSC_SHORT_WINDOW)
historicAccuracyUp, historicAccuracyDown = strat.historicAccuracy(df, SMALSC_LONG_WINDOW, SMALSC_SHORT_WINDOW, TIME_HORIZON)

print("\n** " + str(SMALSC_LONG_WINDOW) +  " day Long " + str(SMALSC_SHORT_WINDOW) + " day Short SMA Crossover **")

if result == 1:
    print("Prediction: Upward move")
elif result == 0:
    print("Prediction: Downward move")
else:
    print("Prediction: Uncertain")
print("Historical Accuracy of Upward Predictions: " + str(historicAccuracyUp) + "%")
print("Historical Accuracy of Downward Predictions: " + str(historicAccuracyDown) + "%")
sys.stdout.flush()


""" Run EMA Crossover """

strat = EMACrossover.EMACrossover()
result = strat.heuristic(df, EMAC_WINDOW)
historicAccuracyUp, historicAccuracyDown = strat.historicAccuracy(df, EMAC_WINDOW, TIME_HORIZON)

print("\n** " + str(EMAC_WINDOW) + " day EMA Crossover **")


if result == 1:
    print("Prediction: Upward move")
elif result == 0:
    print("Prediction: Downward move")
else:
    print("Prediction: Uncertain")
print("Historical Accuracy of Upward Predictions: " + str(historicAccuracyUp) + "%")
print("Historical Accuracy of Downward Predictions: " + str(historicAccuracyDown) + "%")
sys.stdout.flush()

""" Run Linear Regression """

strat = LinearRegression.LinearRegression()
result = strat.heuristic(df, LR_WINDOW)
historicAccuracyUp, historicAccuracyDown = strat.historicAccuracy(df, LR_WINDOW, TIME_HORIZON)

print("\n** " + str(LR_WINDOW) + " day Linear Regression **")


if result == 1:
    print("Prediction: Upward move")
elif result == 0:
    print("Prediction: Downward move")
else:
    print("Prediction: Uncertain")
print("Historical Accuracy of Upward Predictions: " + str(historicAccuracyUp) + "%")
print("Historical Accuracy of Downward Predictions: " + str(historicAccuracyDown) + "%")
sys.stdout.flush()

""" Run Random Forest """

strat = RandomForest.RandomForest(df, TIME_HORIZON)
result = strat.heuristic()
historicAccuracyUp, historicAccuracyDown = strat.historicAccuracy()

print("\n** Random Forest **")
if result == 1:
    print("Prediction: Upward move")
elif result == 0:
    print("Prediction: Downward move")
else:
    print("Prediction: Uncertain")
print("Historical Accuracy of Upward Predictions: " + str(historicAccuracyUp) + "%")
print("Historical Accuracy of Downward Predictions: " + str(historicAccuracyDown) + "%")
sys.stdout.flush()

if plot:
    plt.plot(ticker, enrichedPath, indicators)

exit()
