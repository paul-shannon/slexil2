import flask
from dash import Dash, dcc, html, dash_table, Input, Output, State, callback
from dash.exceptions import PreventUpdate

import base64
import datetime
import io
import json
import pdb

import pandas as pd
pd.set_option('display.width', 1000)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
dynamicDivStyle = {"width": 400,
                   "border": "1px solid darkblue",
                   "border-radius": 5,
                   "margin": 10,
                   "padding": 10}

app = flask.Flask(__name__)

dashApp = Dash(__name__, server=app, url_base_pathname='/',
                external_stylesheets=external_stylesheets)

dashApp.title = "input widget only"


dashApp.layout=html.Div(
   id='output',
   children=[
      html.H4('Project Name',style={'display':'inline-block','margin-right':20}),
      dcc.Input(id='projectNameInput',type='text',
                style={'display':'inline-block', 'font-size': "24px"}),
      html.Div(id="messageDiv", children=[html.Span("")], style=dynamicDivStyle),
      ], style={"margin": "20px"})

@callback(
     Output('messageDiv', 'children'),
     Input('projectNameInput', 'value'),
     prevent_initial_call=True)
def handleInputChars(userEnteredString):
    return(userEnteredString)

if __name__ == '__main__':
    print("=============================")
    port = 9009
    print("starting main.py on port %d" % port)
    app.run(host='0.0.0.0', debug=True, port=port)
    print("=============================")

