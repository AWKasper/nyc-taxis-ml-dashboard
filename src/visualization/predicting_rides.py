import numpy as np
import math
import pandas as pd
from datetime import datetime

import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression, Ridge
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import pickle


def linear_prediction(date, time, precipitation, temperature):

    time_of_day = time.strftime(r'%H')
    day = date.weekday()
    month = date.strftime(r'%m')

    loaded_model = pickle.load(open('src\models\multi_lin_regr_trained.sav', 'rb'))

    prediction = loaded_model.predict([[temperature, precipitation, day, month, time_of_day]])

    df = pd.DataFrame([[math.ceil(prediction[0]), 'multiple linear regression']], columns=["prediction", 'model'])
    
    # , x=prediction.columns[0]
    g = sns.catplot(data=df, kind='bar', x='model', y='prediction')

    ax = g.facet_axis(0, 0)

    ax.bar_label(ax.containers[0])

    plt.show()