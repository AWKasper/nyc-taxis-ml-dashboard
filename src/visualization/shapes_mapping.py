import geopandas as gpd
import matplotlib.pyplot as plt

def plotting_map(path, column_used_for_legend=''):
    df = gpd.read_file(fr'{path}')
    df.head()

    fig, ax = plt.subplots(1, 1, figsize=(15, 15))

    if(column_used_for_legend == ''):
        df.plot(ax=ax)
    else:
        df.plot(ax=ax, column=f'{column_used_for_legend}', legend=True)

    return df