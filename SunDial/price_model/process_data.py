import os
import pandas as pd
from dateutil import parser


DATA_FILENAME = "./price_time.csv"


def main():
	df = pd.read_csv(DATA_FILENAME)

	df["time"] = pd.to_datetime(df["time"])
	df = df.sort_values(by="time")
	datetime_hour = pd.DatetimeIndex(pd.to_datetime(df['time']))
	df["hour"] = datetime_hour.hour

	print(df)

if __name__ == '__main__':
	main()