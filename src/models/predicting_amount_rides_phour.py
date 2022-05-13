import numpy as np
import pandas as pd
from datetime import datetime

from src.data.nyc_taxis_oege import oege_engine

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

# next add the day of the week and the month

