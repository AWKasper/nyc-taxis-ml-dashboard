import numpy as np
import math
import pandas as pd
import datetime
from datetime import datetime as dt
import time as tm

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

    datetime_unix = dt.combine(date, time)
    
    unix_timestamp = tm.mktime(datetime_unix.timetuple())
    
    found_unix = min(dframe['dt'], key=lambda x:abs(x-unix_timestamp))

    row = dframe.loc[dframe['dt'] == found_unix]

    weather = row['weather']
    tempC = row['main.temp']
    pressure = row['main.pressure']
    humidity = row['main.humidity']
    wind_speed = row['wind.speed']
    wind_deg = row['wind.deg']

    return weather, tempC, pressure, humidity, wind_speed, wind_deg

def linear_prediction(date, time, precipitation, temperature):

    time_of_day = time.strftime(r'%H')
    day = date.weekday()
    month = date.strftime(r'%m')

    loaded_model = pickle.load(open(r'src\models\multi_lin_regr_trained.sav', 'rb'))

    prediction = loaded_model.predict([[temperature, precipitation, day, month, time_of_day]])

    df = pd.DataFrame([[math.ceil(prediction[0]), 'multiple linear regression']], columns=["prediction", 'model'])
    
    # , x=prediction.columns[0]
    g = sns.catplot(data=df, kind='bar', x='model', y='prediction')

    ax = g.facet_axis(0, 0)

    ax.bar_label(ax.containers[0])

    plt.show()
