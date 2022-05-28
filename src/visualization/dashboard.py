import inspect
import textwrap
from collections import OrderedDict

import streamlit as st
from streamlit.logger import get_logger
import plots

st.set_page_config(
    layout="wide",
    initial_sidebar_state="expanded"
)

#Deleting watermark
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {width: 0 !important; height: 0 !important;}

            .block-container {
                max-width: 1000px;
            }
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

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
                On this page you get to see a prediction of the amount of rides there will be within a certain hour
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
                """
                Extra Info.
                """,
            ),
        ),
    ]
)


def run():

    home = st.button('Home1')
    
    #the navigation buttons in the header
    header = """
        <div data-stale="false" width="829" class="element-container css-1apqg8s e1tzin5v3">
            <div class="row-widget stButton" style="width: 829px;"><button kind="primary" class="css-jik6m7 edgvbvh9">Home2</button>
            </div>
        </div>
        """
    header_mark = st.markdown(header, unsafe_allow_html=True) 

    st.write(str(home) + str(header_mark))

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
    run()
