This document contains information on the data will will use in our project

Requirements
To fufill the aims decribed in the README, we require:
1. Dataset for utility price
2. Dataset for weather (to predict solar generation), and also other weather data to use to model ultility price if dependant on other renewables (rain, wind, etc.)
3. Data on battery (state of health, capacity, etc.)
4. Dataset on energy demand for several "test" installations (residential home, data center, gridscale)
5. Dataset on Solar cell output (solar irradiance vs. time)

Sources
Utility rates database: http://www.caiso.com/Pages/default.aspx

US weather data:
-Dark Sky Forecasts: https://darksky.net/dev
-Observed weather data: https://www.ncdc.noaa.gov/

US DOE:
-Energy Demand Data

Solar Irradiance Data:
-NREL : http://rredc.nrel.gov/solar/old_data/nsrdb/

Battery / Solar data soruces:
- Li-ion battery cycle data - http://www.calce.umd.edu/batteries/data.htm



Evaluation
|                     | DarkSky | Cal-ISO | NREL | CALCE | DOE |
|---------------------|---------|---------|------|-------|-----|
| Weather Forecast    |    x    |         |      |       |     |
| Energy Price        |         |    x    |      |       |     |
| Energy Demand       |         |         |      |       |  x  |
| Solar Irradiance    |         |         |   x  |       |     |
| Battery Degradation |         |         |      |   x   |     |

