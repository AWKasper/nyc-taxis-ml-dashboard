import numpy as np
import pandas as pd
from datetime import datetime

from src.data.nyc_taxis_oege import oege_engine

import seaborn as sns
import matplotlib.pyplot as plt

# setup of the data that will be used

# firstly getting the amount of trips for every hour

chunks = pd.read_sql("SELECT tpep_pickup_datetime, VendorID FROM uncleaned_NYC_yellowcabs_2015", oege_engine(), chunksize=10000)

df = pd.concat(chunks, ignore_index=True)

df.rename(columns={"VendorID": "count"}, inplace=True)

df.tpep_pickup_datetime = df.tpep_pickup_datetime.apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S').replace(minute=0, second=0))

df = df.groupby('tpep_pickup_datetime', as_index=False).count()

df.to_sql(name='rides_per_day_2015',con=oege_engine(),if_exists='replace',index=False, chunksize=10000)

# secondly getting the weather information per day or hour

dfw = pd.read_csv(r'local\weather_2015.csv')

dfw = dfw[['EST', 'Mean TemperatureC', 'Precipitationmm']].copy()

dfw.EST = dfw.EST.apply(lambda x: datetime.strptime(x, '%Y-%m-%d').date())

data = pd.read_csv(r'local\rides_phour.csv')

data['mean_temperatureC'] = 0.0

data['precipitationmm'] = 0.0

for index, row in data.iterrows():
    date = data['tpep_pickup_datetime'][index]

    temperature = dfw.loc[dfw['EST'] == datetime.strptime(date, '%Y-%m-%d %H:%M:%S').date()]['Mean TemperatureC']
    precipitation = dfw.loc[dfw['EST'] == datetime.strptime(date, '%Y-%m-%d %H:%M:%S').date()]['Precipitationmm']

    data['mean_temperatureC'][index] = float(temperature)
    data['precipitationmm'][index] = float(precipitation)

data.to_sql(name='rides_per_day_2015', con=oege_engine(), if_exists = 'replace', index=False, chunksize=10000)

# next add the time of day, day of the week and the month

chunks = pd.read_sql("SELECT * FROM rides_per_day_2015", oege_engine(), chunksize=10000)

dfr = pd.concat(chunks, ignore_index=True)

dfr['day_of_the_week'] = 'empty'
dfr['month_of_the_year'] = 'empty'
dfr['time_of_day'] = 'empty'

dfr['day_of_the_week'] = dfr['tpep_pickup_datetime'].apply(lambda x: x.strftime('%A'))

dfr['month_of_the_year'] = dfr['tpep_pickup_datetime'].apply(lambda x: x.strftime(r'%b'))

dfr['time_of_day'] = dfr['tpep_pickup_datetime'].apply(lambda x: x.strftime(r'%H'))

dfr.to_sql(name='rides_per_day_2015', con=oege_engine(), if_exists = 'replace', index=False, chunksize=10000)

# now some plots to get a simple view of the data

chunks = pd.read_sql("SELECT * FROM rides_per_day_2015", oege_engine(), chunksize=10000)

dfv = pd.concat(chunks, ignore_index=True)

sns.set_theme(style="ticks")

hue_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

sns.relplot(x='time_of_day', y='count', data=dfv, hue='day_of_the_week', kind="line", palette=sns.color_palette("rocket_r", n_colors=7), ci=None, size="month_of_the_year", hue_order=hue_order, alpha=.7)

plt.show() 

sns.relplot(x='mean_temperatureC', y='count', data=dfv, kind="line", ci=None)

plt.show() 



# training model

