import pullAndEnrich
import utilities as util
from scripts import plot
import predict

import datetime
ticker = "spx"
ticker = ticker.upper()
size = "full"
enrichedPath = "data/enriched/" + ticker + ".enriched.csv"
rawPath = "data/raw/" + ticker + ".csv"

##########################################################################################3
#pullAndEnrich.pullAndEnrich(ticker, size, "data/raw/", "data/enriched/", "sma20", "sma100")


predict.smaLongShortCrossover(enrichedPath, 100, 20)
#predict.smaCrossover(path, 20)
#plot.plot(path, "sma5", "ema5")
