import pandas as pd
from sqlalchemy import create_engine

def oege_engine():
    engine = create_engine('mysql+mysqlconnector://kaspera1:H1c3VA29xnjPrT@oege.ie.hva.nl/zkaspera1', echo=True)
    return engine
