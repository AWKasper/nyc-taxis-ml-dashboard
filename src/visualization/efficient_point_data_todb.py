from sqlalchemy import create_engine, false, insert, MetaData, Table, select
import tools.db_tools as tools
from datetime import datetime, timedelta
import pandas as pd

DATE_COL = "tpep_pickup_datetime"
LONGI = "pickup_longitude"
LATI = "pickup_latitude"
MIN_DATE_ID = datetime(2015,1,1,0)

# amount = 0 will be interpreted as all
def __get_data(offset = 0, amount = 50000, chunksize = 10000):
    engine = create_engine('mysql+mysqlconnector://kaspera1:H1c3VA29xnjPrT@oege.ie.hva.nl/zkaspera1')
    query = f"SELECT {DATE_COL}, {LONGI}, {LATI} FROM uncleaned_NYC_yellowcabs_2015 LIMIT {amount} OFFSET {offset}"
    if amount == 0: query = f"SELECT {DATE_COL}, {LONGI}, {LATI} FROM uncleaned_NYC_yellowcabs_2015"
    chunks = pd.read_sql(query, engine, chunksize = chunksize )
    return pd.concat(chunks, ignore_index=True)
    
def __format_date_strings(df : pd.DataFrame):
    df[DATE_COL] = df.apply(lambda row:row['tpep_pickup_datetime'][:-6], axis=1)
    return df

def execute_process():
    df = __get_data(amount = 0)
    df = __format_date_strings(df)
    df[DATE_COL] = df[DATE_COL].apply(__convert_date_to_id)
    __write_to_db(df)

def __convert_date_to_id(row):
    dt = datetime.strptime(row, '%Y-%m-%d %H')
    delta = dt - MIN_DATE_ID
    return delta.days * 24 + delta.seconds / 3600

def __write_to_db(df : pd.DataFrame):
    engine = create_engine('mysql+mysqlconnector://kaspera1:H1c3VA29xnjPrT@oege.ie.hva.nl/zkaspera1')
    
    df = df.rename(columns={'tpep_pickup_datetime' : 'ID', 'pickup_longitude' : 'Longitude', 'pickup_langitude' : 'Langitude'})
    
    df.to_sql(name='ID_date_points', con=engine, if_exists='replace', index=False)
    

if __name__ == '__main__':
    # data = __get_data(amount=25)
    # data = __format_date_strings(data)
    # data[DATE_COL] = data[DATE_COL].apply(__convert_date_to_id)
    # print(data)
    # for x in data.iterrows():
    #     print(x)
    execute_process()
    #__generate_dts()