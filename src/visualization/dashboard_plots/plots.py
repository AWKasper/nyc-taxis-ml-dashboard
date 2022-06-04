from typing import Any
from dashboard_plots.predicting_rides import rides_prediction, check_weather_range, get_weather_for_date
import pandas as pd
import numpy as np
import os

dfweather_desc = pd.read_csv(r'/app/nyc-taxis-ml-dashboard/data/processed/weather_data/weather_description.csv')

options = dfweather_desc['New York'].drop_duplicates().str.replace(' ', '').unique()
options[2] = 'clearsky'
options = options[1:].copy()

def info_plots():
    import streamlit as st

def ride_prediction():
    import streamlit as st
    import time as tm
    from datetime import datetime

    st.set_option('deprecation.showPyplotGlobalUse', False)
  
    st.header('Set the date and time')

    date = st.date_input(
        "Pick a date for prediction")
    time = st.time_input(
        'Pick a time for prediction')

    st.header('Set the weather')
    st.write('The weather will be set automatically by an openweathermap API if the chosen date and time is within the next five days.\n'
            + 'When a date and time outside of the next five days is chosen, an average from 2012-2017 will be chosen instead.')

    if check_weather_range(date, time):
        weather_list = get_weather_for_date(date, time)

        result = np.where(options == weather_list[0].iloc[0].replace(" ", ""))[0][0]

        do_prediction(date, time, result, weather_list[1], weather_list[2], weather_list[3], weather_list[4], weather_list[5], True)
    else:
        month = date.strftime(r'%B')

        hour = float(time.strftime(r'%H'))

        dfaverage = pd.read_csv(r'data\processed\weather_data\average_weather_2012-2017.csv')

        average_weather = dfaverage.loc[(dfaverage['month'] == month) & (dfaverage['time'] == hour)]

        result = np.where(options == average_weather['weather'].iloc[0].replace(" ", ""))[0][0]

        do_prediction(date, time, result, average_weather['temperature'].iloc[0] - 273.15, average_weather['humidity'].iloc[0],
                        average_weather['pressure'].iloc[0], average_weather['wind_speed'].iloc[0], average_weather['wind_direction'].iloc[0], False)

def do_prediction(date, time, weather_desc, temp, humid, press, spd, dgr, auto):
    import streamlit as st

    col1, col2, col3 = st.columns(3)

    auto_text = "a free version of an openweathermap API" if auto else "the average weather from 2012 to 2017"

    st.markdown('''<span style="color:green">Showing results for {} {}, weather was set with {}</span>.'''.format(date, time, auto_text), unsafe_allow_html=True)

    weather = col1.selectbox(
        'Choose the kind of weather',
        index=int(weather_desc),
        options=options
    )

    temperature = col2.number_input(
        'Temperature in Celsius',
        min_value=-100.0,
        value=float(temp),
        max_value=100.0,
        step=0.1
    )

    humidity = col3.number_input(
        'Humidity',
        min_value=0.0,
        value=float(humid),
        max_value=100.0,
        step=0.1
    )

    pressure = col1.number_input(
        'Pressure',
        min_value=800.0,
        value=float(press),
        max_value=1100.0,
        step=0.1
    )

    wind_spd = col2.number_input(
        'Wind speed',
        min_value=0.0,
        value=float(spd),
        max_value=500.0,
        step=0.1
    )

    wind_dgr = col3.number_input(
        'Degree of the wind',
        min_value=0.0,
        value=float(dgr),
        max_value=360.0,
        step=0.1
    )

    st.pyplot(rides_prediction(date, time, weather, temperature, humidity, pressure, wind_spd, wind_dgr))

def kmeans():
    import streamlit as st
    import dashboard_plots.kmeans_map as km

    amount_of_data = st.sidebar.slider('Amount data', 20000, 100000, value=25000)
    kmeans_points = st.sidebar.slider('kmeans', 0, 50, value=10)
    plot = km.make_kmeans_map_graph(kmeans_points, amount_of_data)

    st.pyplot(plot)
