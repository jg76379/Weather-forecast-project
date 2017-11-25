import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

conn = sqlite3.connect('C:\\Python_Scripts\\Weather\\forecast.db')

c = conn.cursor()

# read sql query into pandas dataframe 
df = pd.read_sql("SELECT forecasts.date_of_forecast, forecasts.date, forecasts.high, forecasts.low, history.high, history.low FROM forecasts INNER JOIN history ON forecasts.date=history.date;", con=conn)

# set column names
df.columns = ['date_of_forecast', 'date', 'forecasted_high', 'forecasted_low', 'actual_high', 'actual_low']

# df.set_index('date', inplace=True)


# Calculate mean absolute percentage error (MAPE)
# MAPE measures the size of error as a percentage
# MAPE is defined by the formula M = 100 * sum((A - F) / (A))
# where A is the actual value and F is the forecasted value
# https://en.wikipedia.org/wiki/Mean_absolute_percentage_error



df['difference'] = abs(df['actual_high'] - df['forecasted_high'])
sumDifference = df['difference'].sum()
sumActuals = df['actual_high'].sum()
mape = (sumDifference / sumActuals) * 100




print('mean absolute percentage error (MAPE): ', round(mape,2), '%')




# df.to_excel('C:\\Python_Scripts\\Weather\\weather.xlsx')
