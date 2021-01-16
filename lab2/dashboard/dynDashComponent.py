import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from sklearn import preprocessing
from filterData import * 

import inspect

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
    {'label': 'category', 'value': 'categories'},
]

dropdownStatsTypeValues = [
    {'label': 'mean', 'value': 'mean'},
    {'label': 'median', 'value': 'median'},
    {'label': 'sum', 'value': 'sum'},
    {'label': 'var', 'value': 'var'},
]

dropdownStatsFilterCombinationValues = [
    {'label': 'equals', 'value': 'equals'},
    {'label': 'or', 'value': 'or'},
    {'label': 'and', 'value': 'and'},
]

ascDesc = [
    {'label': 'asc', 'value': 'asc'},
    {'label': 'desc', 'value': 'desc'}
]

sortType = [
    {'label': '%', 'value': '%'},
    {'label': 'count', 'value': 'count'}
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

dashTableColumns = [
    'name',
    'appid',
    'release_date',
    'release_year',
    #'english',
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
    'total_ratings',
    'rating',
    'average_playtime',
    'median_playtime',
    'price',
    'owners_low_bound',
    'owners_high_bound',
    #'rating_ratio',
    #'linux',
    #'mac',
    #'windows',
    'top_tag',
    'type',
    'total_playtime',
    'estimated_revenue']

explainQueryLanguage = '''
 Query Syntax: 
    1) one Query per row
    2) CSV formated, 3 Columns,  seperator=";", quotechar="'"
        filterType;Column;[item1,item2,...]
filterTypes:
    for List columns:
        and => all items must be in the game
        or => one of the item must be in the game
        not => none of the items must be in the game
        equals => excat these items items must be in the game 
                  (order does not matter)
    for single Value columns:
        smaller => game must be smaller than item
        bigger => game must be bigger than item
        same => item and game must match
        notSame => item and game must be different
Examples:
or;'platforms';[linux,mac]
or;'categories';[Single-player]
or;'developer';[Valve]

ignore top3 games:
notSame;'appid';570
notSame;'appid';578080
notSame;'appid';730
'''

explainColumns = '''
Multi item columns: 
* developer
* publisher
* platforms
* categories
* genres
* steamspy_tags

Single item label columns:
* name
* top_tag (from steamspy tags)
* type (Paid or Free)

Single item numeric columns:
* release_date
* release_year
* required_age 
* achievements
* average_playtime
* median_playtime
* price
* owners_low_bound
* owners_high_bound
* rating
* total_playtime
* estimated_revenue (price*owner_low_bound)

'''

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
                    html.Div(children=self.getTableHTML()),
                    html.Div(children=self.getScatterHTML()),
                    html.Div(children=self.getBarHTML()),
                    html.Div(children=self.getBoxHTML()),
                    html.Div(children=self.getRadialHTML()),

                ]
            ),
            className="mt-3",
        )

    def getFilterHTML(self):
        return [
            html.H2(children='Dataset filter'),
            dbc.Row([
                dbc.Col(html.Pre(explainQueryLanguage)),
                dbc.Col(html.Pre(explainColumns)),
            ]),
                

            dbc.Row(
                [
                    html.H3('Filter Query:'),
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
                dbc.Col(dcc.Dropdown(
                    id='dashboard-sortByType', 
                    options = sortType,
                    value='%'
                )),
                html.P("n of data:"),
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
    
    def getRadialHTML(self):
            return [
                html.H3("Radial Stats Chart"),
                dbc.Col([
                    dbc.Row([
                        dbc.Col(dcc.Graph(id="dashboard-radial"),width=7),
                        dbc.Col([
                            html.P("Column"),
                            dcc.Input(
                                id='dashboard-stats-column',
                                type="text", placeholder="",
                                value="platforms"
                            ),
                            html.P("Combination type"),
                            dcc.Dropdown(
                                id='dashboard-stats-filter-type', 
                                options=dropdownStatsFilterCombinationValues,
                                value='or'
                            ), 
                            #html.P("Combinations"),
                            #dcc.Input(
                            #    id='dashboard-stats-combinations',
                            #    type="text", placeholder="all"
                            #),
                            html.P("Stats type"), 
                            dcc.Dropdown(
                                id='dashboard-stats-type', 
                                options=dropdownStatsTypeValues,
                                value='mean'
                            ), 
                            
                            html.Button('Update Stats', id='update-stats', n_clicks=0)
                        ],width=3),
                    ])
                ])

            ]

    def getTableHTML(self):
         return [
            dbc.Row([
                dbc.Col(html.H3("first 25 Entries")),
                dbc.Col(html.P("total:")),
                dbc.Col(html.P(id = "dashboard-rowCount",children=["init"])),

            ]),
            dash_table.DataTable(
                id='dashboard-table',
                #fixed_columns={ 'headers': True, 'data': 1 },
                #columns=[{"name": i, "id": i} for i in self.global_dashboard_df],
                columns=[{"name": i, "id": i} for i in dashTableColumns],
                style_table={'overflowX': 'auto','overflowY': 'auto','height': '300px',},
            )
         ]

    def initCallbacks(self):
        self.app.callback(
            Output('signal', 'children'),
            Output('dashboard-rowCount', 'children'),
            Input('update-filter','n_clicks'),
            State('dashboard-sortBy-Column', 'value'),
            State('dashboard-sortByASC', 'value'),
            State('dashboard-sortByType', 'value'),
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
        self.app.callback(
            Output("dashboard-table", "data"),
            Input('signal', 'children'))(self.createTable)
        self.app.callback(
            Output("dashboard-radial", "figure"),
            Input('signal', 'children'),
            Input('update-stats','n_clicks'),
            State('dashboard-stats-column', 'value'),
            #State('dashboard-stats-combinations', 'value'),
            State('dashboard-stats-type', 'value'),
            State('dashboard-stats-filter-type', 'value'),)(self.createRadar)

    def updateFilteredData(self,n_clicks,dataSortBy,dataAscDesc,sortByType,dataPercent,textBox):
        self.global_dashboard_df = sortAndLimit2(self.pDF,dataSortBy,dataAscDesc,dataPercent,sortByType)
        #print("before lambdaArr parseFilterTextField")
        lambdaArr = parseFilterTextField(textBox)
        #print("after lambdaArr parseFilterTextField")
        self.global_dashboard_df = multipleFilter(self.global_dashboard_df,lambdaArr)
        return n_clicks,str(self.global_dashboard_df.shape[0])

    def createTable(self,signal):
        return self.global_dashboard_df.head(25).to_dict('records')

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
        fig.update_layout(autosize=True,height=800)
        return fig
    
    def createBox(self,signal,y):
        df = self.global_dashboard_df
        fig = px.box(df,y=y,hover_name="name", hover_data=infoColumns)
        fig.update_layout(autosize=True,height=500)
        return fig

    def createBar(self,signal,x,y,col):
        df = self.global_dashboard_df
        fig = px.bar(df, x=x, y=y,color=col,hover_name="name", hover_data=infoColumns,)
        fig.update_layout(autosize=True,height=750)
        return fig

    def createRadar(self,clicks,signal,columnParam,statstype,filtertype):

        stats = getStatsDataFrame(
                    df = self.global_dashboard_df,
                    columnname = columnParam,
                    combinations = splitList(get_unique_combined(self.global_dashboard_df[columnParam])),
                    filterType = filtertype,ergType=statstype,statsColumns=statsColumns)

        #add row with zero values to force minMaxScaler to begin at zero
        stats.loc[len(stats)] = 0

        x = stats.values.astype(float)
        min_max_scaler = preprocessing.MinMaxScaler()
        x_scaled = min_max_scaler.fit_transform(x)
        rowNames = stats.index.to_list()
        stats_normalized = pd.DataFrame(x_scaled, stats.index, stats.columns)

        #delete row again to hide in the graph
        stats_normalized.drop(stats_normalized.tail(1).index,inplace=True)

        fig = go.Figure()
        for index, row in stats_normalized.iterrows():
            fig.add_trace(go.Scatterpolar(
                r=row.to_list(),
                theta=stats_normalized.columns.to_list(),
                #fill='toself',
                name=index
            ))
        fig.update_polars(radialaxis_autorange=True)
        '''fig.update_layout(
            polar=dict(
                radialaxis=dict(
                visible=True,
                range=[0, 5]
                )),
            showlegend=False
        )
        '''
        fig.update_layout(autosize=True,height=750)
        return fig