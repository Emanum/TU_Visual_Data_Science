import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
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
    {'label': 'name', 'value': 'name'},
    {'label': 'release_year', 'value': 'release_year'},
    {'label': 'release_date', 'value': 'release_date'},
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
    #'categories',row is too long
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
        self.global_dashboard_df = df
        self.app = app
        self.initCallbacks()

    def getTab(self):
        return dbc.Card(
            dbc.CardBody(
                [
                    html.Div(children=self.getFilterHTML()),
                    html.Div(children=self.getScatterHTML()),
                    html.Div(children=self.getBoxHTML()),
                    html.Div(children=self.getBarHTML()),

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
                            value='release_date'
                        )
                    ),
                    html.P("y-axis:"),
                    dbc.Col(
                        dcc.Dropdown(
                            id='y-axis-scatterdashboard', 
                            options=dropdownNumericalValues,
                            value='rating'
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
    
    def getBoxHTML(self):
        return [
            html.H3("Box Plot"),
                dbc.Row([
                    html.P("y-axis:"),
                    dbc.Col(
                        dcc.Dropdown(
                            id='y-axis-boxdashboard', 
                            options=dropdownNumericalValues,
                            value='rating'
                        )
                    )
                ]),
                dcc.Graph(id="dashboard-box"),
        ]
    
    def getBarHTML(self):
        return [
            html.H3("Bar Chart"),
                dbc.Row([
                    html.P("x-axis:"),
                    dbc.Col(
                        dcc.Dropdown(
                            id='x-axis-bardashboard', 
                            options=dropdownLabelValues,
                            value='top_tag'
                        )
                    ),
                    html.P("y-axis:"),
                    dbc.Col(
                        dcc.Dropdown(
                            id='y-axis-bardashboard', 
                            options=dropdownNumericalValues,
                            value='owners_low_bound'
                        )
                    ),
                    html.P("color:"),
                    dbc.Col(
                        dcc.Dropdown(
                            id='color-bardashboard', 
                            options=dropdownLabelValues,
                            value='release_year'
                        ), 
                    ),
                ]),
                dcc.Graph(id="dashboard-bar"),
        ]
    
    def initCallbacks(self):
        self.app.callback(
            Output('signal', 'children'),
            Input('update-filter','n_clicks'),
            State('dashboard-sortBy-Column', 'value'),
            State('dashboard-sortByASC', 'value'),
            State('dashboard-filter-percent', 'value'),
            State('dashboard-filter-textfield', 'value'))(self.updateFilteredData)
        self.app.callback(
            Output("dashboard-scatter", "figure"),
            Input('signal', 'children'),
            Input("x-axis-scatterdashboard", "value"), 
            Input("y-axis-scatterdashboard", "value"),
            Input("color-scatterdashboard", "value"),
            Input("size-scatterdashboard", "value"),
            Input("config-scatterdashboard", "value"))(self.createScatter)
        self.app.callback(
            Output("dashboard-box", "figure"),
            Input('signal', 'children'), 
            Input("y-axis-boxdashboard", "value"))(self.createBox)
        self.app.callback(
            Output("dashboard-bar", "figure"),
            Input('signal', 'children'), 
            Input("x-axis-bardashboard", "value"),
            Input("y-axis-bardashboard", "value"),
            Input("color-bardashboard", "value"))(self.createBar)

    def updateFilteredData(self,n_clicks,dataSortBy,dataAscDesc,dataPercent,textBox):
        self.global_dashboard_df = sortAndLimit(self.pDF,dataSortBy,dataAscDesc,dataPercent)
        return n_clicks

    def createScatter(self,signal,x, y,col,siz,config):
        df = self.global_dashboard_df
        if('color' in config and 'size' in config):
            fig = px.scatter(df, x=x, y=y, color=col,size=siz,hover_name="name", hover_data=infoColumns,trendline="ols")
        elif('color' in config):
            fig = px.scatter(df, x=x, y=y, color=col,hover_name="name", hover_data=infoColumns,trendline="ols")
        elif('size' in config):
            fig = px.scatter(df, x=x, y=y, size=siz,hover_name="name", hover_data=infoColumns,trendline="ols")
        else:
            fig = px.scatter(df, x=x, y=y,hover_name="name", hover_data=infoColumns,trendline="ols")
        fig.update_layout(autosize=True)
        return fig
    
    def createBox(self,signal,y):
        df = self.global_dashboard_df
        return px.box(df,y=y,hover_name="name", hover_data=infoColumns)

    def createBar(self,signal,x,y,col):
        df = self.global_dashboard_df
        return px.bar(df, x=x, y=y,color=col,hover_name="name", hover_data=infoColumns,)