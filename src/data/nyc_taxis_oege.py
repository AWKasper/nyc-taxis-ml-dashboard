import pandas as pd
from sqlalchemy import create_engine

def oege_engine():
    engine = create_engine('mysql+mysqlconnector://kaspera1:H1c3VA29xnjPrT@oege.ie.hva.nl/zkaspera1', echo=True)
    return engine

chunks = pd.read_sql("SELECT pickup_longitude, pickup_latitude, dropoff_longitude, dropoff_latitude, trip_distance FROM uncleaned_NYC_yellowcabs_2015", oege_engine(), chunksize=50000)

df = pd.concat(chunks, ignore_index=True)