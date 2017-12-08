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

