import os

from shapes_mapping import plotting_map
#Plotting NYC zones
import pandas as pd
from sqlalchemy import create_engine
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

def make_kmeans_map_graph(kmeans_points : int = 10, n_data : int = 25000):
    engine = create_engine('mysql+mysqlconnector://kaspera1:H1c3VA29xnjPrT@oege.ie.hva.nl/zkaspera1')

    df = pd.read_sql(f"SELECT dropoff_longitude, dropoff_latitude FROM uncleaned_NYC_yellowcabs_2015 LIMIT {n_data}", engine)

    df_fixed = df['dropoff_longitude'].between(-74.3,-73.7) & df['dropoff_latitude'].between(40.0,41.0)
    df = df[df_fixed]
    df_num = df.to_numpy()

    model = KMeans(n_clusters = kmeans_points)
    model.fit(df_num)

    # get plotting map and scatter cluster points
    p = plotting_map(rf'{os.getcwd()}\data\processed\taxi_zones\taxi_zones.shp', 'borough')
    p.scatter(df['dropoff_longitude'],df['dropoff_latitude'],alpha=0.05, color='green')
    p.scatter(model.cluster_centers_[:,0],model.cluster_centers_[:,1],color='red')

    return p