import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
import itertools
import re
import math
import numpy as np
from prepareData import *
from barchart import *
from scatterChart import *
from filterData import * 
from dynDashComponent import *  

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# INIT
df = pd.read_csv(filepath_or_buffer = '/Users/Manuel 1/Desktop/TU_Visual_Data_Science/lab2/dashboard/data/steam.csv',sep=',', decimal = ".")
pDF = pre_process(df)
#topPDF = topDataset(50,pDF)
tptPDF = pDF.sort_values('total_playtime',ascending=False).head(math.ceil(27075*0.01))

# INIT Dropdown
dropdownNumericalValues = [
    {'label': 'price', 'value': 'price'},
    {'label': 'owners_low_bound', 'value': 'owners_low_bound'},
    {'label': 'release_year', 'value': 'release_year'},
    {'label': 'rating', 'value': 'rating'},
    {'label': 'release_year', 'value': 'release_year'},
    {'label': 'release_date', 'value': 'release_date'},
    {'label': 'required_age', 'value': 'required_age'},
    {'label': 'achievements', 'value': 'achievements'},
    {'label': 'average_playtime', 'value': 'average_playtime'},
    {'label': 'median_playtime', 'value': 'median_playtime'},
    {'label': 'total_playtime', 'value': 'total_playtime'},
    {'label': 'estimated_revenue', 'value': 'estimated_revenue'}
]

statsColumns = ['release_date','required_age','achievements','average_playtime','price','owners_low_bound','rating','total_playtime','estimated_revenue']

dropdownLabelValues = [
    {'label': 'FreeToPlay-Paid', 'value': 'type'},
    {'label': 'SteamSpy-TopTag', 'value': 'top_tag'},
    {'label': 'publisher', 'value': 'publisher'},
    {'label': 'developer', 'value': 'developer'},
    {'label': 'name', 'value': 'name'}
]

ascDesc = [
    {'label': 'asc', 'value': 'asc'},
    {'label': 'desc', 'value': 'desc'}
]

infoColumns = [
    'release_date',
    'developer',
    'publisher',
    'platforms',
    'required_age',
    'categories',
    'genres',
    'steamspy_tags',
    'achievements',
    'positive_ratings',
    'negative_ratings',
    'rating',
    'average_playtime',
    'median_playtime',
    'owners_low_bound', 
    'owners_high_bound',
    'price'
 ]

# Bar Charts
barFig = barChartAllYears(pDF)

barFig2 = barChartPerYear(pDF)

top=50
barFig3 = barChartPerYearTopN(pDF,top)
barFig4 = barChartAllYearsName(pDF,top)

#Boxplot
boxplot1 = px.box(pDF, y="total_playtime")


# ----- INIT CACHE -----
#TODO use cache

#global_dashboard_df = pDF

# -------- INIT DASHBOARD -------

dashboardComp = DashboardCompoment(df,app)
dashboard = dashboardComp.getTab()

# --------   LAYOUT  ------------

presentationTab = dbc.Card(
    dbc.CardBody(
        [
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

            html.H3(children='Distribution Total Playtime'),
                dcc.Graph(
                id='box-1',
                figure=boxplot1
            ),
        ]
    ),
    className="mt-3",
)

app.layout = dbc.Container([
    html.H1(children='Steam Game Data'),
    dbc.Tabs(
        [
            dbc.Tab(dashboard, label="Dashboard"),
            dbc.Tab(presentationTab, label="Presentation"),
        ]
    ),

    html.Div(id='signal', style={'display': 'none'})

], fluid=True)

if __name__ == '__main__':
    app.run_server(debug=True)