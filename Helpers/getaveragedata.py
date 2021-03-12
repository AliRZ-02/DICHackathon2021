import pandas as pd
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn import metrics
import joblib
import numpy as np
import matplotlib.pyplot as plt


data = pd.read_csv('RHData.csv')


def average(data):
    avg = dict()
    sums = 0  # total temp that year
    count = 0  # number of temperatures recorded that year
    prev_year = data.iloc[0][7]  # the year in the first row
    for row in data.itertuples():
        year = row[8]
        temp = row[11]
        if prev_year != year:
            year_avg = sums / count
            avg[prev_year] = year_avg
            prev_year = year
            sums = temp
            count = 1
        elif not np.isnan(temp):  # if the temperature was recorded that day
            sums += temp
            count += 1
    return avg


avg = average(data)
for key in avg:
    print(key, avg[key])


