## Component List

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
1. What it does. This should be a high level description of the roles of the component.
2. Name. This should be the name that you use in the component's implementation (e.g., the name of a python class or function).
3. Inputs. Be specific about the data types. For DataFrames, specify the column names and the types of the column values.
4. Outputs. Same consideration as with inputs.
5. How it works (ideally with pseudo code).

### PV output modeling
1. What it does. This should be a high level description of the roles of the component
2. Name:  This should be the name that you use in the component's implementation (e.g., the name of a python class or function).
3. Inputs. Be specific about the data types. For DataFrames, specify the column names and the types of the column values.
4. Outputs. Same consideration as with inputs.
5. How it works (ideally with pseudo code).

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
