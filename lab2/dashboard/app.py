import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import itertools
import re
import math
import numpy as np
from prepareData import *
from barchart import *

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df_example = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

fig_example = px.bar(df_example, x="Fruit", y="Amount", color="City", barmode="group")

# INIT
df = pd.read_csv(filepath_or_buffer = '/Users/Manuel 1/Desktop/TU_Visual_Data_Science/lab2/dashboard/data/steam.csv',sep=',', decimal = ".")
pDF = pre_process(df)
topPDF = topDataset(50,pDF)

# GRAPH 1
barFig = barChartAllYears(pDF)

barFig2 = barChartPerYear(pDF)

top=50
barFig3 = barChartPerYearTopN(pDF,top)

app.layout = html.Div(children=[
    html.H1(children='Steam Game Data'),

    html.H2(children='Total Playtime'),

    dcc.Graph(
        id='barChart-all',
        figure=barFig
    ),

    html.H2(children='Total Playtime per Release Year'),

    dcc.Graph(
        id='barChart-perYear',
        figure=barFig2
    ),

    html.H2(children='Total Playtime per Release Year top 50 Games'),

    dcc.Graph(
        id='barChart-perYearAndName',
        figure=barFig3
    )

])

if __name__ == '__main__':
    app.run_server(debug=True)