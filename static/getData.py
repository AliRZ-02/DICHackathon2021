import requests
from scipy.stats import stats, iqr
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def get_data(name = "Default", number = 12345, neededYear = 2021):
    data = requests.get(
        url="https://api.weather.gc.ca/collections/ahccd-annual/items?f=json&properties="
            "temp_mean__temp_moyenne&station_id__id_station=" + str(number))
    jsonData = data.json()
    years = jsonData["features"]
    getInfoList = {}
    for year in years:
        try:
            temp = float(year["properties"]["temp_mean__temp_moyenne"])
            if temp <= 40 and temp >= -40:
                getInfoList[year["properties"]["year__annee"]] = temp
        except:
            pass
    if len(getInfoList) == 0:
        return 0
    X = [(list(getInfoList.keys()))]
    for element in X:
        for elements in element:
            elements = int(elements)
    Y = [(list(getInfoList.values()))]

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
    predictions = model.predict([[neededYear]])
    plt.plot(X2, Y2, 'ro')
    plt.plot(X2, (model.coef_ * X2) + model.intercept_)
    fig = plt.gcf()
    # plt.show()
    plt.savefig("static/"+name, bbox_inches="tight")
    plt.close(fig)
    new = predictions[0][0]
    return round(new, 3)

def get_lat_long(number = 8404343):
    data = requests.get(
        url="https://api.weather.gc.ca/collections/ahccd-annual/items?f=json&properties="
            "temp_mean__temp_moyenne&station_id__id_station=" + str(number))
    jsonData = data.json()
    lat = jsonData["features"][0]["geometry"]["coordinates"][1]
    long = jsonData["features"][0]["geometry"]["coordinates"][0]
    return lat, long

# if __name__ == "__main__":
#     num = get_data("WHITEHORSE", 2202578, 2021)
#     num2 = get_data("VANCOUVER", 1108380, 2021)
