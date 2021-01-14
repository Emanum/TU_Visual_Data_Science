import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from filterData import * 

class DashboardCompoment:

    # default constructor 
    def __init__(self,df): 
        self.pDf = df

    def getTab(self):
        return dbc.Card(
            dbc.CardBody(
                [
                    html.H2(children='Dataset filter'),
                    dbc.Row(
                        [
                            html.Article('Erklärung'),
                            dcc.Textarea(
                                id='textarea-example',
                                value='Textarea content initialized\nwith multiple lines of text',
                                style={'width': '100%', 'height': 300},
                            ),
                        ]
                    ),
                ]
            ),
            className="mt-3",
        )