![alt text](img/intro_pic.jpg)

With the costs of solar cells and batteries continuing to decline, solar cell-battery combination systems have become viable options to save on electricity costs while offseting carbon emissions. However, electricity demand, ulility costs, and sunlight avaliability all change dynamically, making it difficult for consumers to optimize their utilization of renewable energy sources.

SunDial is a suite of machine learning models based on weather, utility, and solar cell-battery data to optimize solar battery utilization in a dynamic environment. Our platform will be built to scale for different energy needs, from single family homes to large data centers to county-wide electricity networks. Furthermore, we hope to produce a general economic viablity assessment of solar battery installations in different regions across the United States.

A small demonstration of our final product:

<a href="https://imgflip.com/gif/210n11"><img src="https://i.imgflip.com/210n11.gif" title="made at imgflip.com"/></a>

UI demo link: https://www.youtube.com/watch?v=k8rrkSn-Hzk&feature=youtu.be
### Creators
* Ruchi Kwatra
* Vardhman Mehta
* Casey Pham
* Mike Stepanovic
* Ryan Stoddard

### Project Organization

SunDial has the following structure:

    SunDial/
      |- app.py
      |- LICENSE
      |- README.md
      |- requirements.txt
      |- setup.py
      |- doc/
         |- components.md
         |- data.md
         |- functionalspecs.md
         |- ...
      |- examples/
         |- model_usage_example.py
         |- ipynb/
            |- ...
      |- img/
         |- ...
      |- sundial/
         |- __init__.py
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



### Module code

SunDial has two user modes: a quickstart dashboard mode, and a command-line mode. All functionality can be accessed using `app.py`:

```
python setup.py install
```

```
python app.py
```

At the command line, SunDial contains submodules for each model. These models are initialized
by importing the `sundial` module, and then their corresponding functions are
available via the command line. Requirements can be installed from `setup.py`.

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
