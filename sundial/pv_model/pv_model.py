import numpy as np
import seaborn
import pandas as pd
import datetime
import matplotlib.pyplot as plt
from sklearn.svm import SVR
from sklearn.grid_search import GridSearchCV
from sklearn.externals import joblib
seaborn.set()

# fetching the data
data = pd.read_csv('data/SM_forecast_2016.csv', delimiter=',')
solar = np.loadtxt('data/solar_data_SM_2016.csv', delimiter=',',
                   skiprows=1)

# Declaring the constants

lat = 0.609644              # latitude of the city
decl = -0.40196             # Declination angle
tilt = 0.261799             # Panel tilt
azi = 3.14159               # Azimuth Angle
eff = 0.15                  # Efficiency of the panel

# saved_model = 'finalized_model.pkl'

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

    year1 = 2016
    month1 = 1
    day1 = 1

    year2 = 2016
    month2 = 11
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

# Using the SVM_rbf regressor for anlyzing the data


def SVM_regressor(year3, month3, day3):
    x_train, y_train, x_test, y_test = get_data_split(year3, month3, day3)

    gamma_range = [0.01, 0.001, 0.0001, 0.00001]
    epsilon_range = [x * 0.1 for x in range(0, 1)]
    C_range = (1, 500, 1000)
    tuned_parameters = [{'kernel': ['rbf'], 'C': C_range,
                         'gamma': gamma_range, 'epsilon': epsilon_range}]
    # grid searching for tuned hyperparameter

    svr_rbf = GridSearchCV(SVR(), param_grid=tuned_parameters, verbose=0)
    y_svr = svr_rbf.fit(x_train, y_train).predict(x_test)

    return(svr_rbf)

# saving the SVM_rbf regressor modelfor the test date


def save_model(saved_model):
    svr_rbf_test = SVM_regressor(2016, 12, 1)
    joblib.dump(svr_rbf_test, saved_model)

    return(svr_rbf_test, saved_model)

# Loading the SVM_rbf regressor model for preditions


def load_model(saved_model, year, month, day):
    y_pred = []
    x_train, y_train, x_test, y_test = get_data_split(year, month, day)
    loaded_model = joblib.load(saved_model)
    y_pred_test = loaded_model.predict(x_test)

    for i in range(len(y_pred_test)):
        if i <= 7 or i > 17:
            comp = 0
        else:
            comp = y_pred_test[i]
        y_pred.append(comp)
    y_pred = np.array(y_pred)

    return(y_pred)

# Plotting the predicted data


def plot(saved_model, year, month, day):

    y_pred = load_model(saved_model, year, month, day)
    x_train, y_train, x_test, y_test = get_data_split(year, month, day)
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

# Calling the pv_output model using following function


def pv_output_cph(saved_model, year, month, day):

    y_pred = load_model(saved_model, year, month, day)
    # print(y_pred)
    return (y_pred)


# example running code :
# pv_output_cph('pv_model/finalized_model.pkl', 2016, 12, 15)
