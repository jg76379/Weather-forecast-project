class Forecast:
	"""A class to create forecasts"""
	
	def __init__(self, forecast_source, date_of_forecast, date, high, low):
		self.forecast_source = forecast_source
		self.date_of_forecast = date_of_forecast
		self.date = date
		self.high = high
		self.low = low

		
class Historic_observations:
	"""A class to create historic obersvations"""
	
	def __init__(self, observation_source, date, high, low):
		self.observation_source = observation_source
		self.date = date
		self.high = high
		self.low = low