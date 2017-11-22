# Weather Forecast data

from geopy.geocoders import Nominatim

# Lets look at the forecast every day at noon 
# to decide what to do the next day (starting at midnight).

DarkSky_key = '[875f84f827afd16b1e3ec11c7f6a720b]' # YOUR API KEY HERE
start_date = 1451606400 # 1/1/2016, UNIX epoch time
d = []

def convert_latlong(address):
	geolocator = Nominatim()
	location = geolocator.geocode(address)
	return (location.latitude, location.longitude)

lat, lng = convert_latlong("Salem, Oregon")

for ii in range(365):  
    URL_json = 'https://api.darksky.net/forecast/' + DarkSky_key + '/34.9530,-120.4357,' + str(time_forecast) + '?exclude=currently,minutely,daily,alerts,flags'
    forecast_filename = utils.get_data(URL_json,'json')
    d.append({'time': time_forecast, 'Name': forecast_filename})
    time_forecast = time_forecast + 3600*24

df_SMforecast_filenames = pd.DataFrame(d)

df_SMforecast_filenames.to_csv('SM_forecast_filenames.csv')

#Salem, OR
time_forecast = 1477915200 #UNIX epoch time
d = []
for ii in range(365):
      
    URL_json = 'https://api.darksky.net/forecast/' + DarkSky_key + '/44.9429,-123.0351,' + str(time_forecast) + '?exclude=currently,minutely,daily,alerts,flags'
    forecast_filename = utils.get_data(URL_json,'json')
    d.append({'time': time_forecast, 'Name': forecast_filename})
    time_forecast = time_forecast + 3600*24

df_Salemforecast_filenames = pd.DataFrame(d)

df_Salemforecast_filenames.to_csv('Salem_forecast_filenames.csv')