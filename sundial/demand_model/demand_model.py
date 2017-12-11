# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

#%% Setup

def get_demand_cph():
    import numpy as np
    import pandas as pd
    from datetime import datetime
    import matplotlib.pyplot as plt
    import seaborn as sns


    demand_file = "/demand/USA_CA_Santa.Maria.Public.AP.723940_TMY3_BASE.csv"
    weather_obs_file = "1124193.csv"
    weather_obs_path = "/weather_obs/"
    data_path = "sundial/data"

    #%% Load Data

    with open(data_path + weather_obs_path + weather_obs_file) as f:
        weather_obs = pd.read_csv(f)

    with open(data_path + demand_file) as f:
        demand = pd.read_csv(f)

    #%% Clean and Join Data

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

    #%% Visualize

    # Plot to see what it looks like first

    fig, ax = plt.subplots(figsize = (15, 10))

    ax.scatter(demand_obs["HLY-TEMP-NORMAL"], demand_obs["Electricity:Facility [kW](Hourly)"])

    sns.jointplot(x = "HLY-TEMP-NORMAL", y = "Electricity:Facility [kW](Hourly)", data = demand_obs, kind = "hex", size = 10)
    sns.jointplot(x = "HLY-DEWP-NORMAL", y = "Electricity:Facility [kW](Hourly)", data = demand_obs, kind = "hex", size = 10)

    fig,ax = plt.subplots(figsize = (15, 10))
    ax.plot(demand_obs["Electricity:Facility [kW](Hourly)"])

    demand_elec = demand_obs["Electricity:Facility [kW](Hourly)"]
    demand_daily = []

    for i in range(362):
        demand_daily.append( sum(demand_elec[i*23:(i+1)*23]) )

    fig,ax = plt.subplots(figsize = (15, 10))
    ax.plot(demand_daily)

    #%% Model

    # Basic model: Average each hour to get an average hourly power consumption

    demand_hourly = [np.NaN]

    for i in range(23):
        demand_hourly.append( np.mean( demand_elec[i:len(demand_elec):23] ) )

    return demand_hourly
