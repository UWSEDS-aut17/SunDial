﻿## Component List

- Energy price modeling
- Energy Demand modeling
- PV output modeling
- Battery State of Health modeling
- Optimization Procedure

### Energy price modeling
1. Models the energy and price relationship over time
	* Uses the past energy prices over time for each location.
	* Uses the past weather forecast for the location.
	* Uses the future forecasts along with the above mentioned features to build a model to predict price of energy for the next day.
2. `EnergyPriceModel`
3. Inputs: Energy-Price data from CA ISO and Weather forecast data from darksky
	* Enery-Price data will be used to consider Locational Marginal Prices (LMP) over an hour with units [$/MWh]
	* Weather forecast data would provide columns like temperature [˚C] & future_forecast [hourly ˚C] 
4. Prices for energy over time [$/MWh]
5. Gather appropriate features from the datasets in a dataframe and make splits for train and test data. Train the model and validate the model by testing it using the test data. Save this model and predict prices given the future forecast and previous energy prices.

### Energy Demand modeling
1. What it does: This component looks at energy demand and correlates/groups it with weather observations to determine patterns in demand (ie higher demand when hot/cold).
2. Name: energy_demand
3. Inputs: 
	* Energy demand data
	* Weather observations (temperature, cloud cover)
4. Outputs:
	* Energy demand correlation with various weather conditions
5. How it works:
	* Energy demand with timestamps loaded
	* Weather observations with timestamps loaded
	* Matching of energy demand and weather observations to, at minimum, the day. Ideally by 12-hour, 1-hour periods best.
	* Determining correlation of energy demand to various temperature ranges
		* With hot (ie >59F or >15C)
		* With cold (ie <41F or <5C)
	* Determining correlation of energy demand to cloud cover

### PV output modeling
1. What it does: This component of the model has two tier calculations: a) First, it integrates the weather data and the solar data to predict effective solar insolation per square meter received by solar panels.
b) Next, it consolidates photo-voltaic (solar panels) data and effective solar irradiance data (per squared meter) to calculate the gross electricty generated per squared meter from solar panels.

2. Name:  pv_output
3. Inputs. Input data would be in dataframes with columns as Zenith angle (degrees), Azimuth angle(degrees), latitude of location(degrees), Air Mass, cloud cover(%), Time of the day(24-Hours format), Day of the year(mmddyyyy), module tilt(degrees), efficiency of the panel(%), Area of the panels(sq.m)
4. Outputs. Output data would be electricity generated per squared meter of panels (KWh/sq.m) and total electricity generated from the installation(KWh)
5. For the entered time and day and angle tilt of solar panels
-- check previous years' weather data for the particular date and time and solar data as per angles and latitude 
-- predicts future solar insolation
-- calculates gross electricity generation from the panels as per entered tilt of panels

### Battery State of Health modeling
1. What it does: The battery model calculates expected degradation of the battery due to a) time and b) cycles, and relates this degradation to cost. Thus, each battery cycle will have a "cost penalty" due to the impact of that cycle on degradation
2. Name: BatterySOH
3. Inputs: Input data to predict the battery State of Health (SOH). SOH is a %, where 100% is new battery performic at specified capacity and 0% is the battery is done. Input data columns include Battery age, battery age * Temperature, past cycle information (Energy vs. time), proposed future cycle information
4. Outputs: Battery SOH [%], Battery Capacity [MWhr], Economics [$ net present value]
5. How it works (ideally with pseudo code): Battery degradation is a function of a) time+environment and b) past cycle history. For simplicity, we will use some battery models developed by NREL rather than training our own (which is a very complex problem).

### Optimization Procedure
#### What it does. 
Given the output of the other models, this is where a decision is made on how to operate the photovoltaic battery asset each hour for the next 24 hours.

#### Name. This should be the name that you use in the component's implementation (e.g., the name of a python class or function).
def optimize_asset(price, demand, pvoutput, batterysoh)

#### Inputs. Be specific about the data types. For DataFrames, specify the column names and the types of the column values.
Because this phase involves the end user, the input data will include what type of battery asset being used (string) and the date (coerced into DateTime).

#### Outputs. Same consideration as with inputs.
The output will be DataFrame of shape (24, 3). The column "PV" indicates whether the solar cell should be used to charge the battery or supply current energy load (string), the column "battery" indicates to what extent the battery is charging or discharging (float), and the column "utility" indicates how much power is being bought or sold from the power grid (float).

#### How it works (ideally with pseudo code).
Consider the following system:
utility ---x1---> how much energy I require 
PV ----x2----> how much energy I require
battery ----x3---> how energy I require

PV -----x4-----> how much energy is charging the battery
PV -----x5----> how much energy is being discharged from the battery
battery ----x6---> how much energy is being discharged from the battery

Find optimum x's given constraints: x1 + x2 + x3 = load | x2 + x4 + x5 = PV generation | battery has constraints (capacity, charge/discharge rate)
This subtask requires at least preliminary progress on other subtasks to function.

The end goal is to compare our optimization solution (in terms of cost) to "human-input" procedures. Three relevent human-input procedures to compare against:
1. No battery (x4, x6, x3) = 0
2. Charge / discharge based on fixed schedule (discharge every day at xx PM)
3. Discharge battery when price exceeds XX $/MWh

One of the final outputs of the project is comparing the cost of powering a load with our optimum vs. the #1, #2, and #3 scenarios.