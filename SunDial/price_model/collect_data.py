import os
import pandas as pd
from bs4 import BeautifulSoup


DATA_FOLDER = "../data/Energy_Price"
RESULT_FILENAME = "./price_time.csv"


def load_xml(data_file):
 	print(data_file)
	with open(data_file, 'r') as src:
		soup = BeautifulSoup(src, 'lxml')
	return soup


def get_dataframes(data_files):
	dframe = pd.DataFrame(columns=["lmp_value", "time"])
	for data_file in data_files:
		soup = load_xml(os.path.join(DATA_FOLDER, data_file))
		data_list = []
		for i in soup.findChildren("report_data"):
			if i.data_item.text != "LMP_PRC": continue
			element_dict = {
				"lmp_value": i.value.text,
				"time": i.interval_start_gmt.text
			}
			data_list.append(element_dict)
		dframe = dframe.append(pd.DataFrame(data_list))
	dframe = dframe.set_index("time")
	return dframe


def main():
	data_files = []
	for file in os.listdir(DATA_FOLDER):
		if not file.endswith(".xml"): continue
		data_files.append(file)
	
	df = get_dataframes(data_files)
	df.to_csv(RESULT_FILENAME)

if __name__ == '__main__':
	main()