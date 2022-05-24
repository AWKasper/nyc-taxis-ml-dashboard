from re import A
from time import strftime
from typing import Dict
from sqlalchemy import create_engine
from sklearn.cluster import KMeans
import pandas as pd
import datetime as dt

DATE_COL = "tpep_pickup_datetime"
LONGI = "pickup_longitude"
LATI = "pickup_latitude"

def __get_data(amount = 50000):
    engine = create_engine('mysql+mysqlconnector://kaspera1:H1c3VA29xnjPrT@oege.ie.hva.nl/zkaspera1')
    query = f"""SELECT {DATE_COL}, {LONGI}, {LATI} FROM 
    (SELECT * FROM uncleaned_NYC_yellowcabs_2015 LIMIT {amount}) 
    AS limited_data"""
    return pd.read_sql(query, engine)
    
def __format_date_strings(df : pd.DataFrame):
    df[DATE_COL] = df.apply(lambda row:row['tpep_pickup_datetime'][:-6], axis=1)
    return df

def __order_coords_by_date(df : pd.DataFrame):
    dic = dict()
    for i, row in df.iterrows():
        dic.setdefault(row[DATE_COL], list())
        dic[row[DATE_COL]].append([row[LONGI],row[LATI]])
    return dic

def __write_to_file(filename : str, data : dict):
    import json
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

if __name__ == '__main__':
    df = __get_data(25)
    df = __format_date_strings(df)
    dic = __order_coords_by_date(df)
    __write_to_file("rides.json", dic)
    
