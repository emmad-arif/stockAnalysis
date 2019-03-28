# Pandas is used for data manipulation
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt
import numpy as np
import sys
from sklearn.tree import export_graphviz
import pydot
# Read in data and display first 5 rows
df = pd.read_csv('data/raw/INTC.csv')

#print(df.head())
NUM_PAST_DAYS = 10
for i in range(NUM_PAST_DAYS, len(df)):
    ct = NUM_PAST_DAYS
    for j in range(i-NUM_PAST_DAYS, i):

        df.loc[i, 'prevClose' + str(ct)] = df.loc[j, 'close']
        #df.loc[i, 'prevOpen' + str(ct)] = df.loc[j, 'open']
        #df.loc[i, 'prevHigh' + str(ct)] = df.loc[j, 'high']
        #df.loc[i, 'prevLow' + str(ct)] = df.loc[j, 'low']
        #df.loc[i, 'prevVolume' + str(ct)] = df.loc[j, 'volume']
        ct -= 1

df = df.drop(['timestamp', 'open', 'high', 'low', 'volume'], axis=1)
for k in range(0, NUM_PAST_DAYS):
    df = df.drop(df.index[0]).reset_index(drop=True)


labels = np.array(df['close'])
features = df.drop('close', axis=1)

feature_list = list(features.columns)
print(feature_list)
exit()
features = np.array(features)

train_features, test_features, train_labels, test_labels = train_test_split(features, labels, test_size = 0.25, random_state = 42)
"""
print('Training Features Shape:', train_features.shape)
print('Training Labels Shape:', train_labels.shape)
print('Testing Features Shape:', test_features.shape)
print('Testing Labels Shape:', test_labels.shape)
"""

rf = RandomForestRegressor(n_estimators = 1000)
rf.fit(train_features, train_labels)

predictions = rf.predict(test_features)

errors = abs(predictions - test_labels)

total = 0
correct = 0
l = len(test_features[0])
for i in range(0, len(predictions)):
    total += 1
    todayClose = test_labels[i]
    yesterdayClose = test_features[i][l-5]
    yesterdayVol = test_features[i][l-1]
    if todayClose > yesterdayClose:
        if predictions[i] > yesterdayClose:
            print("C")
            correct+=1
        else:
            print("W")

    elif predictions[i] < yesterdayClose:
        print("C")
        correct+=1
    else:
        print("W")
    print("Actual Close: " + str(todayClose) + " Yesterday Close: " + str(yesterdayClose) + " Prediction: " + str(predictions[i]) + " Yesterday Vol: " + str(yesterdayVol))

    sys.stdout.flush()



print(str(100*(correct/total)))
sys.stdout.flush()
