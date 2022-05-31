from typing import Any
from dashboard_plots.predicting_rides import linear_prediction, check_weather_range, get_weather_for_date
from dashboard_plots.nyc_taxi_plots import barplot_kosten_pkm, plot_people_per_ride
import pandas as pd
import numpy

dfweather_desc = pd.read_csv(r'data\processed\weather_data\weather_description.csv')

options = dfweather_desc['New York'].unique()
options[1] = 'clear sky'
options = options[1:].copy()

def info_plots():
    import streamlit as st

    st.pyplot(barplot_kosten_pkm())
    st.plotly_chart(plot_people_per_ride())

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
    st.write('The weather will be set automatically by an API if the chosen date and time is within the next five days.\n'
            + 'When a date and time outside of the next five days is chosen, an average from 2012-2017 will be chosen instead.')

    col1, col2, col3 = st.columns(3)

    if check_weather_range(date, time):
        weather_list = get_weather_for_date(date, time)

        result = numpy.where(options == weather_list[0].iloc[0])[0][0]

        do_prediction(date, time, result, weather_list[1], weather_list[2], weather_list[3], weather_list[4], weather_list[5], col1, col2, col3)
    else:
        month = date.strftime(r'%B')

        hour = float(time.strftime(r'%H'))

        dfaverage = pd.read_csv(r'data\processed\weather_data\average_weather_2012-2017.csv')

        average_weather = dfaverage.loc[(dfaverage['month'] == month) & (dfaverage['time'] == hour)]

        print(average_weather)

        result = numpy.where(options == average_weather['weather'].iloc[0])[0][0]

        print(result)

        do_prediction(date, time, result, average_weather['temperature'].iloc[0] - 273.15, average_weather['humidity'].iloc[0],
                        average_weather['pressure'].iloc[0], average_weather['wind_speed'].iloc[0], average_weather['wind_direction'].iloc[0], col1, col2, col3)

def do_prediction(date, time, weather_desc, temp, humid, press, spd, dgr, col1, col2, col3):
    import streamlit as st

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
        max_value=10000.0,
        step=0.1
    )

    pressure = col1.number_input(
        'Pressure',
        min_value=-1000.0,
        value=float(press),
        max_value=10000.0,
        step=0.1
    )

    wind_spd = col2.number_input(
        'Wind speed',
        min_value=0.0,
        value=float(spd),
        max_value=1000.0,
        step=0.1
    )

    wind_dgr = col3.number_input(
        'Degree of the wind',
        min_value=0.0,
        value=float(dgr),
        max_value=360.0,
        step=0.1
    )

    st.pyplot(linear_prediction(date, time, weather, temperature, humidity, pressure, wind_spd, wind_dgr))

def kmeans():
    import streamlit as st
    import kmeans_map as km

    amount_of_data = st.sidebar.slider('Amount data', 20000, 100000, value=25000)
    kmeans_points = st.sidebar.slider('kmeans', 0, 50, value=10)
    plot = km.make_kmeans_map_graph(kmeans_points, amount_of_data)

    st.pyplot(plot)
