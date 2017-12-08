## SunDial
[![Build Status](https://travis-ci.org/uwescience/shablona.svg?branch=master)](https://travis-ci.org/uwescience/shablona)

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
      |- README.md
      |- SunDial/
         |- __init__.py
         |- optimizer.py
         |- sdutils.py
         |- utils.py
         |- utils_old.py
         |- weatherToCSV.py
         |- data/
            AK_forecast.csv
            README.md
            SM_forecast_2016_2017.csv
            SM_forecast_2016.csv
            |- demand/
               |- USA_CA_Santa.Maria.Public.AP.723940_TMY3_BASE.csv
            |- salem/
               |- Salem_forecast_2016_2017.csv
               |- Salem_forecast_2016.csv
               |- USA_OR_Salem-McNary.Field.726940_TMY3_BASE.csv
            |- weather_obs
               |- 1124193.csv
               |- 1124214.csv
               |- 1124228.csv
               |- 1124410.csv
         |- tests/
            |- ...
      |- doc/
         |- components.md
         |- data.md
         |- functionalspecs.md
         |- update_111217.md
         |- sphinxext/
            |- ...
      |- img/
         |- intro_pic.jpg
         |- model_flowchart_outline.png
      |- setup.py
      |- .travis.yml
      |- .mailmap
      |- appveyor.yml
      |- LICENSE
      |- requirements.txt
      |- ipynb/
         |- Downloading_Data.ipynb
         |- Loading_Data_and_Defining_subtasks.ipynb


In the following sections we will examine these elements one by one. First,
let's consider the core of the project. This is the code inside of
`SunDial/SunDial.py`. The code provided in this file _____.

### Module code

We place the module code in a file called `sundial.py` in directory called
`sundial`. This structure is a bit confusing at first, but it is a simple way
to create a structure where when we type `import sundial as sd` in an
interactive Python session, the classes and functions defined inside of the
`sundial.py` file are available in the `sd` namespace. For this to work, we
need to also create a file in `__init__.py` which contains code that imports
everything in that file into the namespace of the project:

    from .sundial import *

In the module code, we follow the convention that all functions are either
imported from other places, or are defined in lines that precede the lines that
use that function. This helps readability of the code, because you know that if
you see some name, the definition of that name will appear earlier in the file,
either as a function/variable definition, or as an import from some other module
or package.

In the case of the sundial module, the main classes defined at the bottom of
the file make use of some of the functions defined in preceding lines.

### Project Data
* DarkSky API: weather forecasts
* Center for Advanced Life Cycle Engineering (CALCE): battery cycling
* National Oceanic and Atmospheric Administration (NOAA): weather observations
* California Independent System Operator (ISO): renewable energy prices
* National Renewable Energy Laboratory (NREL): solar output
* U.S. Department of Energy, Energy Efficiency and Renewable Energy (EEE): energy demand

### Documentation

Documenting your software is a good idea. Not only as a way to communicate to
others about how to use the software, but also as a way of reminding yourself
what the issues are that you faced, and how you dealt with them, in a few
months/years, when you return to look at the code.

The first step in this direction is to document every function in your module
code. We recommend following the [numpy docstring
standard](https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt),
which specifies in detail the inputs/outputs of every function, and specifies
how to document additional details, such as references to scientific articles,
notes about the mathematics behind the implementation, etc.

This standard also plays well with a system that allows you to create more
comprehensive documentation of your project. Writing such documentation allows
you to provide more elaborate explanations of the decisions you made when you
were developing the software, as well as provide some examples of usage,
explanations of the relevant scientific concepts, and references to the relevant
literature.

To document `shablona` we use the [sphinx documentation
system](http://sphinx-doc.org/). You can follow the instructions on the sphinx
website, and the example [here](http://matplotlib.org/sampledoc/) to set up the
system, but we have also already initialized and commited a skeleton
documentation system in the `docs` directory, that you can build upon.

Sphinx uses a `Makefile` to build different outputs of your documentation. For
example, if you want to generate the HTML rendering of the documentation (web
pages that you can upload to a website to explain the software), you will type:

	make html

This will generate a set of static webpages in the `doc/_build/html`, which you
can then upload to a website of your choice.

Alternatively, [readthedocs.org](https://readthedocs.org) (careful,
*not* readthedocs.**com**) is a service that will run sphinx for you,
and upload the documentation to their website. To use this service,
you will need to register with RTD. After you have done that, you will
need to "import your project" from your github account, through the
RTD web interface. To make things run smoothly, you also will need to
go to the "admin" panel of the project on RTD, and navigate into the
"advanced settings" so that you can tell it that your Python
configuration file is in `doc/conf.py`:

![RTD conf](https://github.com/uwescience/shablona/blob/master/doc/_static/RTD-advanced-conf.png)

 http://shablona.readthedocs.org/en/latest/
