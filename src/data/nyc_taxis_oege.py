import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt

def oege_engine():
    engine = create_engine('mysql+mysqlconnector://kaspera1:H1c3VA29xnjPrT@oege.ie.hva.nl/zkaspera1', echo=True)
    return engine

def main():

    chunks = pd.read_sql("SELECT * FROM uncleaned_NYC_yellowcabs_2015 LIMIT 100000", oege_engine(), chunksize=50000)

    df = pd.concat(chunks, ignore_index=True)

    df.describe()

    df.to_csv(r'local\taxi_coords.csv', index=False)

    from src.visualization.shapes_mapping import plotting_map

    nycdf = plotting_map(r'data\processed\taxi_zones\taxi_zones.shp', 'borough')


    for row in df.itertuples():
        plt.plot()

    plt.show()

if __name__ == '__main__':
    main()