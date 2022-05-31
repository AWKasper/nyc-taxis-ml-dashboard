import streamlit as st
import utils as utl
from views import home,about,documentation,dashboard,about

st.set_page_config(page_title='Navbar sample')
st.set_option('deprecation.showPyplotGlobalUse', False)
utl.inject_custom_css()
utl.navbar_component()

def navigation():
    route = utl.get_current_route()
    if route == "home":
        home.load_view()
    elif route == "about":
        about.load_view()
    elif route == "documentation":
        documentation.load_view()
    elif route == "dashboard":
        dashboard.load_view()
    elif route == "about":
        about.load_view()
    elif route == None:
        home.load_view()
        
navigation()