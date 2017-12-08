# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

#%% Setup

import pandas as pd
from sklearn import linear_model
from datetime import datetime

demand_file = "USA_CA_Santa.Maria.Public.AP.723940_TMY3_BASE.csv"
weather_obs_file = "1124193.csv"
weather_obs_path = "\\Weather_Observations\\"
data_path = "C:\\Users\\cdpha\\Google Drive\\Classes\\CSE 583 Software Development for Data Scientists\\SunDial\\SunDial\\data"

#%% Load Data

with open(data_path + weather_obs_path + weather_obs_file) as f:
    weather_obs = pd.read_csv(f)

with open(data_path + "\\demand\\" + demand_file) as f:
    demand = pd.read_csv(f)

#%% Clean and Join Data

#salem_obs = [obs for obs in weather_obs if obs.NAME == "SALEM MCNARY FIELD, OR US"]
    
sm_obs = weather_obs[weather_obs.NAME == "SANTA MARIA PUBLIC AIRPORT, CA US"]

sm_datetime = [datetime.strptime(time, "%m-%dT%H:%M:%S") for time in sm_obs["DATE"]]


# Clean demand Date/Time

demand_clean = pd.DataFrame(columns = list(demand.columns.values))

for i in range(len(demand)):
    if demand.loc[i]["Date/Time"][8:10] != "24":
        demand_clean.loc[i] = demand.loc[i]

demand_datetime = [datetime.strptime(time, " %m/%d  %H:%M:%S") for time in demand_clean["Date/Time"]]

# Add DateTime to each dataset

sm_obs["DateTime"] = sm_datetime
demand_clean["DateTime"] = demand_datetime


# Merge weather obs and demand data

demand_obs = demand_clean.merge(sm_obs, on = "DateTime")

columns = list(demand_obs.columns.values)
print(columns)

#%% Model

# Lasso

reg = linear_model.Lasso(alpha = 0.1)
reg.fit(demand_obs["Electricity:Facility [kW](Hourly)"], demand_obs["HLY-TEMP-NORMAL"])








