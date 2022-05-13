import numpy as np
import pandas as pd
from datetime import datetime

from src.data.nyc_taxis_oege import oege_engine

chunks = pd.read_sql("SELECT tpep_pickup_datetime, VendorID FROM uncleaned_NYC_yellowcabs_2015", oege_engine(), chunksize=10000)

df = pd.concat(chunks, ignore_index=True)

df.rename(columns={"VendorID": "count"}, inplace=True)

df.tpep_pickup_datetime = df.tpep_pickup_datetime.apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S').replace(minute=0, second=0))

df = df.groupby('tpep_pickup_datetime', as_index=False).count()

df.to_sql(name='rides_per_day_2015',con=oege_engine(),if_exists='replace',index=False, chunksize=10000)
