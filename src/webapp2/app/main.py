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

from slexil.xmlFileUtils import XmlFileUtils
from slexil.eafParser import EafParser
from slexil.tierGuide import TierGuide

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
dynamicDivStyle = {"width": 400,
                   "border": "1px solid darkblue",
                   "border-radius": 5,
                   "margin": 10,
                   "padding": 10}

majorButtonStyle = {"font-size": "24px",
                    "border-style": "solid",
                    "border-width" : "1px 1px 1px 1px",
                    "border-radius": "10px",
                    "text-decoration" : "none",
                    "background-color": "#F3F9F1",
                    "color": "black",
                    "padding": "10px",
                    "border-color": "#000000",
                    "margin": "20px",
                    "display": "flex"
                    }
actionButtonStyle = {"font-size": "24px",
                     "border-style": "dashed",
                     "border-width" : "1px 1px 1px 1px",
                     "border-radius": "10px",
                     "text-decoration" : "none",
                     "background-color": "#F3F9F1",
                     "color": "black",
                     "padding": "10px",
                     "border-color": "#000000",
                     "margin": "20px",
                     "display": "flex",
                     "height": "60px"
                     }


app = flask.Flask(__name__)

dashApp = Dash(__name__, server=app, url_base_pathname='/',
                external_stylesheets=external_stylesheets)

dashApp.title = "SLEXIL2 test"

# the dynamic div's children must be a list, so that it can be
# note that list += [newItem] is equivalent to list.append(newItem)

    #---------------------------------------
    # layout
    #---------------------------------------

dashApp.layout=html.Div(
   id='output',
   children=[
      html.Form(dcc.Input(id="foo", type="text"), id="foo_form"),
      html.H4('Project Name',style={'display':'inline-block','margin-right':20}),
      dcc.Input(id='projectNameInput',type='text',
                placeholder='enter convenient, concise text title here, no spaces please!',
                style={'display':'inline-block', 'font-size': "24px"}),
      html.Button("Set Project Name", id="setProjectNameButton", n_clicks=0),
      html.Div(id='supportsCallbackOnAppLoadDiv'),
      dcc.Store(id='memoryStore', storage_type='memory'),
      html.Button("Initialize Store",id='initializeStoreButton', n_clicks=0),
      #html.Button("Clear Messages",id='clearMessagesButton', n_clicks=0),
      html.Div(id="initializationDiv",
               style={"width": "300px", "height": "100px", "border": "1px solid darkGreen"}),
      html.Div(id="uploadButtonsDiv", style={"display": "flex"},
         children=[
               dcc.Upload(
                   id='eafUploaderWidget',
                   children=html.Div([html.A('Select EAF File', style=majorButtonStyle)],
                                     style={"margin": "20px"}),
                   multiple=False,
                   accept=".eaf"
                   ),
               dcc.Upload(
                   id='tierGuideUploaderWidget',
                   children=html.Div([html.A('Select Tier Guide File', style=majorButtonStyle)],
                                     style={"margin": "20px"}),
                   multiple=False,
                   accept=".yaml"
                   ),
             #dcc.Upload(
             #     id='grammaticalTerms_uploaderWidget',
             #     children=html.Div([html.A('Select Grammatical Terms File (optional)',
             #                               style=majorButtonStyle)],
             #                       style={"margin": "20px"}),
             #      multiple=False
             #      )
         ]),

      html.Div(id="actionDiv", style={"border": "0px solid red", "margin": "20px;"},
               children=[
                   html.Button("Create HTML File",id='createHtmlFileButton',
                               style=actionButtonStyle, n_clicks=0)
                   ]),

      html.Div(id="adminDiv", style={"border": "0px solid red",  "margin": "20px;"},
               children=[
                   html.Button("See Storage",id='displayStorageButton', n_clicks=0),
                   html.Button("Clear Messages",id='clearMessagesButton', n_clicks=0),
                   html.Div(id="messageDiv", children=[html.Span("")], style=dynamicDivStyle),
                   html.Div(id="tierTableDiv",
                            children=[],
                            style = {"margin": "100px"}
                            ),
                   html.Div(id="timeTableDiv",
                            children=[],
                            style = {"margin": "100px"}
                            ),
                   html.Div(id="tablesDiv", children=[],
                            style={"font-size": "18px",
                                   "margin": "10px",
                                   "padding": "10px"}
                                   ),
                   html.Div(id="tierGuideTableDiv",
                            children=[],
                            style = {"margin": "100px", "border": "1px blue"}
                            )
                   ])
      ],
 
   ) # outermost div

    #---------------------------------------
    # setProjectName button handler
    #---------------------------------------

@dashApp.callback(
    Output('messageDiv',        'children', allow_duplicate=True),
    Input('foo_form', 'formContents'),
    prevent_initial_call=True)
def handleProjectNameForm(formContents, messageDivContents):
    messageDivContents += [html.P("form contents: %s" % formContents)]
    return messageCivContents
    
    
@dashApp.callback(
    Output('messageDiv',        'children', allow_duplicate=True),
    Input('setProjectNameButton', 'n_clicks'),
    State('projectNameInput', 'value'),
    State('messageDiv',         'children'),
    prevent_initial_call=True)
def setProjectNameHander(n_clicks, projectName, messageDivContents):
    messageDivContents += [html.P("project name: %s" % projectName)]
    return messageDivContents

    #---------------------------------------
    # eafUploaderWidget handler
    #---------------------------------------

@dashApp.callback(
    Output('messageDiv',        'children', allow_duplicate=True),
    Output('tablesDiv',         'children', allow_duplicate=True),
    Output('memoryStore',       'data'),
    Input('eafUploaderWidget',  'filename'),
    State('messageDiv',         'children'),
    State('eafUploaderWidget',  'contents'),
    State('eafUploaderWidget',  'last_modified'),
    State('memoryStore',        'data'),
    prevent_initial_call=True)
def eafUploadHandler(filename, messageDivContents, contents, date, data):
    print('entering eafUploadHandler')
    if filename == None:
        raise PreventUpdate
    print("--- 2: messageDiv before adding new info")
    messageDivContents += [html.P("eaf file: %s" % filename)]
    messageDivContents += [html.P("eaf file size: %d" % len(contents))]
    data = data or {'ignore': 99}    # creates a default data dict if needed
    data['eaf'] = filename
    xmlUtils = XmlFileUtils(filename, "/tmp", contents, verbose=True)
    localFile = xmlUtils.saveBytesToFile()
    data['eafLocalFile'] = localFile
    #result = xmlUtils.validElanXML()
    #data['valid'] = result['valid']
    formattedDate = datetime.datetime.fromtimestamp(date).strftime('%Y-%m-%d %H:%M:%S')
    data['eafFileDate'] = formattedDate
    filesize = len(contents)/1000
    data['eafFileSize'] = "%sk" % filesize
    testContentsForTablesDiv = [html.P("test contents")]
    success = True
    tierTable = html.Div(id="tierTable")
    timeTable = html.Div(id="timeTableDiv")

    print("--- about to call EafParser with %s" % data['eafLocalFile'])
    try:
       parser = EafParser(data['eafLocalFile'], verbose=True, fixOverlappingTimeSegments=False)
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
                              style = {"width": "100%", "margin": "20",
                                        "border": "2px solid red"})
       # not using the times table for now
       #tbl = parser.getTimeTable()
       #print("--- time table shape")
       #print(tbl.shape)
       #dashTable = dash_table.DataTable(tbl.to_dict('records'),
       #                                   [{"name": i, "id": i} for i in tbl.columns],
       #                                    fixed_rows={'headers': True},
       #                                    style_table={'height': 400})
       #timeTable = html.Div(id="timeTableDiv",
       #                       children=[dashTable],
       #                       style = {"width": "600px",
       #                                 "margin": "20",
       #                                 "border": "2px solid orange"})
       timeTable = html.Div(id="timeTableDiv")
    return messageDivContents, [tierTable, timeTable], data



    #---------------------------------------
    # tierGuideUploaderWidget handler
    #---------------------------------------

@dashApp.callback(
    Output('messageDiv',      'children', allow_duplicate=True),
    Output('tierGuideTableDiv',         'children', allow_duplicate=True),
    Output('memoryStore',     'data',     allow_duplicate=True),
    Input('tierGuideUploaderWidget', 'filename'),
    State('messageDiv',       'children'),
    State('tierGuideUploaderWidget',   'contents'),
    State('tierGuideUploaderWidget',   'last_modified'),
    State('memoryStore',      'data'),
    prevent_initial_call=True)
def tierGuideUploadHandler(filename, messageDivContents, contents, date, data):
    if filename == None:
        raise PreventUpdate
    print("--- 2: messageDiv before adding new info")
    messageDivContents += [html.P("tierGuide file: %s" % filename)]
    messageDivContents += [html.P("tierGuide size: %d" % len(contents))]
    data = data or {'ignore': 99}    # creates a default data dict if needed
    data['tierGuideFile'] = filename
    xmlUtils = XmlFileUtils(filename, "/tmp", contents, verbose=True)
    localFile = xmlUtils.saveBytesToFile()
    data['tierGuideLocalFile'] = localFile
    formattedDate = datetime.datetime.fromtimestamp(date).strftime('%Y-%m-%d %H:%M:%S')
    data['tierGuideFileDate'] = formattedDate
    messageDivContents += [html.P("local tier guide file: %s" % localFile)]
    try:
       tg = TierGuide(localFile)
       tgg = tg.getGuide()
       tggAsString = json.dumps(tgg)
       messageDivContents += [html.P(tggAsString)]
       tierGuideTableDiv = html.Div(html.P(tggAsString))
       messageDivContents += [html.P("after creating tierGuideTableDiv")]
    except BaseException as e:
       success = False
       print("--- tier guide exception caught")
       print(e)
       messageDivContents = ["BaseException %s" % e.args[2]]
       tierGuideTableDiv = html.Div(id="tierGuideTable")
    print(tgg)


#     #filesize = len(contents)/1000
#     #data['fileSize'] = "%sk" % filesize
#     #testContentsForTablesDiv = [html.P("test contents")]
#     #success = True
#     #tierTable = html.Div(id="tierTable")
#     #timeTable = html.Div(id="timeTableDiv")
    return messageDivContents, [tierGuideTableDiv], data


    #------------------------------
    # initializeStoreButton
    #------------------------------

@dashApp.callback(
    Output('memoryStore',          'data', allow_duplicate=True),
    Input('initializeStoreButton', 'n_clicks'),
    State('memoryStore',           'data'),
    prevent_initial_call=True)
def initializeStore(buttonClicks, data):
    print("--- initializeStore")
    data = {'ignore': 99}    # creates a default data dict if needed
    # data['eaf'] = "fubar"
    # data['eafLocalFile'] = "fubar"
    # data['eafFileDate'] = "fubar"
    #data['eafFileSize'] = "fubar"

    #initializeDivContents += [html.P("initializing store")]
    return data


    #------------------------------
    # createHtmlFileButton hndler
    #------------------------------

@dashApp.callback(
    Output('messageDiv',          'children', allow_duplicate=True),
    Input('createHtmlFileButton', 'n_clicks'),
    State('messageDiv',           'children'),
    State('memoryStore',          'data'),
    prevent_initial_call=True)
def createHtmlFile(buttonClicks, messageDivContents, data):
    print("--- createHtmlFile")
    messageDivContents += [html.P("about to create html file")]
    messageDivContents += [html.P("eaf: %s" % data['eafLocalFile'])]
    return messageDivContents


    #---------------------------------------
    # displayStorageButton handler
    #---------------------------------------

@dashApp.callback(
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

@dashApp.callback(
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
