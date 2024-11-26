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
import dash_bootstrap_components as dbc

import pandas as pd
slexil_webapp_version = "2.0.0"
from slexil.yamlToText import YamlToText


#--------------------------------------------------------------------------------
PROJECTS_DIRECTORY = "PROJECTS"
try:
    assert (os.path.exists(PROJECTS_DIRECTORY))
except AssertionError:
    os.mkdir(PROJECTS_DIRECTORY)
#--------------------------------------------------------------------------------
uploaderStyle = {'width': '60%',
                 'height': '60px',
                 'lineHeight': '60px',
                 'borderWidth': '1px',
                 'borderStyle': 'solid',
                 'borderRadius': '5px',
                 'textAlign': 'center',
                 'fontSize': '24px',
                 'margin': '10px',
                 'marginLeft': '100px',
                 'display': 'none'
                 }

simpleTextDisplayStyle = {'fontSize': '32px',
                          'marginLeft': '200px'
                          }
external_stylesheets = [dbc.themes.BOOTSTRAP,
                        'https://codepen.io/chriddyp/pen/bWLwgP.css']

app = flask.Flask(__name__)
dashApp = dash.Dash(__name__, server = app, url_base_pathname = '/', 
                    external_stylesheets=external_stylesheets)
dashApp.title = 'slexil new'

errorBox = dbc.Modal([
    dbc.ModalHeader(dbc.ModalTitle("Error")),
    dbc.ModalBody("An error occurred."),
    ], id="errorBox", is_open=False)

dashApp.layout = html.Div([
    dcc.Store(id="globals", data={'slexil initialized': slexil_webapp_version}),
    errorBox,
    html.H1("Sləxil",
             style={"textAlign": "left", "marginLeft": "20px"}),
    html.Div(id="titleDiv",
             children=[html.Span("Title: ",
                                 style={"marginLeft": "20px", "fontSize": "24px"}),
                       dcc.Input(id="titleInput",
                                 type='text',
                                 debounce=True,
                                 placeholder='<return> to assign',
                                 value="",
                                 className="titleInput",
                                 style={"fontSize": "24px", "width": "800px"}),
                       html.Button('Submit',
                             id='saveTitleButton',
                             className="button",
                                   disabled=False)
                       ]),
    html.Div(id="fileTypeChooser",
             style={'margin': '20px', 'fontSize': '24px',
                    'display': 'inline-block', 'marginRight': '10px'},
             children=[html.Span("Input File Type? ",
                                 id="inputFileTypePrompt",
                                 style={'color': 'lightgray'}
                                 ),
                       dcc.RadioItems(id="fileTypeRadioButtons",
                                      options=[
                                          {'label': 'EAF', 'value': 'EAF', 'disabled': True},
                                          {'label': 'YAML', 'value': 'YAML', 'disabled': True}
                                         ],
                                      inline=True,
                                      style={'display': 'inline-block',
                                             "color": "lightgray"}),
                                      # disabled=True),
                       dcc.Upload(
                           id='mainTextUploader',
                           children=html.Div([
                               'Drag and Drop or ',
                               html.A('Select File')
                           ]),
                           style=uploaderStyle,
                           multiple=False
                       ),
                       html.Div(id='eafFilename-display',
                                style=simpleTextDisplayStyle),
                       ]),

    dcc.Upload(
        id='grammaticalTermsFilename-select',
        children=html.Div([
            'grammaticalTerms.yaml: Drag and Drop or ',
            html.A('Select File')
            ]),
        style=uploaderStyle,
        multiple=False
        ),
    html.Div(id="buttonDiv",
             style={"margin": "20px"},
             children=[
                 html.Button('Create HTML',
                             id='createHtmlButton',
                             className="button",
                             disabled=True), 
                 html.Div(id="download-html-div",
                          children=[html.Button("Download HTML",
                                                id="downloadHtmlButton",
                                                className="button",
                                                disabled=True),
                                    dcc.Download(id="download-html")],
                          style={"display": "inline-block"}),
                 html.Div(id="download-yaml-div",
                          children=[html.Button("Download YAML",
                                                id="btn-download-txt",
                                                className="button",
                                                disabled=True),
                                    dcc.Download(id="download-yaml")],
                          style={"display": "inline-block"}),
                 html.Button("Display State",
                             id='displayStateButton',
                             className="button")
                 ]),
    html.Div(id='grammaticalTermsFilename-display',
             style=simpleTextDisplayStyle),
    html.Div(id='message-div', style={'height': '400px', 'width': "90%",
                                      'border': '1px solid black',
                                      'borderRadius': '10px',
                                      'margin': '20px',
                                      'padding': '10px',
                                      'fontSize': '24px',
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
    

@dashApp.callback(Output('globals', 'data', allow_duplicate=True),
                  Output('mainTextUploader', 'style'),
                  Input('fileTypeRadioButtons', 'value'),
                  State('message-div', 'children'),
                  State('globals', 'data'),
                  prevent_initial_call=True)
def handleFileTypeSelection(fileType, currentMessageContents, globals):
    print("handleFileTypeSelection: %s" % fileType)
    newText = dcc.Markdown("- input file type: %s" % fileType)
    mainTextUploaderStyle = {'display': 'inline-block'}
    globals['fileType'] = fileType
    return globals, mainTextUploaderStyle


def handleFileTypeSelection(fileType, currentMessageContents):
    print("handleFileTypeSelection: %s" % fileType)
    if currentMessageContents is None:
        currentMessageContents = []
    currentMessageContents.append(fileType)
    return currentMessageContents, {'fileType': fileType}


@dashApp.callback(Output('globals', 'data', allow_duplicate=True),
                  #Output('createHtmlButton', 'disabled'),
                  Output('fileTypeRadioButtons', 'options'),
                  Output('fileTypeRadioButtons', 'style'),
                  Output('inputFileTypePrompt', 'style'),
                  Input('titleInput', 'value'),
                  State('globals', 'data'),
                  prevent_initial_call=True)
def saveProjectName(projectTitle, globals):
    projectName = projectTitle.replace(" ", "")
    print("--- projectName: %s" % projectName)
    #pdb.set_trace()
    globals['projectTitle'] = projectTitle
    globals['projectName'] = projectName
    enabledRadioButtonOptions=[
        {'label': 'EAF', 'value': 'EAF', 'disabled': False},
        {'label': 'YAML', 'value': 'YAML', 'disabled': False}
        ]
    radioButtonStyle = {'color': 'black', 'display': 'inline-block'}
    inputFileTypePromptStyle = {'color': 'black'}
    
    return globals, enabledRadioButtonOptions, radioButtonStyle, inputFileTypePromptStyle

    

@dashApp.callback(Output('createHtmlButton', 'disabled'),
                  Output('globals', 'data', allow_duplicate=True),
                  Output('errorBox', 'is_open'),
                  Output('errorBox', 'children'),
                  Input('mainTextUploader', 'contents'),
                  State('mainTextUploader', 'filename'),
                  State('mainTextUploader', 'last_modified'),
                  State('globals', 'data'),
                  prevent_initial_call=True)

def handleMainTextUploadAndEafParse(contents, filename, date, globals):

    globals['mainTextFilename'] = filename
    projectName = globals['projectName']
    projectTitle = globals['projectTitle']
    projectDirectory = os.path.join(PROJECTS_DIRECTORY, projectName)
    mainTextFilePath = os.path.join(projectDirectory, filename)
    globals['mainTextFilePath'] = mainTextFilePath

      # expected return values
    errorBoxOpen = False
    errorBoxChildren = None
    createHtmlButton = True

    try: 
        saveUploadedFile(contents, projectName, filename)

        fileType = globals['fileType']
        print("%s has format %s" % (filename, fileType))
        if fileType == "EAF":
            p = EafParser(mainTextFilePath, verbose=False, fixOverlappingTimeSegments=False)
            p.run()
            title = globals['projectTitle'] = projectTitle
            yamlText = p.toYAML(projectTitle, projectName, projectName)
            yamlFileName = os.path.join(projectDirectory, "%s.yaml" % projectName)
            p.writeYAML(yamlText, yamlFileName)
            globals['yamlFileName'] = yamlFileName
            #pdb.set_trace()
            tbl = p.getTierTable()
            globals['tiers'] = list(tbl['TIER_ID'])
            globals['time aligned'] = list(tbl['TIME_ALIGNABLE'])
            globals['parent'] = list(tbl['PARENT_REF'])
            globals['lineCount'] = list(tbl['LINES'])
            print(p.getTierTable())
            if fileType == "YAML":
                globals['yamlFileName'] = mainTextFilePath

    except Exception as e:
       errorBoxOpen = True
       errorBoxChildren = dbc.ModalBody("error!")
       createHtmlButton = False
       return createHtmlButton, globals, errorBoxOpen, errorBoxChildren
       
    return createHtmlButton, globals, errorBoxOpen, errorBoxChildren
   
#--------------------------------------------------------------------------------
def saveUploadedFile(contents, projectName, filename):

   data = contents.encode("utf8").split(b";base64,")[1]
   print("len(data) = %d" %len(data))

   targetDirectory = os.path.join(PROJECTS_DIRECTORY, projectName)
   if (not os.path.exists(targetDirectory)):
        os.mkdir(targetDirectory)
   newFile = os.path.join(targetDirectory, filename)

   with open(newFile, "wb") as fp:
      fp.write(base64.decodebytes(data))
   print("Filename: %s" % newFile)
   assert(os.path.isfile(newFile))

#--------------------------------------------------------------------------------
# 
# @dashApp.callback(Output('message-div', 'children'),
#                   Input('yamlFilename-select', 'contents'),
#                   State('yamlFilename-select', 'filename'),
#                   State('yamlFilename-select', 'last_modified'),
#                   State('message-div', 'children'),
#                   prevent_initial_call=True)
# def update_output(contents, filename, date, currentMessageContents):
#     if(contents is not None):
#        if currentMessageContents is None:
#            currentMessageContents = []
#        newText = dcc.Markdown('''
#          - YAML: %s
#          - date: 19 nov 2024
#          ''' % (filename))
# 
#        currentMessageContents.append(newText)
#        return currentMessageContents
# 
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
    State("globals", "data"),
    prevent_initial_call=True,
    )
def download_html(n_clicks, globals):
    filename = os.path.join(PROJECTS_DIRECTORY,
                            globals['projectName'],
                            "%s.html" % globals['projectName'])
    return dcc.send_file(filename)


@dashApp.callback(Output('globals', 'data', allow_duplicate=True),
                  Output('downloadHtmlButton', 'disabled'),
                  [Input('createHtmlButton', 'n_clicks')],
                  State('globals', 'data'),
                  prevent_initial_call=True)
def createHtml(n_clicks, globals):
   print("--- runSlexil, n_clicks: %d" % n_clicks)

   title = globals['projectTitle']
   projectName = globals['projectName']
   projectDirectory = os.path.join(PROJECTS_DIRECTORY, globals['projectName'])
   fileType = globals['fileType']
   if fileType == "YAML":
      yamlFileName = globals['mainTextFilePath']
   elif fileType == "EAF":
      yamlFileName = globals['yamlFileName']
   htmlFileName = createHtmlFromYaml(yamlFileName, title,
                                     projectName, projectDirectory)
   globals['htmlFileName'] = htmlFileName
   return globals, False
        
def createHtmlFromEAF(eafFile, title, projectName, projectDirectory):

   #p = EafParser(eafFile, verbose=False, fixOverlappingTimeSegments=False)
   #p.run()
   #yamlText = globals['yamlText'] #p.toYAML(title, projectName, projectName)
   #yamlFileName = os.path.join(projectDirectory, "%s.yaml" % projectName)
   #p.writeYAML(yamlText, yamlFileName)
   yamlFileName = globals['yamlFileName']
   return(createHtmlFromYaml(yamlFileName, title, projectName, projectDirectory))

def createHtmlFromYaml(yamlFile, title, projectName, projectDirectory):

   text = YamlToText(yamlFile,
                     grammaticalTerms=[],
                     projectDirectory=projectDirectory,
                     verbose = False,
                     fontSizeControls = True,
                     startLine = None,
                     endLine = None,
                     pageTitle = title,
                     helpFilename = None,
                     helpButtonLabel = None,
                     kbFilename = None,
                     linguisticsFilename = None,
                     fixOverlappingTimeSegments = False,
                     webpackLinksOnly=False,
                     useTooltips=False)
   htmlText = text.toHTML()
   htmlFileName = os.path.join(projectDirectory, "%s.html" % projectName)
   print("--- writing html file for at %s" % htmlFileName)
   with open(htmlFileName, "w") as file:
       file.write(htmlText)
   return htmlFileName


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

        
