import sqlite3
from datetime import datetime, date, time
import time
from forecast import Forecast, Historic_observations
from Wunder_api import *
from Wunder_api_history import getHistory

conn = sqlite3.connect('C:\\Python_Scripts\\Weather\\forecast.db')

c = conn.cursor()

def create_table(createQuery):
	c.execute(createQuery)


def insert_forecast(forecast):
	with conn:
		c.execute("INSERT INTO forecasts VALUES (:forecast_source, :date_of_forecast, :date, :high, :low)", {'forecast_source' : forecast.forecast_source , 'date_of_forecast' : forecast.date_of_forecast,
		'date' : forecast.date, 'high' : forecast.high, 'low' : forecast.low})
		

def insert_history(historic_observations):
	with conn:
		c.execute("INSERT INTO history VALUES (:observation_source, :date, :high, :low)", {'observation_source' : historic_observations.observation_source , 
		'date' : historic_observations.date, 'high' : historic_observations.high, 'low' : historic_observations.low})
		
def select_forecast_by_date(date):
	c.execute("SELECT * FROM forecasts WHERE date=:date", {'date' : date})
	return c.fetchall()
	
def select_forecasts():
	c.execute("SELECT * FROM forecasts")
	return c.fetchall()
	
def select_historic():
	c.execute("SELECT * FROM history")
	return c.fetchall()

def Join_forecasts_history():
	c.execute("SELECT forecasts.forecast_source, forecasts.date_of_forecast, forecasts.date, forecasts.high, forecasts.low, history.high, history.low FROM forecasts INNER JOIN history ON forecasts.date=history.date;")
	return c.fetchall()
	
# query to create the forecasts table
create_query_forecasts = """CREATE TABLE IF NOT EXISTS forecasts (
				forecast_source TEXT,
				date_of_forecast TEXT,
				date TEXT,
				high REAL,
				low REAL
				)"""

# query to create the history table 				
create_query_history = """CREATE TABLE IF NOT EXISTS history (
				`observation_source` TEXT,
				`date` TEXT,
				`high` REAL,
				`low` REAL
				)"""


# Call create table functions with the SQL queries
create_table(create_query_forecasts)
create_table(create_query_history)

# call getForecast function from Wunder_api.py to get the current 10 day forecast
forecastValues = getForecast()
# unpack the variables from the tuple
dates = forecastValues[0]
highs = forecastValues[1]
lows = forecastValues[2]

# insert all days of the forecast into the forecasts table
count = 0
for days in dates:
	fore = Forecast('Weather Underground', dates[0],dates[count],highs[count],lows[count])
	insert_forecast(fore)
	
	count = count + 1

# This section determines which dates to request from the historic weather API
# by checking the rows in the history table against the rows in the forecasts table	
# also checks date to make sure that it comes before todays date

# select all rows from history table and populate a list with the dates
records_in_historic = select_historic()
# create a list and extract dates from records_in_historic
dates_in_history = []
count = 0
for rows in records_in_historic:
	currentRow = records_in_historic[count]
	dates_in_history.append(currentRow[1])
	count = count + 1

# call select forecasts, returns a list of tuples of all forecasts
all_forecasts = select_forecasts()
# Create a list to hold dates extracted from all_forecasts
historic_dates_to_request = []
# get todays date
todays_date = date.today()

# iterate through the dates from the forecasts table and append the historic_dates_to_request list with the ones that we want
count = 0
for forecasts in all_forecasts:
	current = all_forecasts[count]
	date_from_forecast = current[2]
	# format the date string and create datetime object
	date_from_forecast_format = date_from_forecast.split('-')
	date_from_forecast_format = date(int(date_from_forecast_format[0]),int(date_from_forecast_format[1]),int(date_from_forecast_format[2]))
	# if the date is not already in the history table and it has already occured then add it to the list
	if date_from_forecast not in dates_in_history and date_from_forecast_format < todays_date:
		historic_dates_to_request.append(date_from_forecast)
	count = count + 1
	
# free API key has a request limit of 10 per a minute
# split the list of dates to request into smaller lists
master_date_list = []
subList = []
length = len(historic_dates_to_request)
for i in range(length):
	if len(subList) < 5:
		subList.append(historic_dates_to_request[i])
	else:
		master_date_list.append(subList)
		subList = []
master_date_list.append(subList)
print(master_date_list)	

# iterate through the master_date_list
# pausing for a minute after each iteration to avoid going over the limit
list_length = len(master_date_list)
for lists in range(list_length):
	# call getHistory to get history for dates in master_date_list
	get_history_results = getHistory(master_date_list[lists])
	# unpack the variables
	historic_dates = get_history_results[0]
	historic_highs = get_history_results[1]
	historic_lows = get_history_results[2]
		
	# insert data into historic table
	count = 0
	for days in historic_dates:
		observation = Historic_observations('Weather Underground', historic_dates[count], historic_highs[count], historic_lows[count])
		insert_history(observation)
		count = count + 1
	time.sleep(61)
	

c.close()
conn.close()
