import requests
import json

# gets history for each date in forecasts table. need to avoid duplicates
def getHistory(observation_dates):

	apiKey = # API Key removed
	latLong = # Coordinated removed for privacy
	
	datesList = []
	highsList = []
	lowsList = []
	
	count = 0
	for dates in observation_dates:
		date_to_request = observation_dates[count].replace('-','')
		urlConditions = "http://api.wunderground.com/api/" + apiKey + "/history_" + date_to_request + "/q/" + latLong + ".json"
		responseConditions = requests.get(urlConditions)
		responseConditions = responseConditions.json()


		# extract the history dict
		history = responseConditions['history']

		# extract the date dict
		date = history['date']
		# concatenate year, month, day from date dictionary
		dateStr = str(date['year']) + "-" + str(date['mon']) + "-" + str(date['mday'])
		# append the string to the dates list
		datesList.append(dateStr)
		
		# extract dailysummary list, length of the list is one
		dailySummary = history['dailysummary']
		print(dailySummary)
		# extract the dict form the list
		dailySummary = dailySummary[0]

		# get the high and append to high list
		high = dailySummary['maxtempi']
		highsList.append(high)
		# get the low and append to low list
		low = dailySummary['mintempi']
		lowsList.append(low)
		
		count = count + 1
	return(datesList, highsList, lowsList)












