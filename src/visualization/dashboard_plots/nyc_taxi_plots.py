import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
import plotly.express as px

data= pd.read_csv(r"data\clean data\taxiclean.csv")
df= pd.DataFrame(data)
data.columns

def barplot_kosten_pkm():
    data.groupby('trip_distance')['total_amount'].mean().sort_values(ascending= False)
    sns.barplot(x='trip_distance', y= 'total_amount', data= df)
    plt.title("Kosten per kilometer")
    plt.show()

def plot_people_per_ride():
    df.sort_values('trip_distance',inplace= True, ascending= True)
    df['passenger_count'].info()
    # print(df['trip_distance'])
    fig = px.scatter(df, x='trip_distance', y= 'total_amount', color= 'passenger_count', trendline= "ols",trendline_scope="overall", trendline_color_override="black")
    
    return fig