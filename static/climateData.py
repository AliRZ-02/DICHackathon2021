import json
import requests
from scipy.stats import stats, iqr
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def climate_data(name = "Default", number = 2100200, year = 2021):
    try:
        stationDataRaw = requests.get(url="https://api.weather.gc.ca/collections"
                                      "/climate-stations/items/"+number+"?f=json")
        stationData = stationDataRaw.json()
        id = stationData["properties"]["STN_ID"]
        startYear = int(stationData["properties"]["FIRST_DATE"].split("-")[0]) + 1
        endYear = int(stationData["properties"]["LAST_DATE"].split("-")[0])
        if startYear < 1960:
            startYear = 1960
    except:
        print("Here JSON ERROR")
        return -900

    print(id)
    data_dict = {}
    for i in range(startYear, endYear):
        sum = 0
        counter = 0
        for j in range(1, 13, 3):
            try:
                dataRaw = requests.get(url="https://api.weather.gc.ca/collections/climate-monthly/items/"
                                           + str(id) + "." + str(i) + "." + str(j) + "?f=json")
                data = dataRaw.json()
                temp_avg = float(data["properties"]["MEAN_TEMPERATURE"])
                sum = sum + temp_avg
                counter += 1
            except:
                pass
        if counter != 0:
            data_dict[str(i)] = sum / counter

    if len(data_dict) == 0:
        print("empty")
        return -900
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

    model = LinearRegression()
    model.fit(X2, Y2)
    predictions = model.predict([[year]])
    plt.plot(X2, Y2, 'ro')
    plt.plot(X2, model.coef_ * X2 + model.intercept_)
    fig = plt.gcf()
    plt.savefig(name, bbox_inches="tight")
    plt.close(fig)
    return round(predictions[0][0], 3)


def get_lat_long(number = 8404343):
    data = requests.get(
        url="https://api.weather.gc.ca/collections"
            "/climate-stations/items/" + number + "?f=json")
    jsonData = data.json()
    lat = jsonData["geometry"]["coordinates"][1]
    long = jsonData["geometry"]["coordinates"][0]
    return lat, long
