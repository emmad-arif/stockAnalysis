import operator
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import PolynomialFeatures

data = pd.read_csv("data/raw/SPX.csv")

data['ticks'] = range(0, len(data.index.values))

data['timestamp'] = pd.to_datetime(data['timestamp'])

data = data.reset_index()

filteredData = data[(data['ticks'] <= (len(data) - 5))]

x = filteredData['ticks']
y = filteredData['close']
# transforming the data to include another axis
x = x[:, np.newaxis]
y = y[:, np.newaxis]

polynomial_features= PolynomialFeatures(degree=4)
x_poly = polynomial_features.fit_transform(x)

model = LinearRegression()
model.fit(x_poly, y)
y_poly_pred = model.predict(x_poly)


predictions = model.predict(x_poly)
predictions = pd.DataFrame(data = predictions, index = filteredData.index.values, columns = ['pred'])

joined_df = data.join(predictions, how = 'outer')

fig = plt.figure();
ax = fig.add_subplot(111);
ax.plot(joined_df['timestamp'], joined_df['close'], color = (0,0,0), linewidth = 4, alpha = .9, label = 'Original');
ax.plot(joined_df['timestamp'], joined_df['pred'], color = (1,0,0), label = 'Prediction');
ax.set_title('Close vs Linear Regression')
ax.set_xlabel('Ticks')
ax.set_ylabel('Price')
ax.legend(loc='lower right');

plt.show()
