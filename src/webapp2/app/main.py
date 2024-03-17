import flask
from dash import Dash, dcc, html, dash_table, Input, Output, State, callback
from dash.exceptions import PreventUpdate

import base64
import datetime
import io
import pdb

import pandas as pd
pd.set_option('display.width', 1000)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

from slexil.xmlFileUtils import XmlFileUtils
from slexil.eafParser import EafParser

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
dynamicDivStyle = {"width": 400,
                     "border": "1px solid darkblue",
                     "border-radius": 5,
                     "margin": 10,
                     "padding": 10}
app = flask.Flask(__name__)

dash_app = Dash(__name__, server=app, url_base_pathname='/',
                external_stylesheets=external_stylesheets)

# the dynamic div's children must be a list, so that it can be
# note that list += [newItem] is equivalent to list.append(newItem)

    #---------------------------------------
    # layout
    #---------------------------------------

dash_app.layout=html.Div(
   id='output',
   children=[
      dcc.Store(id='memoryStore', storage_type='memory'),
      html.Button("See Storage",id='displayStorageButton', n_clicks=0),
      html.Button("Clear Messages",id='clearMessagesButton', n_clicks=0),
      dcc.Upload(
        id='uploaderWidget',
        children=html.Div([html.A('Select File',
                                  style={"font-size": "32px",
                                         "border-style": "solid",
                                         "border-width" : "1px 1px 1px 1px",
                                         "border-radius": "10px",
                                         "text-decoration" : "none",
                                         "background-color": "#F3F9F1",
                                         "color": "black",
                                         "padding": "10px",
                                         "border-color": "#000000",
                                         "margin": "20px"
                                         })], style={"margin": "20px"}),
        multiple=False
        ),
      html.Div(id="tierTableDiv",
               children=[],
               style = {"margin": "100px"}
               ),
      html.Div(id="timeTableDiv",
               children=[],
               style = {"margin": "100px"}
               ),
       html.Div(id="tablesDiv", children=[html.P("tablesDiv")]),
       html.Div(id="messageDiv", children=[html.Span("")], style=dynamicDivStyle)
      ],
   ) # outermost div

    #---------------------------------------
    # uploaderWidget handler
    #---------------------------------------

@dash_app.callback(
    Output('messageDiv',      'children', allow_duplicate=True),
    Output('tablesDiv',       'children', allow_duplicate=True),
    Output('memoryStore',     'data'),
    Input('uploaderWidget',   'filename'),
    State('messageDiv',       'children'),
    State('uploaderWidget',   'contents'),
    State('uploaderWidget',   'last_modified'),
    State('memoryStore',      'data'),
    prevent_initial_call=True)
def uploadHandler(filename, messageDivContents, contents, date, data):
    if filename == None:
        raise PreventUpdate
    print("--- 2: messageDiv before adding new info")
    messageDivContents += [html.P(filename)]
    messageDivContents += [html.P(len(contents))]
    data = data or {'ignore': 99}    # creates a default data dict if needed
    data['eaf'] = filename
    xmlUtils = XmlFileUtils(filename, "/tmp", contents, verbose=True)
    localFile = xmlUtils.saveBytesToFile()
    data['localFile'] = localFile
    #result = xmlUtils.validElanXML()
    #data['valid'] = result['valid']
    formattedDate = datetime.datetime.fromtimestamp(date).strftime('%Y-%m-%d %H:%M:%S')
    data['fileDate'] = formattedDate
    filesize = len(contents)/1000
    data['fileSize'] = "%sk" % filesize
    testContentsForTablesDiv = [html.P("test contents")]
    success = True
    tierTable = html.Div(id="tierTable")
    timeTable = html.Div(id="timeTableDiv")

    print("--- about to call EafParser with %s" % data['localFile'])
    try:
       parser = EafParser(data['localFile'], verbose=True, fixOverlappingTimeSegments=False)
    except BaseException as e:
       success = False
       print("--- exception caught")
       print(e.args[2])
       messageDivContents = ["BaseException %s" % e.args[2]]
    print("--- after call to EafParser")
    print("--- value of success: %s" % success)
    if success:
       print("-- in the success block")
       tbl = parser.getTierTable()
       dashTable = dash_table.DataTable(tbl.to_dict('records'),
                                           [{"name": i, "id": i} for i in tbl.columns])
       tierTable = html.Div(id="tierTable",
                              children=[dashTable],
                              style = {"width": "1000px", "margin": "20",
                                        "border": "1px solid red"})
       tbl = parser.getTimeTable()
       print("--- time table shape")
       print(tbl.shape)
       dashTable = dash_table.DataTable(tbl.to_dict('records'),
                                          [{"name": i, "id": i} for i in tbl.columns],
                                           fixed_rows={'headers': True},
                                           style_table={'height': 400})
       timeTable = html.Div(id="timeTableDiv",
                              children=[dashTable],
                              style = {"width": "600px",
                                        "margin": "20",
                                        "border": "2px solid orange"})
    return messageDivContents, [tierTable, timeTable], data

    #---------------------------------------
    # displayStorageButton handler
    #---------------------------------------

@dash_app.callback(
    Output('messageDiv',          'children', allow_duplicate=True),
    Input('displayStorageButton', 'n_clicks'),
    State('messageDiv',           'children'),
    State('memoryStore',          'data'),
    prevent_initial_call=True)
def displayMemoryStore(buttonClicks, messageDivContents, data):
    if buttonClicks == 0:
        raise PreventUpdate
    el = html.Ul(id="list", children=[])
    for key in data.keys():
       el.children.append(html.Li("%s: %s" % (key, data[key])))
    messageDivContents += [el]
    return messageDivContents

    #---------------------------------------
    # clearMessagesButton handler
    #---------------------------------------

@dash_app.callback(
    Output('messageDiv',          'children', allow_duplicate=True),
    Input('clearMessagesButton',  'n_clicks'),
    prevent_initial_call=True)
def clearMessages(buttonClicks):
    if buttonClicks == 0:
        raise PreventUpdate
    messageDivContents =  html.Div(id="messageDiv", children=[html.Span("")])
    return messageDivContents


if __name__ == '__main__':
    print("=============================")
    print("starting main.py on port 80")
    port = 80
    app.run(host='0.0.0.0', debug=True, port=port)
    print("=============================")

