import pandas as pd
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn import metrics
import joblib
import numpy as np
import matplotlib.pyplot as plt

data = pd.read_csv('RHAVGDATA.csv')
# Input Data
X = data[['YEAR']]
# Output Data
Y = data[['AVG']]
X_train,X_test, y_train, y_test = train_test_split(X,Y,test_size=0.2)
print(X_train)

# Train
model = LinearRegression()
model.fit(X_train, y_train)
predictions = model.predict(X_test)
data.plot(x="YEAR", y="AVG", style="o")
plt.show()

print("Root Mean Squared Error: ", np.sqrt(metrics.mean_squared_error(y_test,predictions)))

print('Coefficients: \n', model.coef_)
print('Coefficients: \n', model.intercept_)