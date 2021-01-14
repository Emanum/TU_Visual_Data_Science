import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
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

# Scatter Charts
#scatter1 = scatterChart(tptPDF,'total_playtime','owners_low_bound',col='top_tag',siz='rating')
#scatter2 = scatterChart(tptPDF,'rating','price',col='developer',siz='windows')

def filterData(df,dataSortBy,dataAscDesc,dataPercent):
    asc = dataAscDesc == 'asc'
    rowNr = int(len(df)*(dataPercent/100))
    return df.sort_values(by=dataSortBy,ascending=asc).head(rowNr)

@app.callback(
    Output("scatter-plot-1", "figure"), 
    [Input("x-axis-scatter1", "value"), 
     Input("y-axis-scatter1", "value"),
     Input("size-scatter1", "value"),
     Input("color-scatter1", "value"),
     Input("config-scatter1", "value"),
     Input("data-sortBy-scatter1", "value"),
     Input("data-ascdesc-scatter1", "value"),
     Input("data-percentage-scatter1", "value"),
     ])
def generate_scatter1(x, y,siz,col,config,dataSortBy,dataAscDesc,dataPercent):
    dataProc = sortAndLimit(df,dataSortBy,dataAscDesc,dataPercent)
    if('color' in config and 'size' in config):
        fig = px.scatter(dataProc, x=x, y=y, color=col,size=siz,hover_name="name", hover_data=infoColumns,trendline="ols")
    elif('color' in config):
        fig = px.scatter(dataProc, x=x, y=y, color=col,hover_name="name", hover_data=infoColumns,trendline="ols")
    elif('size' in config):
        fig = px.scatter(dataProc, x=x, y=y, size=siz,hover_name="name", hover_data=infoColumns,trendline="ols")
    else:
        fig = px.scatter(dataProc, x=x, y=y,hover_name="name", hover_data=infoColumns,trendline="ols")
    fig.update_layout(autosize=True, height=1250)
    return fig

@app.callback(
    Output("custom-box-plot", "figure"), 
    [Input("y-axis-box1", "value"), 
     Input("data-sortBy-box1", "value"),
     Input("data-ascdesc-box1", "value"),
     Input("data-percentage-box1", "value")
     ])
def generate_box1(y,dataSortBy,dataAscDesc,dataPercent):
    dataProc = sortAndLimit(df,dataSortBy,dataAscDesc,dataPercent)
    return px.box(dataProc,y=y,hover_name="name", hover_data=infoColumns)

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

explorationTab = dbc.Card(
    dbc.CardBody(
        [
            html.H2(children='Customizable Box Plot'),

            html.H5("Datasource:"),
            html.P("sortBy:"),
            dcc.Dropdown(
                id='data-sortBy-box1', 
                options=dropdownNumericalValues,
                value='total_playtime'
            ),
            dcc.Dropdown(
                id='data-ascdesc-box1', 
                options = ascDesc,
                value='desc'
            ),
            html.P("percentage of data:"),
            dcc.Slider(
                id='data-percentage-box1',
                min=0,
                max=100,
                step=1,
                value=10,
                tooltip={
                    'always_visible':True,
                    'placement':'bottom'
                }
            ),
            html.P("y-axis:"),
            dcc.Dropdown(
                id='y-axis-box1', 
                options=dropdownNumericalValues,
                value='total_playtime'
            ),
            dcc.Graph(id="custom-box-plot"),

            html.H2(children='Customizable Scatter Plot'),

            html.H5("Datasource:"),
            html.P("sortBy:"),
            dcc.Dropdown(
                id='data-sortBy-scatter1', 
                options=dropdownNumericalValues,
                value='total_playtime'
            ),
            dcc.Dropdown(
                id='data-ascdesc-scatter1', 
                options = ascDesc,
                value='desc'
            ),
            html.P("percentage of data:"),
            dcc.Slider(
                id='data-percentage-scatter1',
                min=0,
                max=100,
                step=1,
                value=1,
                tooltip={
                    'always_visible':True,
                    'placement':'bottom'
                }
            ),
            html.P("x-axis:"),
            dcc.Dropdown(
                id='x-axis-scatter1', 
                options=dropdownNumericalValues,
                value='total_playtime'
            ),
            html.P("y-axis:"),
            dcc.Dropdown(
                id='y-axis-scatter1', 
                options=dropdownNumericalValues,
                value='total_playtime'
            ),
            html.P("Config:"),
            dcc.Checklist(
                id='config-scatter1', 
                options=[
                    {'label': 'enable color', 'value': 'color'},
                    {'label': 'enable size', 'value': 'size'}
                ],
                value=[],
                labelStyle={'display': 'inline-block'}
            ),
            html.P("color:"),
            dcc.Dropdown(
                id='color-scatter1', 
                options=dropdownLabelValues,
                value='type'
            ),
            html.P("size:"),
            dcc.Dropdown(
                id='size-scatter1', 
                options=dropdownNumericalValues,
                value='price'
            ),
            dcc.Graph(id="scatter-plot-1"),
        ]
    ),
    className="mt-3",
)

dashboardComp = DashboardCompoment(df,app)
dashboard = dashboardComp.getTab()

app.layout = dbc.Container([
    html.H1(children='Steam Game Data'),

    dbc.Tabs(
        [
            dbc.Tab(dashboard, label="Dashboard"),
            dbc.Tab(presentationTab, label="Presentation"),
            dbc.Tab(explorationTab, label="Exploration"),
        ]
    )

])




if __name__ == '__main__':
    app.run_server(debug=True)