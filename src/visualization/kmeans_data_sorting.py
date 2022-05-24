from time import strftime
from sqlalchemy import create_engine
from sklearn.cluster import KMeans
import pandas as pd
import datetime as dt

def get_data(amount = 50000):
    engine = create_engine('mysql+mysqlconnector://kaspera1:H1c3VA29xnjPrT@oege.ie.hva.nl/zkaspera1')
    query = f"""SELECT tpep_pickup_datetime, pickup_longitude, pickup_latitude FROM 
    (SELECT * FROM uncleaned_NYC_yellowcabs_2015 LIMIT {amount}) 
    AS limited_data"""
    df = pd.read_sql(query, engine)
    df['tpep_pickup_datetime'] = df.apply(lambda row:row['tpep_pickup_datetime'][:-6], axis=1)
    print(df['tpep_pickup_datetime'].value_counts())

if __name__ == '__main__':
    get_data(5)