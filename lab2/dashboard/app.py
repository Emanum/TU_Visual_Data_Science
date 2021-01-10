import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import itertools
import re
import math
import numpy as np
from prepareData import *
from barchart import *
from scatterChart import *

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
#topPDF = topDataset(50,pDF)
tptPDF = pDF.sort_values('total_playtime',ascending=False).head(math.ceil(27075*0.01))


# INIT Dropdown
dropdownNumericalValues = [
    {'label': 'price', 'value': 'price'},
    {'label': 'owners_low_bound', 'value': 'owners_low_bound'},
    {'label': 'owners_high_bound', 'value': 'release_year'},
    {'label': 'release_year', 'value': 'release_year'},
    {'label': 'required_age', 'value': 'required_age'},
    {'label': 'achievements', 'value': 'achievements'},
    {'label': 'average_playtime', 'value': 'average_playtime'},
    {'label': 'median_playtime', 'value': 'median_playtime'},
    {'label': 'total_playtime', 'value': 'total_playtime'},
    {'label': 'estimated_revenue', 'value': 'estimated_revenue'}
]

# Bar Charts
barFig = barChartAllYears(pDF)

barFig2 = barChartPerYear(pDF)

top=50
barFig3 = barChartPerYearTopN(pDF,top)
barFig4 = barChartAllYearsName(pDF,top)

#Boxplot
boxplot1 = px.box(pDF, y="total_playtime")

# Scatter Charts
scatter1 = scatterChart(tptPDF,'total_playtime','owners_low_bound',col='top_tag',siz='rating')
scatter2 = scatterChart(tptPDF,'rating','price',col='developer',siz='windows')

@app.callback(
    Output("scatter-plot-1", "figure"), 
    [Input("x-axis-scatter1", "value"), 
     Input("y-axis-scatter1", "value")])
def generate_chart(x, y):
    fig = px.scatter(pDF, x=x, y=y, hover_name="name", hover_data=[x, y])
    return fig

app.layout = html.Div(children=[
    html.H1(children='Steam Game Data'),

    html.H2(children='Total Playtime'),

    html.H4(children='Total Playtime = average_playtime * owners_lower_bound'),

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
    ),

    html.H2(children='Total Playtime top 50 Games'),

    dcc.Graph(
        id='barChart-allTop50',
        figure=barFig4
    ),

    html.H1(children='Distribution Total Playtime'),
        dcc.Graph(
        id='box-1',
        figure=boxplot1
    ),

    html.H1(children='Distribution Top 271 Games'),
        dcc.Graph(
        id='scatter-1',
        figure=scatter1
    ),

    html.H1(children='Distribution Top 271 Games'),
        dcc.Graph(
        id='scatter-2',
        figure=scatter2
    ),

    html.P("x-axis:"),
    dcc.Dropdown(
        id='x-axis-scatter1', 
        options=dropdownNumericalValues,
        value='price'
        #labelStyle={'display': 'inline-block'}
    ),
    html.P("y-axis:"),
    dcc.Dropdown(
        id='y-axis-scatter1', 
        options=dropdownNumericalValues,
        value='price'
        #labelStyle={'display': 'inline-block'}
    ),
    dcc.Graph(id="scatter-plot-1"),

])

if __name__ == '__main__':
    app.run_server(debug=True)