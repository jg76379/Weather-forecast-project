# Weather-forecast-project
Python project that downloads weather forecasts and historical weather observations and compares them.

** Note: API keys have been removed from the code so if you want to try running it you can request a free API key from Weather Underground https://www.wunderground.com/weather/api/
* I also removed my lat/long coordinates for privacy reasons

- WeatherDB.py is the main file. Handles connecting to the database as well as calling the other functions and classes
- Wunder_api.py contains the functions to access the Weather Underground API and download the weather forecast
- Wunder_api_history.py contains the function to download historical weather observations
- forecast.py contains the Forecast class and Historic_observations class
- compare_forecasts.py this file will handle analyzing and comparing the data. Still a work in progress. 
