import pullAndEnrich
import utilities as util
from scripts import plot as plt
import predict, sys, os
from strategies import emaC, SMACrossover, smaLSC, RSI, randomStrategy
import datetime # linear

randomStrategyCount = 10

##########################################################################################3


if len(sys.argv) < 2:
    file = open("backtestHelp.txt", "r")
    print (file.read())
    exit()

if "-h" in sys.argv or "-H" in sys.argv:
    file = open("backtestHelp.txt", "r")
    print (file.read())
    exit()


ticker = sys.argv[1][1:].upper()
enrichedPath = "data/enriched/" + ticker + ".enriched.csv"
rawPath = "data/raw/" + ticker + ".csv"

indicators = []
strategies = []
plot = False
forcePull = False

""" Process command line arguments"""

for i in range(2, len(sys.argv)):
    arg = sys.argv[i].lower()

    if arg[0] != '-':
        continue
    arg = arg[1:]

    if arg == "smac":
        smaPeriod = sys.argv[i+1]
        strategies.append(arg + smaPeriod)
        indicators.append("sma" + smaPeriod)
        continue

    if arg == "emac":
        emaPeriod = sys.argv[i+1]
        strategies.append(arg + emaPeriod)
        indicators.append("ema" + emaPeriod)
        continue

    if arg == "smalsc":
        smaLongPeriod = sys.argv[i+1]
        smaShortPeriod = sys.argv[i+2]
        if int(smaLongPeriod) <= int(smaShortPeriod):
            print("Error: SMA Long Horizon must be longer than SMA Short Horizon")
            sys.stdout.flush()
            continue
        strategies.append(arg + smaLongPeriod + '-' + smaShortPeriod)
        indicators.append("sma" + smaLongPeriod)
        indicators.append("sma" + smaShortPeriod)
        continue

    if arg == "rsi":
        strategies.append("rsi")
        indicators.append("rsi")
        continue

    if arg == "plot":
        plot = True

    if arg == "forcepull":
        forcePull = True

""" Remove Duplicates from strategies and indicators """

indicators = util.removeDuplicates(indicators)
strategies = util.removeDuplicates(strategies)

""""
print("Strategies:")
print(strategies)

print("Indicators:")
print(indicators)

exit()
"""

if forcePull and os.path.isfile(rawPath):
    os.unlink(rawPath)

if os.path.isfile(enrichedPath):
    os.unlink(enrichedPath)

""" Pull and/or Enrich pricing data """
pullAndEnrich.pullAndEnrich(ticker, "full", rawPath, enrichedPath, indicators)


for strategy in strategies:
    if "smac" in strategy:
        horizon = strategy[4:]
        print("\nSimulating SMA Crossover Strategy with time horizon: " + horizon)
        sys.stdout.flush()
        SMACrossover.SMACrossover().runBacktest(enrichedPath, int(horizon))

    elif "emac" in strategy:
        horizon = strategy[4:]
        print("\nSimulating EMA Crossover Strategy with time horizon: " + horizon)
        sys.stdout.flush()
        emaC.emaCrossover(enrichedPath, int(horizon))

    elif "smalsc" in strategy:
        i = 0
        for letter in strategy:
            if letter == '-':
                break
            i += 1
        longHorizon = strategy[6:i]
        shortHorizon = strategy[i+1:]
        print("\nSimulating SMA Long/Short Crossover Strategy with long time horizon: " + longHorizon + " and short time horizon: " + shortHorizon)
        sys.stdout.flush()
        smaLSC.smaLongShortCrossover(enrichedPath, int(longHorizon), int(shortHorizon))

    elif "rsi" in strategy:
        print("\nSimulating RSI Strategy")
        RSI.RSI().runBacktest(enrichedPath)
        sys.stdout.flush()


if len(strategy) > 0:
    print("\nSimulating Random Strategy " + str(randomStrategyCount) + " times.")
    randomReturn = randomStrategy.runMultipleRandoms(enrichedPath, randomStrategyCount)
    print("\nRandom strategy would have returned: " + str(randomReturn) + "% over the same period of time (on average).")
    sys.stdout.flush()

if plot:
    plt.plot(ticker, enrichedPath, indicators)
    #print("WOOO")


"""
if "-smaLSC" in sys.argv:
    predict.smaLongShortCrossover(enrichedPath, 200, 20)

if "-emaC" in sys.argv:
    predict.emaCrossover(enrichedPath, 10)

if "-four" in sys.argv:
    predict.fourCandleHammer(rawPath)
"""
#predict.smaCrossover(path, 20)
#plot.plot(path, "sma5", "ema5")
