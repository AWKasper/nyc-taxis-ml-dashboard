import numpy as np
import pandas as pd
import gmaps
import gmaps.datasets
from src.data.nyc_taxis_oege import oege_engine

chunks = pd.read_sql("SELECT * FROM uncleaned_NYC_yellowcabs_2015 LIMIT 100000", oege_engine(), chunksize=1000000)

df = pd.concat(chunks, ignore_index=True)

df.describe()

