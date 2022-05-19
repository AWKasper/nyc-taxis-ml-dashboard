from typing import Any
from predicting_rides import linear_prediction
from nyc_taxi_plots import barplot_kosten_pkm, plot_people_per_ride
import pandas as pd

def info_plots():
    import streamlit as st
    import time
    import datetime

    st.pyplot(barplot_kosten_pkm())
    st.plotly_chart(plot_people_per_ride())

    

def ride_prediction():
    import streamlit as st
    import time
    import datetime

    df = pd.read_csv(r'data\processed\weather_data\weather_description.csv')

    options = df['New York'].unique()

    st.set_option('deprecation.showPyplotGlobalUse', False)
  
    st.header('Set the date and time')

    date = st.date_input(
     "Pick a date for prediction")
    time = st.time_input(
        'Pick a time for prediction')

    st.header('Set the weather')
    st.write('The weather will be set automatically by an API if the chosen date and time is within the next five days')

    col1, col2, col3 = st.columns(3)

    weather = col1.selectbox(
        'Choose the kind of weather',
        options=options
    )
    
    temperature = col2.number_input(
        'Temperature in Celsius',
        min_value=-100.0,
        value=0.0,
        max_value=100.0,
        step=0.1
    )

    st.pyplot(linear_prediction(date, time, 0.0,  temperature))


def kmeans():
    import streamlit as st

    import os

    from shapes_mapping import plotting_map
    #Plotting NYC zones
    import pandas as pd
    from sqlalchemy import create_engine
    from sklearn.cluster import KMeans
    import matplotlib.pyplot as plt
    mycwd = os.getcwd()
    engine = create_engine('mysql+mysqlconnector://kaspera1:H1c3VA29xnjPrT@oege.ie.hva.nl/zkaspera1')
    amount_of_data = st.slider('Amount data', 20000, 100000, value=25000)
    df = pd.read_sql(f"SELECT dropoff_longitude, dropoff_latitude FROM uncleaned_NYC_yellowcabs_2015 LIMIT {amount_of_data}", engine)

    df_fixed = df['dropoff_longitude'].between(-74.3,-73.7) & df['dropoff_latitude'].between(40.0,41.0)
    df = df[df_fixed]
    df_num = df.to_numpy()

    kmeans_points = st.slider('kmeans', 0, 50, value=10)

    model = KMeans(n_clusters = kmeans_points)
    model.fit(df_num)
    # print(model.cluster_centers_)

    # get plotting map and scatter cluster points
    p = plotting_map(r'data/processed/taxi_zones/taxi_zones.shp', 'borough')
    p.scatter(df['dropoff_longitude'],df['dropoff_latitude'],alpha=0.05)
    p.scatter(model.cluster_centers_[:,0],model.cluster_centers_[:,1],color='red')

    #Going back to the working directory from before
    os.chdir(fr'{mycwd}')

    st.pyplot(p)
# fmt: on

# Turn off black formatting for this function to present the user with more
# compact code.
# fmt: off


def fractal_demo():
    import streamlit as st
    import numpy as np

    # Interactive Streamlit elements, like these sliders, return their value.
    # This gives you an extremely simple interaction model.
    iterations = st.sidebar.slider("Level of detail", 2, 20, 10, 1)
    separation = st.sidebar.slider("Separation", 0.7, 2.0, 0.7885)

    # Non-interactive elements return a placeholder to their location
    # in the app. Here we're storing progress_bar to update it later.
    progress_bar = st.sidebar.progress(0)

    # These two elements will be filled in later, so we create a placeholder
    # for them using st.empty()
    frame_text = st.sidebar.empty()
    image = st.empty()

    m, n, s = 960, 640, 400
    x = np.linspace(-m / s, m / s, num=m).reshape((1, m))
    y = np.linspace(-n / s, n / s, num=n).reshape((n, 1))

    for frame_num, a in enumerate(np.linspace(0.0, 4 * np.pi, 100)):
        # Here were setting value for these two elements.
        progress_bar.progress(frame_num)
        frame_text.text("Frame %i/100" % (frame_num + 1))

        # Performing some fractal wizardry.
        c = separation * np.exp(1j * a)
        Z = np.tile(x, (n, 1)) + 1j * np.tile(y, (1, m))
        C = np.full((n, m), c)
        M: Any = np.full((n, m), True, dtype=bool)
        N = np.zeros((n, m))

        for i in range(iterations):
            Z[M] = Z[M] * Z[M] + C[M]
            M[np.abs(Z) > 2] = False
            N[M] = i

        # Update the image placeholder by calling the image() function on it.
        image.image(1.0 - (N / N.max()), use_column_width=True)

    # We clear elements by calling empty on them.
    progress_bar.empty()
    frame_text.empty()

    # Streamlit widgets automatically run the script from top to bottom. Since
    # this button is not connected to any other logic, it just causes a plain
    # rerun.
    st.button("Re-run")


# fmt: on

# Turn off black formatting for this function to present the user with more
# compact code.
# fmt: off
def plotting_demo():
    import streamlit as st
    import time
    import numpy as np

    progress_bar = st.sidebar.progress(0)
    status_text = st.sidebar.empty()
    last_rows = np.random.randn(1, 1)
    chart = st.line_chart(last_rows)

    for i in range(1, 101):
        new_rows = last_rows[-1, :] + np.random.randn(5, 1).cumsum(axis=0)
        status_text.text("%i%% Complete" % i)
        chart.add_rows(new_rows)
        progress_bar.progress(i)
        last_rows = new_rows
        time.sleep(0.05)

    progress_bar.empty()

    # Streamlit widgets automatically run the script from top to bottom. Since
    # this button is not connected to any other logic, it just causes a plain
    # rerun.
    st.button("Re-run")


# fmt: on

# Turn off black formatting for this function to present the user with more
# compact code.
# fmt: off
def data_frame_demo():
    import streamlit as st
    import pandas as pd
    import altair as alt

    from urllib.error import URLError

    @st.cache
    def get_UN_data():
        AWS_BUCKET_URL = "http://streamlit-demo-data.s3-us-west-2.amazonaws.com"
        df = pd.read_csv(AWS_BUCKET_URL + "/agri.csv.gz")
        return df.set_index("Region")

    try:
        df = get_UN_data()
        countries = st.multiselect(
            "Choose countries", list(df.index), ["China", "United States of America"]
        )
        if not countries:
            st.error("Please select at least one country.")
        else:
            data = df.loc[countries]
            data /= 1000000.0
            st.write("### Gross Agricultural Production ($B)", data.sort_index())

            data = data.T.reset_index()
            data = pd.melt(data, id_vars=["index"]).rename(
                columns={"index": "year", "value": "Gross Agricultural Product ($B)"}
            )
            chart = (
                alt.Chart(data)
                .mark_area(opacity=0.3)
                .encode(
                    x="year:T",
                    y=alt.Y("Gross Agricultural Product ($B):Q", stack=None),
                    color="Region:N",
                )
            )
            st.altair_chart(chart, use_container_width=True)
    except URLError as e:
        st.error(
            """
            **This demo requires internet access.**
            Connection error: %s
        """
            % e.reason
        )
