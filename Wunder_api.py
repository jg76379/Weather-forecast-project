import requests
import json


def getForecast():
	apiKey = # API KEY Removed

	latLong = # Coordinates removed for privacy

	# Url to request the 10-day forecast from the Wunderground API
	urlForecast = "http://api.wunderground.com/api/" + apiKey + "/forecast10day/q/" + latLong + ".json"

	# Get the forecast page with requests
	responseForecast = requests.get(urlForecast)

	# Convert responseForecast object to Json dictionary 
	responseForecast = responseForecast.json()

	# pull out the forecast dict from the forecast10day dict
	currentForecast = responseForecast['forecast']

	# pull the simple forecast dict out of currentForecast dict
	currentForecast = currentForecast['simpleforecast']

	# pull forecastDay list out of currentForecast dict
	forecastDay = currentForecast['forecastday']

	count = 0

	datesList = []
	highsList = []
	lowsList = []

	for days in forecastDay:
		
		
		current = forecastDay[count]
		
		dateDict = current['date']
		
		year = dateDict['year']

		month = dateDict['month']

		day = dateDict['day']

		date = str(year) + "-" + str(month) + "-" + str(day)
		
		datesList.append(date)
		
		highDict = current['high']
		
		high = highDict['fahrenheit']
		
		highsList.append(high)
		
		lowDict = current['low']
		
		low = lowDict['fahrenheit']
		
		lowsList.append(low)	
		
		count = count + 1
		
	return(datesList, highsList, lowsList)
	

