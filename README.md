## SunDial
![alt text](img/intro_pic.jpg)

With the costs of solar cells and batteries continuing to decline, solar cell-battery combination systems have become viable options to save on electricity costs while offseting carbon emissions. However, electricity demand, ulility costs, and sunlight avaliability all change dynamically, making it difficult for consumers to optimize their utilization of renewable energy sources.

SunDial is a suite of machine learning models based on weather, utility, and solar cell-battery data to optimize solar battery utilization in a dynamic environment. Our platform will be built to scale for different energy needs, from single family homes to large data centers to county-wide electricity networks. Furthermore, we hope to produce a general economic viablity assessment of solar battery installations in different regions across the United States.

### Creators
* Ruchi Kwatra
* Vardhman Mehta
* Casey Pham
* Mike Stepanovic
* Ryan Stoddard

### Project Organization

SunDial has the following structure:

    SunDial/
      |- LICENSE
      |- README.md
      |- requirements.txt
      |- setup.py
      |- doc/
         |- bat_model.md
         |- components.md
         |- data.md
         |- functionalspecs.md
         |- update_111217.md
      |- examples/
         |- model_usage_example.py
         |- ipynb/
            |- BatPlots.ipynb
            |- Downloading_Data.ipynb
            |- Gaussian_Model.ipynb
            |- KNN_Model.ipynb
            |- Loading_Data_and_Defining_subtasks.ipynb
            |- model_usage_example.ipynb
            |- parse_cycledata.ipynb
            |- parse_storagedata.ipynb
            |- train_cycle.ipynb
            |- train_shelf.ipynb
      |- img/
         |- intro_pic.jpg
         |- model_flowchart_outline.png
         |- price_model_plots/
            |- ...
      |- sundial/
         |- __init__.py
         |- optimizer.py
         |- data/
            |- ...
         |- battery_model/
            |- ...
         |- demand_model/
            |- ...
         |- price_model/
            |- ...
         |- pv_model/
            |- ...
         |- tests/
            |- ...


In the following sections we will examine these elements one by one. First,
let's consider the core of the project. This is the code inside of
`SunDial/SunDial.py`. The code provided in this file _____.

### Module code

Sundial contains submodules for each model. These models are initialized
by importing the `sundial` module, and then their corresponding functions are
available via the command line:

```python
import sundial as sd

tomorrow = "2017-12-14"

sd.battery_model.bat_price_per_hour(tomorrow)
sd.demand_model.get_demand_cph(tomorrow)
```

### Project Data
SunDial was built using six data sources:
* DarkSky API: weather forecasts
* Center for Advanced Life Cycle Engineering (CALCE): battery cycling
* National Oceanic and Atmospheric Administration (NOAA): weather observations
* California Independent System Operator (ISO): renewable energy prices
* National Renewable Energy Laboratory (NREL): solar output
* U.S. Department of Energy, Energy Efficiency and Renewable Energy (EEE): energy demand
