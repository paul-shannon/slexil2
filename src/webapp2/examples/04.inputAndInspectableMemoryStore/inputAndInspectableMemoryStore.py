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

dashApp.title = "input button memory store"


dashApp.layout=html.Div(
   id='output',
   children=[
     dcc.Store(id='memoryStore', storage_type='memory'),
     html.H4('Project Name',style={'display':'inline-block','margin-right':20}),
      dcc.Input(id='projectNameInput',type='text',
                placeholder='',
                style={'display':'inline-block', 'font-size': "24px"}),
      html.Button("Submit", id="setProjectNameButton", n_clicks=0,
                  style={"margin-left": "20px", "font-size": "24px"}),
      html.Div(id="messageDiv", children=[html.Span("")], style=dynamicDivStyle),
      html.Button("Examine Memory Store", id="memoryStoreButton", n_clicks=0,
                  style={"margin-left": "20px", "margin-top": "30px", "font-size": "24px"}),

      html.Div(id="memoryStoreDiv", children=[html.Span("")],
               style={"height": "400px", "width": "600px", "font-size": "24px",
                      "overflow": "auto",
                      "border": "2px dotted black", "border-radius": "10px",
                      "margin": "30px", "margin-top": "10px", "padding": "20px"})
      ], style={"margin": "20px"})

@callback(
     Output('messageDiv', 'children', allow_duplicate=True),
     Input('projectNameInput', 'value'),
     prevent_initial_call=True)
def handleInputChars(userEnteredString):
    return(userEnteredString)



#@callback(
##     Output('messageDiv', 'children'),
#    Input('projectNameInput', 'value'),
#    prevent_initial_call=True)
#def handleProjectNameInputCharacters(chars):
#     print(chars)
##     return [html.P(chars)]

@callback(
    Output('messageDiv', 'children', allow_duplicate=True),
    Output('memoryStore', 'data'),
    Input('setProjectNameButton', 'n_clicks'),
    State('projectNameInput', 'value'),
    State('memoryStore', 'data'),
    prevent_initial_call=True)
def handleSetProjectNameButton(n_clicks, userEnteredString, data):
    trackingString = "%d n_clicks: %s" % (n_clicks, userEnteredString)
    print("examining memoryStore data")
    print(data)
    if data is None:
       print("initializing None data")
       data = {}
    data['projectName'] = userEnteredString
    return(trackingString, data)

@callback(
    Output('memoryStoreDiv', 'children'),
    Input('memoryStoreButton', 'n_clicks'),
    State('memoryStore', 'data'),
    prevent_initial_call=True)
def displayMemoryStore(n_clicks,data):
    el = html.Ul(id="list", children=[])
    memoryStoreDiv = el
    for key in data.keys():
       el.children.append(html.Li("%s: %s" % (key, data[key])))
    #memoryStoreDiv += [el]
    return memoryStoreDiv



if __name__ == '__main__':
    print("=============================")
    port = 9009
    print("starting main.py on port %d" % port)
    app.run(host='0.0.0.0', debug=True, port=port)
    print("=============================")

