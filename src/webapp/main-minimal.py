import base64
import datetime
import io
import os 
import slexil
from text import *
import pdb

import flask
import dash
from dash.dependencies import Input, Output, State
from dash import dcc, html, dash_table

import pandas as pd
slexil_webapp_version = "2.0.0"

buttonStyle = {'font-size': '24px',
               'color': 'red'}

uploaderStyle = {'width': '60%',
                 'height': '60px',
                 'lineHeight': '60px',
                 'borderWidth': '1px',
                 'borderStyle': 'solid',
                 'borderRadius': '5px',
                 'textAlign': 'center',
                 'font-size': '24px',
                 'margin': '10px',
                 'margin-left': '100px',
                 'display': 'none'
                 }

simpleTextDisplayStyle = {'font-size': '32px',
                          'margin-left': '200px'
                          }
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = flask.Flask(__name__)
dashApp = dash.Dash(__name__, server = app, url_base_pathname = '/', 
                    external_stylesheets=external_stylesheets)
dashApp.title = 'slexil new'

@app.route('/PROJECTS/<path:urlpath>')
def openPreview(urlpath):
    print("--- urlpath: %s" % urlpath)
    fullPath = os.path.join("PROJECTS", urlpath)
    return flask.send_file(os.path.join(fullPath))
        


dashApp.layout = html.Div([
    dcc.Store(id="globals", data={'slexil initialized': slexil_webapp_version}),
    html.H1("Sləxil",
             style={"text-align": "left", "margin-left": "20px"}),
    html.Div(id="titleDiv",
             children=[html.Span("Title: ",
                                 style={"margin-left": "20px", "fontSize": "24px"}),
                       dcc.Input(id="titleInput",
                                 type='text',
                                 debounce=True,
                                 placeholder='',
                                 value="",
                                 className="titleInput",
                                 style={"fontSize": "24px", "width": "800px"})
                       ]),
    html.Div(id="fileTypeChooser",
             style={'margin-left': '20px', 'fontSize': '24px',
                    'display': 'inline-block', 'margin-right': '10px'},
             children=[html.Span("Input File Type? "),
                       dcc.RadioItems(id="fileTypeRadioButtons",
                                      options=['EAF', 'YAML'],
                                      inline=True,
                                      style={'display': 'inline-block',
                                             "color": "green"}), #]),
    dcc.Upload(
        id='eafFilename-select',
        children=html.Div([
            'EAF: Drag and Drop or ',
            html.A('Select File')
            ]),
        style=uploaderStyle,
        multiple=False
        ),
    html.Div(id='eafFilename-display',
             style=simpleTextDisplayStyle),
    dcc.Upload(
        id='yamlFilename-select',
        children=html.Div(
            children=['YAML: Drag and Drop or ', html.A('Select File')]
             ),
        style=uploaderStyle,
        multiple=False
        )]),

    dcc.Upload(
        id='grammaticalTermsFilename-select',
        children=html.Div([
            'grammaticalTerms.yaml: Drag and Drop or ',
            html.A('Select File')
            ]),
        style=uploaderStyle,
        multiple=False
        ),
    html.Button('Create HTML', id='createHtmlButton', className="button",
                disabled=False, style=buttonStyle),
    html.Div(id="download-html-div",
             children=[html.Button("Download HTML", id="downloadHtmlButton",
                                   style={"font-size": "18px"}),
                       dcc.Download(id="download-html")]),
    html.Div(id="download-yaml-div",
             children=[html.Button("Download YAML", id="btn-download-txt",
                                   style={"font-size": "18px"}),
                       dcc.Download(id="download-yaml")]),
    html.Button("Display State", id='displayStateButton', className="submit",
                style={"font-size": "18px"}),
    html.Div(id='grammaticalTermsFilename-display',
             style=simpleTextDisplayStyle),
    html.Div(id='message-div', style={'height': '400px', 'width': "90%",
                                      'border': '1px solid black',
                                      'border-radius': '10px',
                                      'margin': '20px',
                                      'padding': '10px',
                                      'font-size': '24px',
                                      'overflow': 'auto'}),
    html.Div(id='hidden-div', style={'display':'none'})])



#--------------------------------------------------------------------------------
@dashApp.callback(Output('message-div', 'children', allow_duplicate=True),
                  Input('displayStateButton', 'n_clicks'),
                  # State('message-div', 'children'),
                  State('globals', 'data'),
                  prevent_initial_call=True)
def handleDisplayStateButton(n_clicks, globals): #currentMessageContents, globals):
    print("handleDisplayStateButton: %d" % n_clicks)
    currentMessageContents = []   # clears the message box
    print(globals)
    newText = dcc.Markdown("- display state requested")
    keys = globals.keys()
    currentMessageContents.append(dcc.Markdown("**State**"))
    for key in keys:
       newText = dcc.Markdown("   - %s: %s" % (key, globals[key]))
       currentMessageContents.append(newText)

    return currentMessageContents
    

@dashApp.callback(#Output('message-div', 'children', allow_duplicate=True),
                  Output('globals', 'data', allow_duplicate=True),
                  Output('eafFilename-select', 'style'),
                  Output('yamlFilename-select', 'style'),
                  Input('fileTypeRadioButtons', 'value'),
                  State('message-div', 'children'),
                  State('globals', 'data'),
                  prevent_initial_call=True)
def handleFileTypeSelection(fileType, currentMessageContents, globals):
    print("handleFileTypeSelection: %s" % fileType)
    if currentMessageContents is None:
        currentMessageContents = []
    newText = dcc.Markdown("- input file type: %s" % fileType)
    currentMessageContents.append(newText)
    if fileType == "EAF":
       newEafStyle = {'display': 'inline-block'}
       newYamlStyle = {'display': 'none'}
    else:
       newEafStyle = {'display': 'none'}
       newYamlStyle = {'display': 'inline-block'}

    globals['fileType'] = fileType
    #return currentMessageContents, globals, newEafStyle, newYamlStyle
    return globals, newEafStyle, newYamlStyle


def handleFileTypeSelection(fileType, currentMessageContents):
    print("handleFileTypeSelection: %s" % fileType)
    if currentMessageContents is None:
        currentMessageContents = []
    currentMessageContents.append(fileType)
    return currentMessageContents, {'fileType': fileType}


@dashApp.callback(Output('globals', 'data', allow_duplicate=True),
                  Input('titleInput', 'value'),
                  State('globals', 'data'),
                  prevent_initial_call=True)
def saveProjectName(projectTitle, globals):
    projectName = projectTitle.replace(" ", "")
    print("--- projectName: %s" % projectName)
    #pdb.set_trace()
    globals['projectTitle'] = projectTitle
    globals['projectName'] = projectName
    return globals

    
@dashApp.callback(Output('message-div', 'children', allow_duplicate=True),
                  Input('eafFilename-select', 'contents'),
                  State('eafFilename-select', 'filename'),
                  State('eafFilename-select', 'last_modified'),
                  State('message-div', 'children'),
                  prevent_initial_call=True)

def handleEafUpload(contents, filename, date, currentMessageContents):
    if(contents is not None):
       if currentMessageContents is None:
           currentMessageContents = []
       saveEAF(contents, filename)
       newText = dcc.Markdown('''
         - EAF: %s
         - date: 19 nov 2024
         ''' % (filename))
       currentMessageContents.append(newText)
       return currentMessageContents
   
#--------------------------------------------------------------------------------
def saveEAF(contents, filename):

   print("--- stub for parsing and saving %s" % filename)
   data = contents.encode("utf8").split(b";base64,")[1]
   print("len(data) = %d" %len(data))
   filepath = os.path.join("./", filename)
   with open(filename, "wb") as fp:
        fp.write(base64.decodebytes(data))
   print("Filename: %s" %filename)
   assert(os.path.isfile(filename))

          

#--------------------------------------------------------------------------------
@dashApp.callback(Output('message-div', 'children'),
                  Input('yamlFilename-select', 'contents'),
                  State('yamlFilename-select', 'filename'),
                  State('yamlFilename-select', 'last_modified'),
                  State('message-div', 'children'),
                  prevent_initial_call=True)
def update_output(contents, filename, date, currentMessageContents):
    if(contents is not None):
       if currentMessageContents is None:
           currentMessageContents = []
       newText = dcc.Markdown('''
         - YAML: %s
         - date: 19 nov 2024
         ''' % (filename))

       currentMessageContents.append(newText)
       return currentMessageContents

#--------------------------------------------------------------------------------
@dashApp.callback(Output('grammaticalTermsFilename-display', 'children'),
              Input('grammaticalTermsFilename-select', 'contents'),
              State('grammaticalTermsFilename-select', 'filename'),
              State('grammaticalTermsFilename-select', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if(list_of_contents is not None):
       print("update_output")
       print("names: %s" % list_of_names)
       children = list_of_names
       return children
#--------------------------------------------------------------------------------
@dashApp.callback(
    Output("download-html", "data"),
    Input("downloadHtmlButton", "n_clicks"),
    prevent_initial_call=True,
    )
def download_html(n_clicks):
    return dcc.send_file("PROJECTS/fubar.html")


@dashApp.callback(Output('globals', 'data', allow_duplicate=True),
                  [Input('createHtmlButton', 'n_clicks')],
                  State('globals', 'data'),
                  prevent_initial_call=True)
def runSlexil(n_clicks, globals):
    print("--- runSlexil, n_clicks: %d" % n_clicks)
    if(not n_clicks == None):
       print("runSlexil: %d" % n_clicks)
       slexil_msg = runSlexilDemo()
       globals['htmlCreationMessage'] = slexil_msg
       return globals
   
#@dashApp.callback(Output('hidden-div', 'children'),
#                  [Input('previewHtmlButton', 'n_clicks')],
#                  prevent_initial_call=True)
#def previewHTML(n_clicks):
#    print(" previewHTML callback, n_clicks: %d" % n_clicks)
    

#@dashApp.callback(Output('previewLink', 'href', allow_duplicate=True),
#                  [Input('displayHTMLButton', 'n_clicks')],
#                  prevent_initial_call=True)
#def displayHTML(n_clicks):
#         print("displayHTMLButton callback, n_clicks: %d" % n_clicks)
#         return("http://localhost:8050/PROJECTS/fubar.html")
## see https://stackoverflow.com/questions/75725718/redirect-to-a-url-in-dash

#@dashApp.callback(Output('hidden-div', 'children', allow_duplicate=True),
#                  [Input('downloadHTMLButton', 'n_clicks')],
#                  prevent_initial_call=True)
#def downloadHTML(n_clicks):
#               print("downloadHTML")

# html.Button("Display",   id='displayHTMLButton',  n_clicks=0, className="btn"),
# html.Button("Download",  id="downloadHTMLButton", n_clicks=0, className="btn"),




def runSlexilDemo():
    print("--- running slexil demo")
    projectDirectory = "PROJECTS"
    dataDir = "/Users/paul/github/slexil2/testData/inferno"
    elanXmlFilename = os.path.join(dataDir, "inferno-threeLines.eaf")
    tierGuideFile = os.path.join(dataDir, "tierGuide.yaml")
    grammaticalTermsFile = os.path.join(dataDir, "grammaticalTerms.txt")
    fontSizeControls = False
    startLine = None
    endLine = None
    kbFilename = None
    linguisticsFilename = None

    text = Text(elanXmlFilename,
                grammaticalTermsFile=grammaticalTermsFile,
                tierGuideFile=tierGuideFile,
                projectDirectory=projectDirectory,
                verbose=True,
                fontSizeControls = fontSizeControls,
                startLine = startLine,
                endLine = endLine,
                pageTitle = "title",
                helpFilename = None,
                helpButtonLabel = None,
                kbFilename = kbFilename,
                linguisticsFilename = linguisticsFilename,
                fixOverlappingTimeSegments = False)

    # print(text.getTierSummary())
    htmlDoc = text.toHTML()
    webpageAt = "PROJECTS/fubar.h"
    absolutePath = os.path.abspath(webpageAt)
    print("webpageAt: %s" % webpageAt)
    with open(absolutePath, "w") as file:
        file.write(htmlDoc)
        file.close()

    return(webpageAt)

if __name__ == '__main__':
    dashApp.run_server(debug=True)

        
