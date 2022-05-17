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

dfr['day_of_the_week'] = dfr['tpep_pickup_datetime'].apply(lambda x: x.weekday())

dfr['month_of_the_year'] = dfr['tpep_pickup_datetime'].apply(lambda x: x.strftime(r'%m'))

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

# first one is a simple linear regression of which the results are quite bad

from sklearn.linear_model import LinearRegression, Ridge
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

chunks = pd.read_sql("SELECT * FROM rides_per_day_2015", oege_engine(), chunksize=10000)

model_data = pd.concat(chunks, ignore_index=True)

model_data.dtypes

train = model_data.drop(['count', 'tpep_pickup_datetime'], axis=1)

test = model_data['count']

X_train, X_test, y_train, y_test = train_test_split(train, test, test_size=0.2, random_state=2)

linear_regr = LinearRegression()

linear_regr.fit(X_train, y_train)

pred = linear_regr.predict(X_test)

# The coefficients
print("Coefficients: \n", linear_regr.coef_)
# The mean squared error
print("Mean squared error: %.2f" % mean_squared_error(y_test, pred))
# The coefficient of determination: 1 is perfect prediction
print("Coefficient of determination: %.2f" % r2_score(y_test, pred))

# Plot outputs
fig, ax =plt.subplots(1,2)

sns.stripplot(X_test['time_of_day'], y_test, color="black", ax=ax[0], order=['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23'])
sns.stripplot(X_test['time_of_day'], pred, color="red", linewidth=3, alpha=0.3, ax=ax[1], order=['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23'])

fig.show()

# finding best alpha for linear regression
