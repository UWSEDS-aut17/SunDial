from setuptools import setup
import os
from setuptools import find_packages

with open(os.path.join('.', 'README.md')) as file:
    long_description = file.read()


datadir = os.path.join('sundial','data')
datafiles = [(d, [os.path.join(d,f) for f in files])
    for d, folders, files in os.walk(datadir)]

opts = dict(
            name="SunDial",
            version="0.1",
            packages=find_packages(),
            install_requires=['pandas',
                              'sklearn',
                              'numpy',
                              'datetime',
                              'dash',
                              'dash_core_components',
                              'dash_html_components',
                              'plotly',
                              'dash-renderer',
                              'matplotlib',
                              'seaborn'],
            author="Ryan Stoddard, Vardhman Mehta, Casey Pham, Michael Stepanovic, Ruchi Kwatra",
            description="A suite of solar energy cost optimization models",
            long_description=long_description,
            license="MIT",
            keywords="optimization, solar_data_analysis",
            include_package_data=True,
            data_files=datafiles
    )

if __name__ == "__main__":
    setup(**opts)