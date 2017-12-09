import pandas as pd
from pandas.plotting import scatter_matrix
import matplotlib.pyplot as plt
from sklearn import model_selection
import numpy as np

from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import PolynomialFeatures

#Train 2 models upon import, storage and cycle
#First, train storage model (battery degradation from simply sitting, not from cycling
#need to add test to check presence of these csv files
dataset = pd.read_csv('data/bat_shelf.csv')
dataset[dataset['Cap'] > 1] = 1
dataset = dataset[dataset.Cap != 0]
#Try with adding polynomial features
array = dataset.values
X = array[:,[2,3,6]]
Y = array[:,7]
poly = PolynomialFeatures(2)
X2 = poly.fit_transform(X)
validation_size = 0.20
seed = 7
X2_train, X2_validation, Y_train, Y_validation = model_selection.train_test_split(X2, Y, test_size=validation_size, random_state=seed)
# Create linear regression object
regr = linear_model.LinearRegression()
# Train the model using the training sets
regr.fit(X2_train, Y_train)
# Make predictions using the testing set
Y_pred = regr.predict(X2_validation)
# The coefficients
print('Coefficients: \n', regr.coef_)
# The mean squared error
print("Mean squared error: %.2f"
      % mean_squared_error(Y_validation, Y_pred))
# Explained variance score: 1 is perfect prediction
print('Variance score: %.2f' % r2_score(Y_validation, Y_pred))

#now train model for degradation from cycling
#add test to check for csv
dataset = pd.read_csv('data/bat_cycle.csv')
#Try with adding polynomial features
array = dataset.values
X = array[:,[1,3,4,5]]
Y = array[:,2]
poly = PolynomialFeatures(2)
X2 = poly.fit_transform(X)
validation_size = 0.20
seed = 7
X2_train, X2_validation, Y_train, Y_validation = model_selection.train_test_split(X2, Y, test_size=validation_size, random_state=seed)
# Create linear regression object
regr2 = linear_model.LinearRegression()
# Train the model using the training sets
regr2.fit(X2_train, Y_train)
# Make predictions using the testing set
Y_pred = regr2.predict(X2_validation)
# The coefficients
print('Coefficients: \n', regr.coef_)
# The mean squared error
print("Mean squared error: %.2f"
      % mean_squared_error(Y_validation, Y_pred))
# Explained variance score: 1 is perfect prediction
print('Variance score: %.2f' % r2_score(Y_validation, Y_pred))

#load temperature data to input into battery model
df = pd.read_csv('../data/SM_forecast_2016.csv')
df['temperature'] = (df['temperature'] - 32)*(5/9)
daily_temp = []
for ii in range(365):
    daily_temp.append(df.loc[ii*24:ii*24+24,'temperature'].mean(axis=0))


def bat_shelf(soc,temp,days):
    """Model the degradation from the battery sitting there (not from cycling). inputs 
    are state of charge (soc,%, 0 - 100) which is the state of charge while resting, 
    temperature (temp, C, -40 - 50 C), and days (length of time for case, trained up to 
    150 days, but we will use 30 days then extrapolate degradation to adjust for daily calls)
    """
    #Maybe add some code to check inputs are OK range, etc.
    X = np.array([soc,temp,days])
    poly = PolynomialFeatures(2)
    X4 = poly.fit_transform(X.reshape(1,-1))
    a = regr.predict(X4)
    return a

def bat_cycle(cycles,soc_low,soc_high,rate):
    """Model the degradation from the battery due to cycles. inputs are cycle # (1-800),
    lower limit state of charge of cycle (soc,%, 0 - 40) which is the state of charge prior to charging, 
    upper limit state of charge of cycle (soc,%, 60 - 100) which is the state of charge prior 
    to discharging, and the discharging rate (0.5C - 2C)
    """
    #Maybe add some code to check inputs are OK range, etc.
    X = np.array([cycles,soc_low,soc_high,rate])
    poly = PolynomialFeatures(2)
    X4 = poly.fit_transform(X.reshape(1,-1))
    a = regr2.predict(X4)
    return a
    
def bat_day(soc,temp,cycles,soc_low,soc_high,rate):
    """Model the degradation from the battery in one day
    """
    #Maybe add some code to check inputs are OK range, etc.
    DegCycle = bat_cycle(400,soc_low,soc_high,rate)**(cycles/400)
    DegStore = bat_shelf(soc,temp,60)**(1/60)
    a = DegCycle*DegStore
    return a
    
def bat_day2(soc,temp,cycles,soc_low,soc_high,rate):
    """Model the degradation from the battery in one day
    """
    #Maybe add some code to check inputs are OK range, etc.
    DegCycle = bat_cycle(cycles,soc_low,soc_high,rate)
    DegStore = bat_shelf(soc,temp,60)**(1/60)
    a = DegCycle*DegStore
    return (DegCycle, DegStore)
    
def bat_price_per_hour(energy,hour_start,hour_end,day,bat_cap,bat_cost):
    """
    This function outputs a 24x1 vector with the cost of using the battery for given
    inputs. The basic ideal is to call the degradation model, then multiply the very
    little degradation in each hour by the total cost of the battery.
    Note that for no cycling, there is still a cost due to calander fade.
    Inputs:
    energy [=] MWhr, total energy taken from battery in day
    hour_start [=] 0-23, hour of day to start discharging battery
    hour_end [=] 0-23, hour of day to stop discharging battery
    day [=] 1-365, day of year (to access temperature data for battery model)
    bat_cap [=] MWhr, total capacity of the battery
    bat_cost [=] $, total cost of the battery
    Outputs:
    cost [=] $, 24x1 vector showing the cost of operating the battery.
    """
    cycles = energy / bat_cap
    hours = hour_end - hour_start
    temp = daily_temp[day-1]
    if cycles == 0:
        soc = 0
        deg_store = bat_shelf(soc,temp,60)**(1/60)
        deg_store_hour = deg_store**(1/24)
        cost_per_hour = (-(deg_store_hour-1) / .4) * bat_cost
        cost = np.full((24, 1), cost_per_hour)
    else:
        soc = 0
        soc_low = soc
        soc_high = min(max(cycles*100,60),100)
        rate = min(max(cycles/hours,0.5),2)
        deg_store = bat_shelf(soc,temp,60)**(1/60)
        deg_store_hour = deg_store**(1/24)
        deg_cycle = bat_cycle(cycles,soc_low,soc_high,rate)
        deg_cycle_hour = deg_cycle**(1/hours)
        deg_hour = np.full((24,1), deg_store_hour)
        deg_hour[hour_start:hour_end] = deg_hour[hour_start:hour_end]*deg_cycle_hour
        cost = (-(deg_hour-1) / .4) * bat_cost
    return cost
        
        
    


