import numpy as np
import seaborn
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import sys
import os
from sklearn.svm import SVR
from sklearn import neighbors
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.grid_search import GridSearchCV
seaborn.set()

# fetching the data
data = pd.read_csv('sundial/data/SM_forecast_2016.csv', delimiter=',')
solar = np.loadtxt('sundial/data/solar_data_SM_2016.csv', delimiter=',',
                   skiprows=1)

# Declaring the constants

lat = 0.609644              # latitude of the city
decl = -0.40196             # Declination angle
tilt = 0.261799             # Panel tilt
azi = 3.14159               # Azimuth Angle
eff = 0.15                  # Efficiency of the panel

year3 = 2016    # int(sys.argv[1])
month3 = 2      # int(sys.argv[2])
day3 = 7        # int(sys.argv[3])

# cleaning and formatting the weather data


def clean_weather_data(data):
    times = pd.DatetimeIndex(pd.to_datetime(data['time'],
                                            format="%m/%d/%Y %H:%M"))
    data['Date'] = times.date
    data['Hour'] = times.hour
    data['year'] = times.year
    data['month'] = times.month
    data['day'] = times.day
    subset = data[data.year == 2016]

    # Dictionary for the overcast conditions

    """
    {'Windy and Partly Cloudy': 1,
    'Mostly Cloudy': 2,
    'Breezy and Mostly Cloudy': 3,
    'Breezy and Partly Cloudy': 4,
    'Partly Cloudy': 12, 'Clear': 5,
    'Overcast': 6, 'Light Rain': 7,
    'Possible Light Rain': 11,
    'Rain': 9,
    'Breezy': 10,
    'Windy': 8,
    'Heavy Rain': 0,
    'Windy and Mostly Cloudy': 13,
    'Foggy': 14,
    'Breezy and Overcast': 15,
    'Light Rain and Breezy': 16,
    'Rain and Breezy': 17}
    """
    summary_values = list(set(subset["summary"]))
    summary_dict = {value: i for (i, value) in enumerate(summary_values)}
    subset = subset.replace({"summary": summary_dict}).\
        drop(subset.columns[[0, 1, 10, 14]], axis=1).fillna(0.0)
    subset = subset.reindex_axis(['time', 'Date', 'year', 'month', 'day',
                                  'Hour', 'summary', 'precipIntensity',
                                  'precipProbability',
                                  'temperature', 'apparentTemperature',
                                  'dewPoint', 'humidity', 'windSpeed',
                                  'windBearing', 'cloudCover',
                                  'visibility'], axis=1)
    weather = np.array(subset)

    return(weather)

# calculating eletcricty generated


def get_data(solar):

    weather = clean_weather_data(data)
    solar = solar[: weather.shape[0], :]
    elec = []

    for i in range(solar.shape[0]):
        B = (((solar[i, 6] * ((np.sin(decl) * np.sin(lat) * np.cos(tilt)) -
               (np.sin(decl) * np.cos(lat) * np.sin(tilt)*np.cos(azi)) +
               (np.cos(decl) * np.cos(lat) * np.cos(tilt))+(np.cos(decl) *
                                                            np.sin(lat) *
                                                            np.sin(tilt) *
                                                            np.cos(azi)) +
               (np.cos(decl) *
                np.sin(tilt)*np.sin(azi)))) + ((solar[i, 5]) *
                                               ((1.14159-tilt) /
                                               (3.14159)))) * eff*3.6)
        elec.append(B)

    elec = np.vstack(np.array(elec))
    pv_output_array = np.append(weather, elec, axis=1)

    return (pv_output_array)

# getting test-train data


def get_data_split(year3, month3, day3):

    pv_output_array = get_data(solar)

    year1 = pv_output_array[0, 2]
    month1 = pv_output_array[0, 3]
    day1 = pv_output_array[0, 4]

    year2 = pv_output_array[0, 2]
    month2 = month3-1
    day2 = 30

    year4 = year3
    month4 = month3
    day4 = day3

    date_train_start = datetime.date(year1, month1, day1)
    date_train_stop = datetime.date(year2, month2, day2)
    date_test_start = datetime.date(year3, month3, day3)
    date_test_stop = datetime.date(year4, month4, day4)

    train = pv_output_array[(pv_output_array[:, 1] >= (date_train_start)) &
                            (pv_output_array[:, 1] <= date_train_stop) &
                            (pv_output_array[:, 4] >= 0)]
    test = pv_output_array[(pv_output_array[:, 1] >= (date_test_start)) &
                           (pv_output_array[:, 1] <= date_test_stop) &
                           (pv_output_array[:, 4] >= 0)]

    x_train = train[:, 2:-1]
    y_train = train[:, -1]

    x_test = test[:, 2:-1]
    y_test = test[:, -1]

    return (x_train, y_train, x_test, y_test)


def SVM_regressor():
    x_train, y_train, x_test, y_test = get_data_split(year3, month3, day3)

    gamma_range = [0.01, 0.001, 0.0001, 0.00001]
    epsilon_range = [x * 0.1 for x in range(0, 1)]
    C_range = (1, 500, 1000)
    tuned_parameters = [{'kernel': ['rbf'], 'C': C_range,
                         'gamma': gamma_range, 'epsilon': epsilon_range}]

    svr_rbf = GridSearchCV(SVR(), param_grid=tuned_parameters, verbose=0)
    y_svr = svr_rbf.fit(x_train, y_train).predict(x_test)

    return(y_svr)


def KNN_regressor():
    x_train, y_train, x_test, y_test = get_data_split(year3, month3, day3)

    n_neighbors = x_train.shape[1]
    for i, weights in enumerate(['uniform', 'distance']):
        knn = neighbors.KNeighborsRegressor(n_neighbors, weights=weights)

        y_knn = knn.fit(x_train, y_train).predict(x_test)
    return(y_knn)

# choosing the best regressor


def choose_regressor():

    x_train, y_train, x_test, y_test = get_data_split(year3, month3, day3)

    y_svr = SVM_regressor()
    y_knn = KNN_regressor()

    y_pred = np.empty(shape=(y_test.shape[0], 1))

    if (mean_squared_error(y_test, y_svr)) > mean_squared_error(y_test, y_knn):
        y_pred = y_svr

    else:
        y_pred = y_knn

    return(y_pred)


def plot():

    y_pred = choose_regressor()
    x_train, y_train, x_test, y_test = get_data_split(year3, month3, day3)
    x = range(x_test.shape[0])

    plt.plot(x, y_pred, label='predicted')

    plt.legend(loc='upper right')
    plt.xlabel('Time in hours')
    plt.ylabel('pv_ouput in KWh')
    plt.title('pv_output')
    plt.savefig('pv_output.png')
    plt.show(block=True)
    # print(y_pred)
    return(y_pred)


def pv_output_cph():

    y_pred = choose_regressor()

    # print(y_pred)
    return (y_pred)
