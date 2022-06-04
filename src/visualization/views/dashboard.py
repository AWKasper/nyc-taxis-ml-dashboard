import inspect
import textwrap
from collections import OrderedDict

import streamlit as st
from streamlit.logger import get_logger
import dashboard_plots.plots as plots

#Deleting watermark

LOGGER = get_logger(__name__)

# Dictionary of
# demo_name -> (demo_function, demo_description)
PLOTS = OrderedDict(
    [   
        (
            #Name of the plot
            "Predict amount of rides for time of day",
            (
                #Plot function in plots.py
                plots.ride_prediction,
                #Additional information
                """
                On this page you can get a prediction for the amount of rides there will be within a certain hour.
                """,
            ),
        ),
        (
            #Name of the plot
            "Info Plot",
            (
                #Plot function in plots.py
                plots.info_plots,
                #Additional information
                """
                Extra Info.
                """,
            ),
        ),  
        (
            #Name of the Plot
            "Kmeans",
            (
                #Plot function in plots.py
                plots.kmeans,
                #Additional information
                """Blue dots signify a pickup point, the greater the intensity the more saturated the location.
                Red dots indicate centers of the clusters of points. The amount of red dots can be set with the slider on the left.""",
            ),
        ),
    ]
)


def load_view():

    plot_name = st.sidebar.selectbox("Choose a plot", list(PLOTS.keys()), 0)
    current_plot = PLOTS[plot_name][0]


    st.markdown("# %s" % plot_name)

    #Add description if it exists.
    description = PLOTS[plot_name][1]
    if description:
        st.write(description)

    #Clear
    for i in range(10):
        st.empty()


    current_plot()

if __name__ == "__main__":
    load_view()
