""" PERCENT_CHANGE: Minimum % change that must occur for prediction to count as successful """
""" SMAC_WINDOW: Simple Moving Average Window i.e. Use this many previous days for SMA """
""" EMAC_WINDOW: Exponential Moving Average Window i.e. Use this many previous days for EMA """
""" LR_WINDOW: Linear Regression Window i.e. Use this many previous days for LR """
""" RSI_WINDOW: RSI Window i.e. Use this many previous days for RSI """
""" TIME_HORIZON: Maximum number of days you want to stay invested in one stock """

""" Change values here: """

PERCENT_CHANGE = 1 # i.e. 0.5% -

SMAC_WINDOW = 5
EMAC_WINDOW = 5
LR_WINDOW = 5
RSI_WINDOW = 5
SMALSC_LONG_WINDOW = 100
SMALSC_SHORT_WINDOW = 10
TIME_HORIZON = 20


""" Do NOT change anything after this """
PERCENT_CHANGE = PERCENT_CHANGE/100
