import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import linear_model
from datetime import datetime

class LinearRegression:

    data = pd.read_csv("data/raw/AAPL.csv")



    #data['timestamp'] = pd.to_datetime(data['timestamp'])


    #data = data[(data['ticks'] > (len(data) - 20))]
    #data['ticks'] = range(0, len(data.index.values))
    #filteredData = data[(data['ticks'] <= (len(data) - 6))]

    #filteredData['ticks'] = range(0, len(filteredData.index.values))
    #filteredData = filteredData.reset_index()

    #data = data.append({}, ignore_index=True)
    #data['ticks'] = range(0, len(data.index.values))
    data = data.reset_index()
    #filteredData = data
    #print(data)
    #print(filteredData)

    model = linear_model.LinearRegression().fit(data[["index"]], data[['close']])
    m = model.coef_[0]
    b = model.intercept_

    #print ('y = ', round(m[0],2), 'x + ', round(b[0],2))

    #print[int(30)]])
    #exit()
    predictions = model.predict([[len(data)], [len(data)+1]])

    #print(data[['ticks']])
    #predictions = pd.DataFrame(data = predictions, index = data.index.values, columns = ['pred'])
    print(predictions[0][0], predictions[1][0])
    exit()
    joined_df = data.join(predictions, how = 'outer')
    #print(joined_df)
    #print(predictions[len(predictions)-5:])
    fig = plt.figure();
    ax = fig.add_subplot(111);
    ax.plot(joined_df['timestamp'], joined_df['close'], color = (0,0,0), linewidth = 4, alpha = .9, label = 'Original');
    ax.plot(joined_df['timestamp'], joined_df['pred'], color = (1,0,0), label = 'Prediction');
    ax.set_title('Close vs Linear Regression')
    ax.set_xlabel('Ticks')
    ax.set_ylabel('Price')
    ax.legend(loc='lower right');

    plt.show()
