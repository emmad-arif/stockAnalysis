# Pandas is used for data manipulation
import pandas as pd
import numpy as np
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt
import numpy as np
import sys
from sklearn.tree import export_graphviz
import pydot
import datetime

# Read in data and display first 5 rows
df = pd.read_csv('data/raw/SPY.csv')
#print(df.head())

for i in range(1, len(df)):
    if (df.iloc[i]['close'] >= df.iloc[i-1]['close']):
        df.loc[i, 'dir'] = 1
    else:
        df.loc[i, 'dir'] = -1



#for k in range(0, NUM_PAST_DAYS):
#    df = df.drop(df.index[0]).reset_index(drop=True)
PAST_DAYS = 20

for j in range(1, PAST_DAYS+1):
    df['dir' + str(j)] = df.dir.shift(j)
    """
    df['prevRSI5' + str(j)] = df.rsi5.shift(j)
    df['prevSMA5' + str(j)] = df.sma5.shift(j)
    df['prevEMA5' + str(j)] = df.ema5.shift(j)
    df['prevSMA100' + str(j)] = df.sma100.shift(j)
    """
df = df.drop(['timestamp', 'open', 'high', 'low', 'volume', 'close'], axis=1)

df = df.dropna()
#print(df.head())
#exit()
labels = np.array(df['dir'])
features = df.drop('dir', axis=1)

feature_list = list(features.columns)
features = np.array(features)
#print(feature_list)
#exit()
train_features, test_features, train_labels, test_labels = train_test_split(features, labels, test_size = 0.2, shuffle=False)
"""
print("TRAIN FEATURES")
print(train_features)
print("TEST FEATURES")

print(test_features)
print("TRAIN LABELS")

print(train_labels)
print("TEST LABELS")

print(test_labels)
"""
rf = RandomForestRegressor(n_estimators = 1000)

rf.fit(train_features, train_labels)

predictions = rf.predict(test_features)

total = 0
correct = 0
l = len(test_features[0])
for i in range(0, len(predictions)):
    if predictions[i] < 0:
        predictions[i] = -1
    else:
        predictions[i] = 1
    total+=1
    if predictions[i] == test_labels[i]:
        correct+=1
    #    print("C")

    #else:
    #    print("W")
    print( "pred: " + str(predictions[i]) + " Actual: " + str(test_labels[i]))
    sys.stdout.flush()




print(str(100*(correct/total)))
sys.stdout.flush()

# Get numerical feature importances
importances = list(rf.feature_importances_)
# List of tuples with variable and importance
feature_importances = [(feature, round(importance, 2)) for feature, importance in zip(feature_list, importances)]
# Sort the feature importances by most important first
feature_importances = sorted(feature_importances, key = lambda x: x[1], reverse = True)
# Print out the feature and importances
[print('Variable: {:20} Importance: {}'.format(*pair)) for pair in feature_importances];
