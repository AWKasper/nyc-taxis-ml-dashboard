from sqlalchemy import create_engine
from sklearn.cluster import KMeans
import pandas as pd

def get_data(amount = 50000):
    engine = create_engine('mysql+mysqlconnector://kaspera1:H1c3VA29xnjPrT@oege.ie.hva.nl/zkaspera1')
    query = f"""SELECT dropoff_longitude, dropoff_latitude FROM 
    (SELECT * FROM uncleaned_NYC_yellowcabs_2015 LIMIT {amount}) 
    AS limited_data"""
    df = pd.read_sql(query, engine)
    print(df)

if __name__ == '__main__':
    get_data()