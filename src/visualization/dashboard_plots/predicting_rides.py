import numpy as np
import math
import pandas as pd
from datetime import datetime as datetime
import calendar

import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression, Ridge
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import pickle

import requests

params = dict(
    lat=40.7128,
    lon=-74.0060,
    appid='8b4b8a258d0247a8fe04aa9e7c5489ad',
)

url = 'http://api.openweathermap.org/data/2.5/forecast?'

def get_weather_3h_interval():
    resp = requests.get(url=url, params=params)

    data = resp.json()

    dfjson = pd.json_normalize(data['list'])

    dfjson = dfjson.drop(['visibility', 'pop', 'main.feels_like', 'main.temp_min', 'main.temp_max', 'main.sea_level','main.temp_kf', 'main.grnd_level', 'clouds.all', 'wind.gust', 'sys.pod', 'rain.3h'], axis=1)

    dfjson['main.temp'] = dfjson['main.temp'].apply(lambda x: x-273.15)

    dfjson['weather'] = dfjson['weather'].apply(lambda x: x[0].get('description'))

    return dfjson

def get_weather_for_date(date, time, dframe=get_weather_3h_interval()):

    datetime_unix = datetime.combine(date, time)
    
    unix_timestamp = calendar.timegm(datetime_unix.utctimetuple())
    
    found_unix = min(dframe['dt'], key=lambda x:abs(x-unix_timestamp))

    row = dframe.loc[dframe['dt'] == found_unix]

    weather = row['weather']
    tempC = row['main.temp']
    pressure = row['main.pressure']
    humidity = row['main.humidity']
    wind_speed = row['wind.speed']
    wind_deg = row['wind.deg']

    return weather, tempC, humidity, pressure, wind_speed, wind_deg

def check_weather_range(date, time, dframe=get_weather_3h_interval()):
    datetime_unix = datetime.combine(date, time)
    
    unix_timestamp = calendar.timegm(datetime_unix.utctimetuple())
    
    return unix_timestamp >= dframe['dt'].iloc[0] -  7200 and unix_timestamp + 10800 <= dframe['dt'].iloc[-1]


def rides_prediction(date, time, weather, temp, humidity, pressure, wind_speed, wind_degr):

    linear_pred_smape = 0.3413018386054954
    logistic_pred_smape = 0.34397898085140044
    ridge_pred_smape = 0.3413065092336175

    time_of_day = time.strftime(r'%H')
    day = date.strftime('%A')
    month = date.strftime(r'%B')

    multi_linear_model = pickle.load(open(r'src\models\multi_lin_regr_trained.sav', 'rb'))
    ridge_model = pickle.load(open(r'src\models\ridge_trained.sav', 'rb'))

    pred_df = pd.DataFrame([[weather, temp, humidity, pressure, wind_speed, wind_degr, day, month, time_of_day]], 
        columns=["weather_description", 'temperatureC', 'humidity', 'pressure', 'wind_speed', 'wind_degr', 'day_of_the_week', 'month_of_the_year', 'time_of_day'])

    lin_prediction = multi_linear_model.predict(pred_df)
    ridge_prediction = ridge_model.predict(pred_df)

    df = pd.DataFrame([
                    [math.ceil(lin_prediction[0]), 'multiple linear regression', linear_pred_smape],
                    [math.ceil(ridge_prediction[0]), 'ridge regression', ridge_pred_smape]
                    ],
                    columns=["prediction", 'model', 'smape'])
    
    g = sns.barplot(data=df, x='model', y='prediction', yerr=df['prediction'] * df['smape'])

    for index, row in df.iterrows():
        g.text(row.name, row.prediction * row.smape, row.prediction,
            color='white', ha='center')

    plt.show()
