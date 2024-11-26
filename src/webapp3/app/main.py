import flask
import time
import pdb
import slexil
from datetime import datetime
import base64
import json
import zipfile
import os, io, traceback, time
from dash import html, Dash, callback, dcc, Input, Output, State, dash_table
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify
from slexil.eafParser import EafParser
appVersion = "2.6.0"
versionString = "slexil %s, app %s" % (slexil.__version__, appVersion)
dbcStyle = dbc.themes.BOOTSTRAP
styleSheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', dbcStyle]

app = flask.Flask(__name__)
dashApp = Dash(__name__, server=app, url_base_pathname='/',
               external_stylesheets=styleSheets)
dashApp.title = "Slexil 3"

PROJECTS_DIR = "PROJECTS"

#--------------------------------------------------------------------------------
def runBigDemo():

  projectPath = os.path.join(PROJECT_DIR, "timingTest")
  fullPath = os.path.join(projectPath, "4EthelAnita230503Slexil.eaf")
  htmlFile = createWebPage(fullPath, projectPath, "timingTest")
  
#--------------------------------------------------------------------------------
@app.route('/test')
def runTest():

   startTime = time.time()
   runBigDemo()
   endTime = time.time()
   elapsedTime = endTime - startTime
   currentTime = time.ctime()
   msg = "[%s] ran slexil webapp2 demo in %s seconds\n" % \
       (time.ctime(), round(elapsedTime, 2))
   print(msg)
   return msg

#--------------------------------------------------------------------------------
@app.route('/PROJECTS/<path:urlpath>')
def serveFile(urlpath):
    print("=== entering serveFile app.server.route: %s" % urlpath)
    fullPath = os.path.join("PROJECTS", urlpath)
    dirname = os.path.dirname(fullPath)
    filename = os.path.basename(fullPath)
    print("---- %s" % fullPath)

    if urlpath[-4:] == "html":
       print("=== populate textArea from %s" % urlpath)
       return flask.send_file(os.path.join(fullPath))
    elif urlpath[-3:] == "wav":
       print("flask route returning %s" % fullPath)
       return flask.send_file(os.path.join(fullPath))
    elif urlpath[-3:] == "zip":
       print("flask route returning %s" % fullPath)
       return flask.send_file(os.path.join(fullPath), mimetype='application/zip')
    else:
       return ""
    
#--------------------------------------------------------------------------------
basicButtonStyle = {'font-size': '24px',
                    'fontFamily': 'New York Times-Roman',
                    'border': '1px solid black',
                    'border-radius': '10px'}

buttonStyle = {"margin": "15px",
              "fontSize": "20px",
              "border": "1px solid gray",
              "borderRadius": "10px"
              }
#--------------------------------------------------------------------------------
# the webapp requires a PROJECTS_DIRECTORY in the current working directory
# each individual project, one for each text, is created as a subdirectory here
PROJECTS_DIRECTORY = "PROJECTS"
try:
    assert(os.path.exists(PROJECTS_DIRECTORY))
except AssertionError:
    os.mkdir(PROJECTS_DIRECTORY)
#--------------------------------------------------------------------------------
# eafDir = "eafs"
# files = os.listdir(eafDir)
# eafFiles = [f for f in files if f.endswith("eaf")]
# eafFiles.sort()
# print("eaf count: %d" % len(eafFiles))
#-------------------------------------------------------
modalDiv = html.Div(
    [dbc.Modal([
         dbc.ModalHeader(
            dbc.ModalTitle("SLEXIL Notification", id="modalTitle"), close_button=True),
         dbc.ModalBody("", id='modalContents', style={"fontSize": "24px"}),
         dbc.ModalFooter(
            dbc.Button("Close", id="modalCloseButton", className="ms-auto", n_clicks=0))
         ],
         id="slexilModal",
         centered=True,
         is_open=False,
         style={'font-size': '30px'},
         size="xl",    # sm, lg, xl
         fullscreen=False,
         scrollable=True,
         )])
#-------------------------------------------------------
loadTrackerDiv = html.Div(id="loadTrackerDiv")
modalLoadSpinnerWatcher = dcc.Loading(id="modalLoadWatcher",
                                      type="default",
                                      children=[modalDiv])
#-------------------------------------------------------
def createDropdownMenu():

   dropdown = dbc.DropdownMenu(
      label="About",
      id="aboutDropdownMenu",
      align_end=True,
      size="sm",
      children=[
         dbc.DropdownMenuItem(versionString,
                              id="versionLabelPseudoButton",
                              class_name="menuItemClass"),
         dbc.DropdownMenuItem("Media URLs",
                              id="explainMediaURLsButton",
                              class_name="menuItemClass"),
         dbc.DropdownMenuItem("Glossing Abbreviations",
                              id="explainGlossingAbbreviationsButton",
                              class_name="menuItemClass"),
         dbc.DropdownMenuItem("Examine State",
                              id="examineStateButton",
                              class_name="menuItemClass"),
         ])

   return dropdown

#-------------------------------------------------------
def get_exception_traceback_str(exc: Exception) -> str:
    # Ref: https://stackoverflow.com/a/76584117/
    file = io.StringIO()
    traceback.print_exception(exc, file=file)
    return file.getvalue().rstrip()
#-------------------------------------------------------
globals = dcc.Store(id="globals", data={'slexil initialized': appVersion})
dashApp.layout = html.Div(id="mainDiv",
               children=[globals,
                         html.Div(id="bannerDiv", 
                                  children=createDropdownMenu(),
                                  ),
                         loadTrackerDiv,
                         modalLoadSpinnerWatcher],
                      style={"margin": "5px"})
#----------------------------------------------------------------------
# navbar button displays state in a modal dialog
@callback(
    Output('slexilModal', 'is_open', allow_duplicate=True),
    Output('modalTitle', 'children', allow_duplicate=True),
    Output('modalContents', 'children', allow_duplicate=True),
    Input('examineStateButton', 'n_clicks'),
    State('globals', 'data'),
    prevent_initial_call=True
    )
def displayStateAsList(n_clicks, globals):
    #pdb.set_trace()
    if globals is None:
       return(True, "State Variables",
              html.P("state is empty, no variables yet assigned"))
    el = html.Ul(id="list", children=[])
    for key in globals.keys():
       el.children.append(html.Li("%s: %s" % (key, globals[key])))
    return True, "State Variables", el
#--------------------------------------------------------------------------------
# explain how media URLs work, how and why you might change them
@callback(
    Output('slexilModal', 'is_open', allow_duplicate=True),
    Output('modalTitle', 'children', allow_duplicate=True),
    Output('modalContents', 'children', allow_duplicate=True),
    Input('explainMediaURLsButton', 'n_clicks'),
    State('globals', 'data'),
    prevent_initial_call=True
    )
def displayStateAsList(n_clicks, data):
    el = html.Ul(id="list", children=[])
    items = ["In most ELAN files, your media URL points to an audio or video file on your computer.",
             "In that case, these media will only be playable for you in the web page we create here.",
             "Alternatively, you can host your media file on the internet.",
             "todo: explain more..."]
    for item in items:
       el.children.append(html.Li(item))
    return True, "Media URLs", el
#--------------------------------------------------------------------------------
# explain how morpheme gloss capitaliation & fonts can be handled
@callback(
    Output('slexilModal', 'is_open', allow_duplicate=True),
    Output('modalTitle', 'children', allow_duplicate=True),
    Output('modalContents', 'children', allow_duplicate=True),
    Input('explainGlossingAbbreviationsButton', 'n_clicks'),
    State('globals', 'data'),
    prevent_initial_call=True
    )
def displayStateAsList(n_clicks, data):
    el = html.Div(children=["Nothing yet ready on this topic."])
    return True, "Glossing Abbreviations", el
#--------------------------------------------------------------------------------
#m4_include(20.setTitle.py)
#--------------------------------------------------------------------------------
def createProjectDirectory(projectName):

   path = os.path.join(PROJECTS_DIRECTORY, projectName)
   if not os.path.exists(path):
      os.mkdir(path)
   return path
      
#--------------------------------------------------------------------------------
setTitleDiv = html.Div(id="setTitleDiv",
          children=[
              html.H2('Enter Project Title: ',
                      style={'display':'inline-block', 'marginRight': "20px",
                             "fontSize": "24px"}),
              dcc.Input(id='projectNameInput',
                        type='text',
                        value='',
                        placeholder='',
                        debounce=True,
                        style={'display':'inline-block', 'fontSize': "24px",
                               'width': '400px'}),
              html.Button("Submit", id="setProjectNameButton", n_clicks=0,
                          style={'margin-left': '10px', 'margin-right': '10px'}),
              html.Div(id="projectTitleHelp", children=[
                  DashIconify(icon="feather:info", color="blue",width=30),
              ], style={"display": "inline-block"})
          ],className="bodyStyle")
#----------------------------------------------------------------------
dashApp.layout.children.append(setTitleDiv)
#----------------------------------------------------------------------
# @dashApp.callback(Output('globals', 'data', allow_duplicate=True),
#                   Output('fileTypeRadioButtons', 'options', allow_duplicate=True),
#                   Output('fileTypeRadioButtons', 'style', allow_duplicate=True),
#                   Output('inputFileTypePrompt', 'style', allow_duplicate=True),
#                   Input('projectNameInput', 'value'),
#                   State('globals', 'data'),
#                   prevent_initial_call=True)
# def saveProjectName_byCarriageReturn(projectTitle, globals):
#     characterCount = len(projectTitle)
#     if characterCount == 0:
#         projectTitle = "sp99"
#     projectName = projectTitle.replace(" ", "")
#     print("--- projectName: %s" % projectName)
#     globals['projectTitle'] = projectTitle
#     globals['projectName'] = projectName
#     enabledRadioButtonOptions=[
#         {'label': 'EAF', 'value': 'EAF', 'disabled': False},
#         {'label': 'YAML', 'value': 'YAML', 'disabled': False}
#         ]
#     radioButtonStyle = {'color': 'black', 'display': 'inline-block'}
#     inputFileTypePromptStyle = {'color': 'black'}
#     
#     return globals, enabledRadioButtonOptions, radioButtonStyle, inputFileTypePromptStyle
# 

@dashApp.callback(Output('globals', 'data', allow_duplicate=True),
                  Output('fileTypeChooserDiv', 'style'),
                  Input('setProjectNameButton', 'n_clicks'),
                  State('projectNameInput', 'value'),
                  State('globals', 'data'),
                  State('fileTypeChooserDiv', 'style'),
                  prevent_initial_call=True)
def saveProjectName_byButton(nClicks, projectTitle, globals, chooserStyle):
    characterCount = len(projectTitle)
    if characterCount == 0:
        projectTitle = "sp99"
    projectName = projectTitle.replace(" ", "")
    print("--- projectName: %s" % projectName)
    globals['projectTitle'] = projectTitle
    globals['projectName'] = projectName
    globals['projectPath'] = os.path.join(PROJECTS_DIR, projectName)
    chooserStyle['display'] = 'inline-block'
    #enabledRadioButtonOptions=[
    #    {'label': 'EAF', 'value': 'EAF', 'disabled': False},
    #    {'label': 'YAML', 'value': 'YAML', 'disabled': False}
    #    ]
    #radioButtonStyle = {'color': 'black', 'display': 'inline-block'}
    #inputFileTypePromptStyle = {'color': 'black'}
    #fileTypeChooserDivDisplay = "inline-block"
    
    return globals, chooserStyle

@callback(
    Output('slexilModal', 'is_open', allow_duplicate=True),
    Output('modalTitle', 'children', allow_duplicate=True),
    Output('modalContents', 'children', allow_duplicate=True),
    Input('projectTitleHelp', 'n_clicks'),
    prevent_initial_call=True
    )
def displayProjectTitleHelp(n_clicks):
    contents = html.Ul(id="list",
       children=[html.Li("Your title will be displayed prominently at the top of the web page we create from your text."),
                 html.Li("We recommend a concise and descriptive name, 3-40 characters long."),
                 html.Li("It can include spaces and upper and lower case characters."),
                 html.Li("For instance: How Daylight Was Stolen - Harry Moses.")
                 ])
    
    return True, "Help for Project Title Input", contents

# #----------------------------------------------------------------------
# @callback(
#     Output('globals', 'data'),
#     Output('fileTypeRadioButtons', 'options'),
#     Output('fileTypeRadioButtons', 'style'),
#     Output('inputFileTypePrompt', 'style'),
#     Input('setProjectNameButton', 'n_clicks'),
#     State('projectNameInput', 'value'),
#     State('globals', 'data'),
#     prevent_initial_call=True)
# def handleSetProjectNameButton(n_clicks, userEnteredString, data):
#     title = userEnteredString.strip()
#     newProjectName = title.replace(" ", "_")
#     projectPath = createProjectDirectory(newProjectName)
#     if data is None:
#        print("initializing None data")
#        data = {}
#     data['title'] = title
#     data['projectName'] = newProjectName
#     data['projectPath'] = projectPath
#     return(data, False)
#--------------------------------------------------------------------------------

#--------------------------------------------------------------------------------
fileTypeChooserDiv = html.Div(id="fileTypeChooserDiv",
             style={'margin': '5px', 'marginLeft': '10px', 'fontSize': '24px',
                    'display': 'none', 'marginRight': '10px'},
             children=[html.Span("Input File Type? ",
                                 id="inputFileTypePrompt",
                                 style={'fontFamily': 'New York Times-Roman',
                                        'fontSize': '24px'}
                                 ),
                       dcc.RadioItems(id="fileTypeRadioButtons",
                                      options=[
                                          {'label': '   EAF  ', 'value': 'EAF', 'disabled': False},
                                          {'label': '   YAML  ', 'value': 'YAML', 'disabled': False}
                                         ],
                                      labelStyle={'display': 'inline-block', 'margin': '20px', 'margin-top': '0px'},
                                      inline=True,
                                      style={'display': 'inline-block',
                                             'fontFamily': 'New York Times-Roman',
                                             'font-size': '24px'})
                       ])
#----------------------------------------------------------------------
dashApp.layout.children.append(fileTypeChooserDiv)
#----------------------------------------------------------------------
@dashApp.callback(Output('globals', 'data', allow_duplicate=True),
                  Output('mainTextUploader', 'style'),
                  Input('fileTypeRadioButtons', 'value'),
                  State('globals', 'data'),
                  State('mainTextUploader', 'style'),
                  prevent_initial_call=True)
def handleFileTypeSelection(fileType,  globals, uploaderStyle):
    print("handleFileTypeSelection: %s" % fileType)
    newText = dcc.Markdown("- input file type: %s" % fileType)
    globals['fileType'] = fileType
    uploaderStyle['display'] =  'inline-block'
    return globals, uploaderStyle


#m4_include(22.loadEAF.py)
uploaderStyle = {'width': '30%',
                 'height': '60px',
                 'lineHeight': '60px',
                 'borderWidth': '1px',
                 'borderStyle': 'solid',
                 'borderRadius': '5px',
                 'textAlign': 'center',
                 'fontSize': '24px',
                 'margin': '10px',
                 'marginLeft': '50px',
                 'display': 'none'
                 }

simpleTextDisplayStyle = {'fontSize': '32px',
                          'marginLeft': '200px'
                          }

mainTextLoaderDiv = html.Div(id="mainTextLoaderDiv",
                        children = [
                           dcc.Upload(
                              id='mainTextUploader',
                              children=html.Div([
                                 'Drag and Drop or ',
                                 html.A('Select File')
                                 ]), #className="mainTextUploader"),
                              style=uploaderStyle,
                              multiple=False
                              )])

dashApp.layout.children.append(mainTextLoaderDiv)
#--------------------------------------------------------------------------------
@dashApp.callback(Output('createHtmlButtonDiv', 'style'),
                  Output('createHtmlButton', 'children'),
                  Output('globals', 'data', allow_duplicate=True),

                  Output('slexilModal',   'is_open',  allow_duplicate=True),
                  Output('modalTitle',    'children', allow_duplicate=True),
                  Output('modalContents', 'children', allow_duplicate=True),

                  Input('mainTextUploader', 'contents'),
                  State('mainTextUploader', 'filename'),
                  State('mainTextUploader', 'last_modified'),
                  State('createHtmlButtonDiv', 'style'),
                  State('globals', 'data'),
                  prevent_initial_call=True)

def handleMainTextUploadAndEafParse(contents, filename, date, buttonDivStyle, globals):

    globals['mainTextFilename'] = filename
    projectName = globals['projectName']
    projectTitle = globals['projectTitle']
    projectDirectory = os.path.join(PROJECTS_DIRECTORY, projectName)
    mainTextFilePath = os.path.join(projectDirectory, filename)
    buttonDivStyle['display'] = 'inline-block'
    globals['mainTextFilePath'] = mainTextFilePath

      # expected return values
    errorBoxOpen = False
    errorBoxChildren = None
    buttonDivStyle['display'] = 'inline-block' # assume success
    buttonLabel = "Create %s.html" % globals['projectTitle']

    try: 
        saveUploadedFile(contents, projectName, filename)
        fileType = globals['fileType']
        print("%s has format %s" % (filename, fileType))
        if fileType == "EAF":
            p = EafParser(mainTextFilePath, verbose=True,
                          fixOverlappingTimeSegments=False)

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
       errorBoxTitle = "parse error"
       errorBoxChildren = dbc.ModalBody(e.__str__())
       buttonDivStyle['display'] = 'none'
       buttonLabel = "bug!"
       return (buttonDivStyle, buttonLabel, globals, errorBoxOpen,
               errorBoxTitle, errorBoxChildren)
       
    #pdb.set_trace()
    return buttonDivStyle, buttonLabel, globals, errorBoxOpen, errorBoxChildren
    #return globals, errorBoxOpen, errorBoxChildren
   
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

from slexil.yamlToText import YamlToText


buttonDiv = html.Div(id="buttonDiv",
             style={"margin": "20px"},
             children=[
                 html.Div(id="createHtmlButtonDiv",
                          style={'display': 'none'},
                          children=[html.Button('Create HTML',
                                                id='createHtmlButton',
                                                style=buttonStyle)]
                          ),
                 html.Div(id="downloadHtmlButtonDiv",
                          style={'display': 'none'},
                          children=[html.Button("Download HTML",
                                                id="downloadHtmlButton",
                                                style=buttonStyle),
                                    dcc.Download(id="download-html")]),
                 html.Div(id="downloadYamlButtonDiv",
                          style={'display': 'none'},
                          children=[html.Button("Download YAML",
                                                id="btn-download-txt",
                                                className="button"),
                                    dcc.Download(id="download-yaml")],
                          )
                 ])

#--------------------------------------------------------------------------------
dashApp.layout.children.append(buttonDiv)
#--------------------------------------------------------------------------------
@dashApp.callback(Output('downloadHtmlButtonDiv', 'style'),
                  Output('downloadHtmlButton', 'children'),
                  Output('globals', 'data', allow_duplicate=True),
                  [Input('createHtmlButton', 'n_clicks')],
                  State('downloadHtmlButtonDiv', 'style'),
                  State('globals', 'data'),
                  prevent_initial_call=True)
def createHtml(n_clicks, buttonDivStyle, globals):

   print("--- runSlexil, n_clicks: %d" % n_clicks)
   title = globals['projectTitle']

   buttonDivStyle['display'] = 'inline-block'
   buttonLabel = "Download %s.html" % globals['projectTitle']

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
   return buttonDivStyle, buttonLabel, globals
        
def createHtmlFromEAF(eafFile, title, projectName, projectDirectory):

   yamlFileName = globals['yamlFileName']
   htmlFileName = createHtmlFromYaml(yamlFileName, title, projectName, projectDirectory)
   return htmlFilename

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


@dashApp.callback(
    Output("download-html", "data"),
    Input("downloadHtmlButton", "n_clicks"),
    State("globals", "data"),
    prevent_initial_call=True,
    )
def downloadHtml(n_clicks, globals):
    print("--- 23a downloadHtml")
    
    filename = os.path.join(PROJECTS_DIRECTORY,
                            globals['projectName'],
                            "%s.html" % globals['projectName'])
    return dcc.send_file(filename)


#m4_include(28.loadAbbreviations.py)
#m4_include(26.loadAudio.py)
#m4_include(createWebPage.py)
#m4_include(23.makeHtml.py)
#m4_include(24.displayAndDownload.py)
#----------------------------------------------------------------------
if __name__ == '__main__':
    port = 9002
    dashApp.run(host='0.0.0.0', debug=True, port=port)
