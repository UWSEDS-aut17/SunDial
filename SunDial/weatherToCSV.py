# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 13:31:21 2017

@author: Casey

This file is to take in JSON weather data and convert it to CSV for easier data
ingestion for the other parts of this project.
"""

import pandas as pd
import json
import os
import datetime

#%%

path = "C:\\Users\\cdpha\\Google Drive\\Classes\\CSE 583 Software Development for Data Scientists\\SunDial\\SunDial\\Data_local\\Weather_Forecast"
os.chdir(path)

#salem_filenames = pd.read_csv("Salem_forecast_filenames.csv")
#sm_filenames = pd.read_csv("SM_forecast_filenames.csv")

#%% Walk over files in directory

for root, dirs, files in os.walk(path):
    
    continue

#%% Get all forecasts, put in list in original json format

forecasts_json = []

for file in files:
    
    with open(file, "r") as f:
        
        forecasts_json.append(json.load(f))
        
#%% Separate Salem and SM

salem_forecasts_json = []
sm_forecasts_json = []

for forecast in forecasts_json:
    
    if forecast["latitude"] == 44.9429:
        salem_forecasts_json.append(forecast)
        
    elif forecast["latitude"] == 34.953:
        sm_forecasts_json.append(forecast)
        
        
#%% Put into dataframe

# Salem
columns = ("latitude", 
           "longitude", 
           "time", 
           "summary", 
           "precipIntensity",
           "precipProbability",
           "temperature",
           "apparentTemperature",
           "dewPoint",
           "humidity",
           "pressure",
           "windSpeed",
           "windBearing",
           "cloudCover",
           "uvIndex",
           "visibility"
           )

keys = columns

end = len(keys)

#%%

with open("salem_forecast.csv", "w+") as out:
    
    c = 0
    
    # Header row
    for key in keys:
        c += 1
        out.write(key)
        
        if c != end:
            out.write(",")
        
    for forecast in salem_forecasts_json:
        
        latitude = forecast["latitude"]
        longitude = forecast["longitude"]
        
        for hour in forecast["hourly"]["data"]:
            
            out.write("\n")
            c = 0
            
            for key in keys:
                
                c += 1
                
                if key == "latitude":
                    out.write(str(latitude))
                    
                elif key == "longitude":
                    out.write(str(longitude))
                
                elif key == "time":
                    time = datetime.datetime.fromtimestamp(int(hour["time"])).strftime('%Y-%m-%d %H:%M:%S')
                    out.write(time)
                
                elif key in hour:
                    out.write(str(hour[key]))
                    
                else:
                    out.write("NaN")
                    
                if c != end:
                        out.write(",")
