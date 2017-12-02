import os
import pandas as pd
from dateutil import parser


PRICE_DATA_FILENAME = "../data/sm_price/price_time.csv"
WEATHER_DATA_FILENAME = "../data/SM_forecast_2016.csv"
RESULT_FILENAME = "../data/sm_price/processed_price.csv"



def process_data():
	df_price = pd.read_csv(PRICE_DATA_FILENAME)
	df_price["time"] = pd.to_datetime(df_price["time"])
	df_price = df_price.sort_values(by="time")
	datetime_frame = pd.DatetimeIndex(pd.to_datetime(df_price['time']))
	df_price["hour"] = datetime_frame.hour
	df_price["day"] = datetime_frame.dayofweek
	df_price["month"] = datetime_frame.month

	df_weather = pd.read_csv(WEATHER_DATA_FILENAME)
	df_weather["time"] = pd.to_datetime(df_weather["time"])

	m_price_frame = pd.merge(df_price, df_weather, how='inner', on="time")
	final_columns = ["latitude", "longitude", "precipProbability", "uvIndex"]
	m_price_frame = m_price_frame.drop(final_columns, axis=1)

	return m_price_frame

def main():
	price_frame = process_data()
	price_frame.to_csv(RESULT_FILENAME)

if __name__ == '__main__':
	main()