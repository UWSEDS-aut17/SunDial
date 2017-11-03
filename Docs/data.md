This document contains information on the data will will use in our project

Requirements
To fufill the aims decribed in the README, we require:
1. Dataset for utility price
2. Dataset for weather (to predict solar generation), and also other weather data to use to model ultility price if dependant on other renewables (rain, wind, etc.)
3. Data on battery (state of health, capacity, etc.)
4. Dataset on energy demand for several "test" installations (residential home, data center, gridscale)

Sources
Google Project Sunroof: https://www.google.com/get/sunroof/data-explorer/

Utility rates database: https://openei.org/apps/USURDB/
https://www.eia.gov/electricity/data.php
https://openei.org/wiki/Utility_Rate_Database

US weather data:
https://www.ncdc.noaa.gov/
(need to extract relevent info from weather data to model solar cell energy output. To do this, combine with Google Project Sunroof)


Battery / Solar data soruces:
- DAWN (Li-ion aging dataset) https://c3.nasa.gov/dashlink/resources/133/
- Another dataset with another chemistry (Redox-flow, etc.)? 
- https://www.energysage.com/solar/solar-energy-storage/what-are-the-best-batteries-for-solar-panels/
- http://energystorage.org/energy-storage/facts-figures
- https://www.energystorageexchange.org


Evaluation
|               | Google Sunroof | OpenAI | NOAA | DAWN |
|:-------------:|:--------------:|:------:|:----:|:----:|
| Utility Price |                |    x   |      |      |
|    Weather    |        x       |        |   x  |      |
|    Battery    |                |        |      |   x  |
| Energy Demand |                |    x   |      |      |
