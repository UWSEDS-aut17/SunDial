from sundial.bat_model import bat_model
from sundial.price_model import price_model
import numpy as np

#This example shows how to call battery model to predict degradation price per hour
#for the next 24 hours given some inputs

"""The bat_price_per_hour function outputs a 24x1 vector with the cost of using the battery
for given inputs. The basic ideal is to call the degradation model, then multiply the very
little degradation in each hour by the total cost of the battery.
Note that for no cycling, there is still a cost due to calander fade.

Inputs:
energy [=] kWhr, total energy taken from battery in day
hour_start [=] 0-24, hour of day to start discharging battery
hour_end [=] 0-24, hour of day to stop discharging battery
day [=] 1-365, day of year (to access temperature data for battery model)
bat_cap [=] kWhr, total capacity of the battery
bat_cost [=] $, total cost of the battery

Outputs:
cost [=] $, 24x1 vector showing the cost of operating the battery.
"""

#Note: scale battery capacity to be relevant to demand scale used.
#Try using 0.3-0.5 x typically daily energy demand
#For example, for a single family house, typically daily demand is ~30 kWhr,
#use a 13.5 kWhr battery

energy = 8 #kWhr
hour_start = 18 #6pm, sun goes down
hour_end = 22 #10pm, this means battery stops at 10:00pm, not 10:59
day = 343 #Dec 9th
bat_cap = 13.5 #kWhr
bat_cost = 222*bat_cap # $ - cost scales with capacity, adjust to make relavent if needed

cost_per_hour = bat_model.bat_price_per_hour(energy,hour_start,hour_end,day,bat_cap,bat_cost)
cost_per_hour = np.squeeze(cost_per_hour)
print(cost_per_hour)


"""
Price model usage
provide date and model name from ["SVM_rbf", "KNN", "Linear"]
"""
epm = price_model.EnergyPriceModel()
price_per_hour = epm.test_model("2016-12-08", "SVM_rbf")
print(price_per_hour)
