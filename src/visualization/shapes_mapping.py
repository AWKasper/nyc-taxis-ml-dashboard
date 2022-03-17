import geopandas as gpd
import matplotlib.pyplot as plt

df = gpd.read_file(r'data\processed\taxi_zones.shp')
df.head()

df.shape

fig, ax = plt.subplots(1, 1, figsize=(15, 15))
df.plot(ax=ax, column='borough', legend=True)
plt.show()