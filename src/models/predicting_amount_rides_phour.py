import numpy as np
import pandas as pd
from datetime import datetime

from src.data.nyc_taxis_oege import oege_engine

import seaborn as sns
import matplotlib.pyplot as plt

# setup of the data that will be used

# firstly getting the amount of trips for every hour

def amount_trips_phour(dframe):

    df.rename(columns={"VendorID": "count"}, inplace=True)

    df.tpep_pickup_datetime = df.tpep_pickup_datetime.apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S').replace(minute=0, second=0))

    df = df.groupby('tpep_pickup_datetime', as_index=False).count()

    return df

# secondly getting the weather information per day or hour

def weather_phour(dframe):

    dframe = pd.read_csv(r'local\rides_phour.csv')

    dframe = dframe.drop(['mean_temperatureC', 'precipitationmm'], axis=1).copy()

    dfw = pd.read_csv(r'data\processed\weather_data\weather_description.csv')
    dft = pd.read_csv(r'data\processed\weather_data\temperature.csv')
    dfh = pd.read_csv(r'data\processed\weather_data\humidity.csv')
    dfp = pd.read_csv(r'data\processed\weather_data\pressure.csv')
    dfws = pd.read_csv(r'data\processed\weather_data\wind_speed.csv')
    dfwd = pd.read_csv(r'data\processed\weather_data\wind_direction.csv')

    dframe['weather_description'] = 'nan'
    dframe['temperatureC'] = 0.0
    dframe['humidity'] = 0.0
    dframe['pressure'] = 0.0
    dframe['wind_speed'] = 0.0
    dframe['wind_degr'] = 0.0

    for index, row in dframe.iterrows():
        date = dframe['tpep_pickup_datetime'][index]

        dframe['weather_description'][index] = dfw.loc[dfw['datetime'] == date]['New York'].values[0]
        dframe['temperatureC'][index] = round(float(dft.loc[dft['datetime'] == date]['New York'] - 273.15), 2)
        dframe['humidity'][index] = round(float(dfh.loc[dfh['datetime'] == date]['New York']), 2)
        dframe['pressure'][index] = round(float(dfp.loc[dfp['datetime'] == date]['New York']), 2)
        dframe['wind_speed'][index] = round(float(dfws.loc[dfws['datetime'] == date]['New York']), 2)
        dframe['wind_degr'][index] = round(float(dfwd.loc[dfwd['datetime'] == date]['New York']), 2)

    dframe.to_sql(name='rides_per_day_2015',con=oege_engine(),if_exists='replace',index=False, chunksize=10000)


    return dframe

# next add the time of day, day of the week and the month

def add_datetime(dframe):

    chunks = pd.read_sql('SELECT * FROM rides_per_day_2015', con=oege_engine(), chunksize=10000)

    dframe = pd.concat(chunks, ignore_index=True)

    dframe['day_of_the_week'] = 'empty'
    dframe['month_of_the_year'] = 'empty'
    dframe['time_of_day'] = 'empty'

    dframe['day_of_the_week'] = dframe['tpep_pickup_datetime'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S').strftime('%A'))

    dframe['month_of_the_year'] = dframe['tpep_pickup_datetime'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S').strftime(r'%B'))

    dframe['time_of_day'] = dframe['tpep_pickup_datetime'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S').strftime(r'%H'))

    dframe.to_sql(name='rides_per_day_2015',con=oege_engine(),if_exists='replace',index=False, chunksize=10000)

    return dframe

# training model

# first one is a simple linear regression of which the results are not too accurate

from sklearn.linear_model import LinearRegression, Ridge, LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import pickle

chunks = pd.read_sql("SELECT * FROM rides_per_day_2015", oege_engine(), chunksize=10000)

model_data = pd.concat(chunks, ignore_index=True)

model_data.columns.tolist()

from sklearn.preprocessing import OneHotEncoder, StandardScaler

categorical_preprocessor = OneHotEncoder(handle_unknown="ignore")
numerical_preprocessor = StandardScaler()

from sklearn.compose import ColumnTransformer

model_data_cat = model_data[['weather_description', 'day_of_the_week', 'month_of_the_year']].columns.tolist()
model_data_num = model_data.drop(['tpep_pickup_datetime', 'weather_description', 'day_of_the_week', 'month_of_the_year', 'count'], axis=1).columns.tolist()

preprocessor = ColumnTransformer([
    ('one-hot-encoder', categorical_preprocessor, model_data_cat),
    ('standard_scaler', numerical_preprocessor, model_data_num)])

from sklearn.pipeline import make_pipeline

model = make_pipeline(preprocessor, LinearRegression())

train = model_data.drop(['count', 'tpep_pickup_datetime'], axis=1)

test = model_data['count']

X_train, X_test, y_train, y_test = train_test_split(train, test, test_size=0.2, random_state=42)

X_train.head(10)

trained_model = model.fit(X_train, y_train)

pred = trained_model.predict(X_test)

model.score(X_test, y_test)

from sklearn.metrics import mean_absolute_error

mean_absolute_error(y_test, pred)

pickle.dump(trained_model, open(r'src\models\multi_lin_regr_trained.sav', 'wb'))

#get average weather

dfw = pd.read_csv(r'data\processed\weather_data\weather_description.csv')
dft = pd.read_csv(r'data\processed\weather_data\temperature.csv')
dfh = pd.read_csv(r'data\processed\weather_data\humidity.csv')
dfp = pd.read_csv(r'data\processed\weather_data\pressure.csv')
dfws = pd.read_csv(r'data\processed\weather_data\wind_speed.csv')
dfwd = pd.read_csv(r'data\processed\weather_data\wind_direction.csv')

dfw = dfw[['datetime', 'New York']]
dfw.rename({'New York': 'weather'}, axis=1, inplace=True)
dft = dft[['New York']]
dft.rename({'New York': 'temperature'}, axis=1, inplace=True)
dfh = dfh[['New York']]
dfh.rename({'New York': 'humidity'}, axis=1, inplace=True)
dfp = dfp[['New York']]
dfp.rename({'New York': 'pressure'}, axis=1, inplace=True)
dfws = dfws[['New York']]
dfws.rename({'New York': 'wind_speed'}, axis=1, inplace=True)
dfwd = dfwd[['New York']]
dfwd.rename({'New York': 'wind_direction'}, axis=1, inplace=True)

df = pd.concat([dfw, dft, dfh, dfp, dfws, dfwd], axis=1)

df = df.iloc[1: , :]

df['month'] = 'nan'
df['time'] = 00

df['month'] = df['datetime'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S').strftime(r'%B'))

df['time'] = df['datetime'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S').strftime(r'%H'))

df.drop(['datetime'], axis=1, inplace=True)

df.dropna()

dfmean = df.groupby(['month','time'], as_index=False).agg(
                                                    weather = ('weather', lambda x: x.value_counts().index[0]),
                                                    temperature = ('temperature', 'mean'),
                                                    humidity = ('humidity', 'mean'),
                                                    pressure = ('pressure', 'mean'),
                                                    wind_speed = ('wind_speed', 'mean'),
                                                    wind_direction = ('wind_direction', 'mean')
                                                    )

dfmean.tail(10)
dfmean.describe()

dfmean.to_csv(r'data\processed\weather_data\average_weather_2012-2017.csv')
dfmean.to_sql(name='average_weather_2012-2017', con=oege_engine(), if_exists='fail', chunksize=10000, index=False)
