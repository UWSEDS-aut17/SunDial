# Weather Forecast data

from geopy.geocoders import Nominatim
import utils

# Lets look at the forecast every day at noon
# to decide what to do the next day (starting at midnight).

api_key = '[875f84f827afd16b1e3ec11c7f6a720b]' # YOUR API KEY HERE
start_date = 1451606400 # January 1 2016, UNIX epoch time
time_forecast = 1477915200 # UNIX epoch time

def convert_latlong(address):
	""" Uses geopy to convert address into lat-lng coordinates.
	"""
	geolocator = Nominatim()
	location = geolocator.geocode(address)
	return (location.latitude, location.longitude)

def download_weather_year(api_key, location, fcast):
	days = []
	base_url = 'https://api.darksky.net/forecast'
	lat, lng = convert_latlong(location)
	coords = '{},{}'.format(lat, lng)

	# get a forecast for every day
	for i in range(365):
		print("Downloading day {}.".format(i))
	    json_url = "{}/{}/{},{}/{}/?exclude=currently,minutely,daily,alerts,flags".format(base_url, api_key, lat, lng, fcast)
		print(json_url)
	    forecast_f = utils.get_data(json_url,'json')
	    days.append({'time': time_forecast, 'Name': forecast_f})

		fcast = fcast + 3600*24

	sm_forecast = pd.DataFrame(d)
	sm_forecast.to_csv('SM_forecast_filenames.csv')
	print("Download completed.")

#Salem, OR

#d = []
#for ii in range(365):
#
#    URL_json = 'https://api.darksky.net/forecast/' + DarkSky_key + '/44.9429,-123.0351,' + str(time_forecast) + '?exclude=currently,minutely,daily,alerts,flags'
#    forecast_filename = utils.get_data(URL_json,'json')
#    d.append({'time': time_forecast, 'Name': forecast_filename})
#    time_forecast = time_forecast + 3600*24

#lat, lng = convert_latlong("Salem, Oregon")

#df_Salemforecast_filenames = pd.DataFrame(d)

#df_Salemforecast_filenames.to_csv('Salem_forecast_filenames.csv')
