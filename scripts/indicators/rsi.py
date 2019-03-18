import pandas as pd
import sys
def appendRSI(df, column="close", period=14):
    # wilder's RSI

    delta = df[column].diff()
    up, down = delta.copy(), delta.copy()

    up[up < 0] = 0
    down[down > 0] = 0

    rUp = up.ewm(com=period - 1,  adjust=False).mean()
    rDown = down.ewm(com=period - 1, adjust=False).mean().abs()

    rsi = 100 - 100 / (1 + rUp / rDown)
    df = df[period+1:]

    df =  df.join(rsi.to_frame('rsi'))
    print("\nRSI" + str(period) + " added to data.")
    sys.stdout.flush()
    return df.reset_index(drop=True)
