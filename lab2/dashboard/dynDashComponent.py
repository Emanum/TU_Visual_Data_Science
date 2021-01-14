import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
from filterData import * 

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

class DashboardCompoment:

    def __init__(self,df,app): 
        self.pDF = df
        self.app = app

    def getTab(self):
        return dbc.Card(
            dbc.CardBody(
                [
                    html.Div(children=self.getFilterHTML()),
                    html.Div(children=self.getScatterHTML()),
                ]
            ),
            className="mt-3",
        )

    def getFilterHTML(self):
        return [
            html.H2(children='Dataset filter'),
            dbc.Row(
                [
                    html.Article('Erklärung'),
                    dcc.Textarea(
                        id='dashboard-filter-textfield',
                        value='',
                        style={'width': '100%', 'height': 150},
                    ),
                ]
            ),
            dbc.Row([
                html.P("sortBy:"),
                dbc.Col(dcc.Dropdown(
                    id='dashboard-sortBy-Column', 
                    options=dropdownNumericalValues,
                    value='total_playtime'
                )),
                dbc.Col(dcc.Dropdown(
                    id='dashboard-sortByASC', 
                    options = ascDesc,
                    value='desc'
                )),
                html.P("percentage of data:"),
                dbc.Col(dcc.Slider(
                    id='dashboard-filter-percent',min=0, max=100,step=1,value=1,tooltip={'always_visible':True,'placement':'bottom'}
                )),
            ]),
            dbc.Row(html.Button('Update Filter', id='update-filter', n_clicks=0)),
        ]

    def getScatterHTML(self):
            return [
                html.H3("Scatter Plot"),
                dbc.Row([
                    html.P("x-axis:"),
                    dbc.Col(
                        dcc.Dropdown(
                            id='x-axis-scatterdashboard', 
                            options=dropdownNumericalValues,
                            value='total_playtime'
                        )
                    ),
                    html.P("y-axis:"),
                    dbc.Col(
                        dcc.Dropdown(
                            id='y-axis-scatterdashboard', 
                            options=dropdownNumericalValues,
                            value='total_playtime'
                        )
                    ),
                ]),
                html.P("Config:"),
                dbc.Row([
                    dbc.Col(
                        dcc.Checklist(
                            id='config-scatterdashboard', 
                            options=[
                                {'label': 'enable color', 'value': 'color'},
                                {'label': 'enable size', 'value': 'size'}
                            ],
                            value=[],
                            labelStyle={'display': 'inline-block'}
                        ),                       
                    ),
                ]),
                dbc.Row([
                    html.P("color:"),
                    dbc.Col(
                        dcc.Dropdown(
                            id='color-scatterdashboard', 
                            options=dropdownLabelValues,
                            value='type'
                        ), 
                    ),
                    html.P("size:"),
                    dbc.Col(
                        dcc.Dropdown(
                            id='size-scatterdashboard', 
                            options=dropdownNumericalValues,
                            value='price'
                        ),
                    ),
                ]),
                dcc.Graph(id="dashboard-scatter"),
            ]
    
    def initCallbacks(self):
        self.app.callback(dash.dependencies.Output('filteredDataset', 'children'),
            [
                dash.dependencies.Input('dashboard-sortBy-Column', 'value'),
                dash.dependencies.Input('dashboard-sortByASC', 'value'),
                dash.dependencies.Input('dashboard-filter-percent', 'value'),
                dash.dependencies.Input('update-filter', 'value')
            ])(self.updateFilteredData)
        self.app.callback(dash.dependencies.Output('dashboard-scatter', 'figure'),
            [
                dash.dependencies.Input('filteredDataset', 'children'),
                dash.dependencies.Input('x-axis-scatterdashboard', 'value'),
                dash.dependencies.Input('y-axis-scatterdashboard', 'value'),
                dash.dependencies.Input('color-scatterdashboard', 'value'),
                dash.dependencies.Input('size-scatterdashboard', 'value'),
            ])(self.createScatter)

    def updateFilteredData(self,sortBy,dataSortBy,dataAscDesc,dataPercent,n_clicks):
         return sortAndLimit(self.pDF,dataSortBy,dataAscDesc,dataPercent)

    def createScatter(self,df,x, y,siz,col,config):
        if('color' in config and 'size' in config):
            fig = px.scatter(df, x=x, y=y, color=col,size=siz,hover_name="name", hover_data=infoColumns,trendline="ols")
        elif('color' in config):
            fig = px.scatter(df, x=x, y=y, color=col,hover_name="name", hover_data=infoColumns,trendline="ols")
        elif('size' in config):
            fig = px.scatter(df, x=x, y=y, size=siz,hover_name="name", hover_data=infoColumns,trendline="ols")
        else:
            fig = px.scatter(df, x=x, y=y,hover_name="name", hover_data=infoColumns,trendline="ols")
        fig.update_layout(autosize=True, height=1250)
        return fig