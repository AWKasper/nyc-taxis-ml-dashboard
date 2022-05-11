import os
import sys

mycwd = os.getcwd()

from shapes_mapping import plottingNYC
#Plotting NYC zones
import pandas as pd
from sqlalchemy import create_engine
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

engine = create_engine('mysql+mysqlconnector://kaspera1:H1c3VA29xnjPrT@oege.ie.hva.nl/zkaspera1')

df = pd.read_sql("SELECT dropoff_longitude, dropoff_latitude FROM uncleaned_NYC_yellowcabs_2015 LIMIT 25000", engine)

df_fixed = df['dropoff_longitude'].between(-74.3,-73.7) & df['dropoff_latitude'].between(40.0,41.0)
df = df[df_fixed]
df_num = df.to_numpy()
model = KMeans(n_clusters = 10)

# Fit model to samples
model.fit(df_num)
# print(model.cluster_centers_)

p = plottingNYC(mycwd  + r'\data\processed\taxi_zones\taxi_zones.shp', 'borough')
p.scatter(df['dropoff_longitude'],df['dropoff_latitude'],alpha=0.05)
p.scatter(model.cluster_centers_[:,0],model.cluster_centers_[:,1],color='red')


#Going back to the working directory from before
os.chdir(fr'{mycwd}')

p.show()