import os
import pandas as pd
from dateutil import parser

PRICE_DATA_FILENAME = "../data/sm_price/price_time.csv"
WEATHER_DATA_FILENAME = "../data/SM_forecast_2016.csv"
RESULT_FILENAME = "../data/sm_price/processed_price.csv"

"""
{'Windy and Partly Cloudy': 1,
'Mostly Cloudy': 2,
'Breezy and Mostly Cloudy': 3,
'Breezy and Partly Cloudy': 4,
'Partly Cloudy': 12, 'Clear': 5,
'Overcast': 6, 'Light Rain': 7,
'Possible Light Rain': 11,
'Rain': 9,
'Breezy': 10,
'Windy': 8,
'Heavy Rain': 0,
'Windy and Mostly Cloudy': 13,
'Foggy': 14,
'Breezy and Overcast': 15,
'Light Rain and Breezy': 16,
'Rain and Breezy': 17}
"""


def process_data():
    """
    Joins the weather and price data.
    removes unwanted columns and formats the df to remove all nan
    returns a numpy array with values from the processed dataframe
    """
    df_price = pd.read_csv(PRICE_DATA_FILENAME)
    df_price["time"] = pd.to_datetime(df_price["time"])
    df_price = df_price.sort_values(by="time")

    col_titles = ["lmp_value", "time"]
    df_price = df_price.reindex(columns=col_titles)
    datetime_frame = pd.DatetimeIndex(pd.to_datetime(df_price['time']))
    df_price["hour"] = datetime_frame.hour
    df_price["day"] = datetime_frame.dayofweek
    df_price["month"] = datetime_frame.month

    df_weather = pd.read_csv(WEATHER_DATA_FILENAME)
    df_weather["time"] = pd.to_datetime(df_weather["time"])

    m_price_frame = pd.merge(df_price, df_weather, how='inner', on="time")
    drop_columns = ["latitude", "longitude", "uvIndex"]
    m_price_frame = m_price_frame.drop(drop_columns, axis=1)

    # remap values of summary to a known dictionary list
    summary_values = list(set(m_price_frame["summary"]))
    summary_dict = {value: i for (i, value) in enumerate(summary_values)}
    m_price_frame = m_price_frame.replace({"summary": summary_dict})

    # convert all nan to 0 
    # (not sure if this is the right thing for cloud cover)
    m_price_frame = m_price_frame.fillna(0.0)

    # m_price_frame.to_csv(RESULT_FILENAME)
    return m_price_frame


def get_date_range(df_price_frame, train_start, train_end, test_start,
                   test_end):
    """
    gets the data for the give date range. Used for parameter tuning
    """
    train_mask = (df_price_frame.index > train_start) &\
        (df_price_frame.index < train_end) & (df_price_frame["hour"] >= 0)
    test_mask = (df_price_frame.index > test_start) &\
        (df_price_frame.index < test_end) & (df_price_frame["hour"] >= 0)

    price_train = df_price_frame.loc[train_mask].dropna()
    price_test = df_price_frame.loc[test_mask].dropna()

    XX_price_train = price_train.drop('lmp_value', axis=1).reset_index().\
        drop('time', axis=1)
    XX_price_test = price_test.drop('lmp_value', axis=1).reset_index().\
        drop('time', axis=1)

    YY_price_train = price_train['lmp_value']
    YY_price_test = price_test['lmp_value']

    return XX_price_train, YY_price_train, XX_price_test, YY_price_test


def main():
    process_data()


if __name__ == '__main__':
    main()
