import json
import requests
from scipy.stats import stats, iqr
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import time
start_time = time.time()
stationDataRaw = requests.get(url="https://api.weather.gc.ca/collections/climate-stations/items/2100200?f=json")
stationData = stationDataRaw.json()
id = stationData["properties"]["STN_ID"]
startYear = int(stationData["properties"]["FIRST_DATE"].split("-")[0]) + 1
endYear = int(stationData["properties"]["LAST_DATE"].split("-")[0])

# if startYear < 1960:
#     startYear = 1960
# print(id)
# print(startYear)
# print(endYear)
data_dict = {}
for i in range(startYear, endYear):
    sum = 0
    counter = 0
    for j in range(1, 13):
        try:
            dataRaw = requests.get(url="https://api.weather.gc.ca/collections/climate-monthly/items/"
                                + str(id) +"."+ str(i) +"."+ str(j) +"?f=json")
            data = dataRaw.json()
            temp_avg = float(data["properties"]["MEAN_TEMPERATURE"])
            sum = sum + temp_avg
            counter += 1
        except:
            pass
    if counter != 0:
        data_dict[str(i)] = sum / counter

# print(data_dict)
X = [(list(data_dict.keys()))]
for element in X:
    for elements2 in element:
        elements2 = int(elements2)
Y = [(list(data_dict.values()))]

X1 = pd.DataFrame(X, dtype=float).transpose()
Y1 = pd.DataFrame(Y, dtype=float).transpose()

min = np.quantile(Y1, 0.25) - (iqr(Y1))
max = np.quantile(Y1, 0.75) + (iqr(Y1))
newY = []
newX = []
for i in range(0, len(Y1[0])):
    if max > Y1[0][i] > min:
        newY.append(Y1[0][i])
        newX.append(X1[0][i])

newX = [newX]
newY = [newY]
X2 = pd.DataFrame(newX, dtype=float).transpose()
Y2 = pd.DataFrame(newY, dtype=float).transpose()
# print(X2)
# print(Y2)

model = LinearRegression()
model.fit(X2, Y2)
predictions = model.predict([[2021], [2036]])
# print(predictions)
plt.plot(X2, Y2, 'ro')
plt.plot(X2, model.coef_ * X2 + model.intercept_)
plt.savefig('CARCROSS', bbox_inches="tight")
plt.show()

# print("Time: ", (time.time() - start_time))