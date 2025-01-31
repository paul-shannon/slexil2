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
appVersion = "3.0.7"
versionString = "slexil %s, app %s" % (slexil.__version__, appVersion)
dbcStyle = dbc.themes.BOOTSTRAP
styleSheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', dbcStyle]

app = flask.Flask(__name__)
dashApp = Dash(__name__, server=app, url_base_pathname='/',
               external_stylesheets=styleSheets)
dashApp.config.suppress_callback_exceptions=True
dashApp.title = "Slexil 3"

PROJECTS_DIR = "PROJECTS"
#--------------------------------------------------------------------------------
def runBigDemo():

  projectPath = os.path.join(PROJECT_DIR, "timingTest")
  fullPath = os.path.join(projectPath, "4EthelAnita230503Slexil.eaf")
  htmlFile = createWebPage(fullPath, projectPath, "timingTest")
  
#--------------------------------------------------------------------------------
def getStateAsArray():

   print('--- entering getStateAsArray')
   keys = globals.keys()
   print(keys)
   print('--- leaving getStateAsArray')
   
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
buttonDivStyle = {#"height": "100px",
                  "width": "300px",
                  #"background-color": "lightblue",
                  #"display": "inline-block",
                  "float": "right"}
headerButtonStyle = {"display": "inline-block",
                     "marginLeft": "200px",
                     #"width": "200px",
                     'font-size': '24px',
                     'fontFamily': 'New York Times-Roman',
                     'border': '1px solid black',
                     'border-radius': '10px',
                      }


proceedButton = html.Button("Proceed", id="proceedButton",
                            style=headerButtonStyle)

continueButtonStyle = {"margin": "15px",
                        "fontSize": "20px",
                        "border": "1px solid gray",
                        "borderRadius": "10px",
                        "float": "right"}
                        
continueButton = html.Button("Continue...",
                             id="modalDialogContinueButton",
                             style=continueButtonStyle)

modalTitle = dbc.ModalTitle("Slexil Notification", id="modalTitle")
modalHeader = dbc.ModalHeader(children=[modalTitle,
                                        html.Div(continueButton)],
                              close_button=False
                              )
modalFooter = dbc.ModalFooter()
modalBody = dbc.ModalBody(id='modalBody',
                          children=html.Div("fubar"),
                          style={"fontSize": "20px"})

modal = dbc.Modal([modalHeader, modalBody, modalFooter],
                   id="slexilModal",
                   centered=True,
                   is_open=False,
                   keyboard=True,
                   size="xl",
                   scrollable=True)

modalDiv = html.Div([modal])
#    dbc.Modal([
#         dbc.ModalHeader(
#            children=[dbc.ModalTitle("SLEXIL Notification", id="modalTitle"),
#                      html.Div([proceedButton], style=buttonDivStyle)],
#            close_button=True,
#            className="modal-title-custom"),
#         dbc.ModalBody("", id='modalBody', style={"fontSize": "24px"}),
#         #dbc.ModalFooter(
#         #   dbc.Button("Close", id="modalCloseButton", className="ms-auto", n_clicks=0))
#         ],
#         id="slexilModal",
#         centered=True,
#         is_open=False,
#         style={'font-size': '30px'},
#         size="xl",    # sm, lg, xl
#         fullscreen=False,
#         scrollable=True,
#         )])
#-------------------------------------------------------
loadTrackerDiv = html.Div(id="loadTrackerDiv")
modalLoadSpinnerWatcher = dcc.Loading(id="modalLoadWatcher",
                                      type="default",
                                      children=[modalDiv])
#-------------------------------------------------------
def createAboutDropdownMenu():

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

#--------------------------------------------------------------------------------
def createFaqDropdownMenu():

   dropdown = dbc.DropdownMenu(
      label="FAQ",
      id="faqDropdownMenu",
      align_end=True,
      size="sm",
      children=[
         dbc.DropdownMenuItem("YAML Format",
                              id="yamlFormatExplainedButton",
                              class_name="menuItemClass"),
         dbc.DropdownMenuItem("EAF Format",
                              id="eafFormatExplainedButton",
                              class_name="menuItemClass"),
         dbc.DropdownMenuItem("Video & Audio Playback Problems",
                              id="videoAndAudioProblemsExplainedButton",
                              class_name="menuItemClass")
         ])

   return dropdown

#--------------------------------------------------------------------------------
def getExceptionTracebackString(exc: Exception) -> str:

    # Ref: https://stackoverflow.com/a/76584117/
   file = io.StringIO()
   exceptionString = traceback.format_exception_only(None, exc)
   tracebackString = traceback.print_exception(exc, file=file)
   return (file.getvalue().rstrip(), exceptionString)

#--------------------------------------------------------------------------------
def createHtmlErrorReportWithEmailLink(globals, errorString,
                                       errorStringHtml, traceBackString):

   sendTo = 'mailto:paul.thurmond.shannon@gmail.com'
   subject = '?subject=slexil bug report'
   bodyLeadIn = '&body='

   bodyText = ""
   bodyText += "%s\n\n" % errorString
   for key in globals.keys():
       bodyText += "%s: %s\n" % (key, globals[key])

   bodyText += "\n\n"
   bodyText += traceBackString
   
   bodyTextCRLF = bodyText.replace("\n", "%0D%0A")
   body = "%s%s" % (bodyLeadIn, bodyTextCRLF)
   emailHref = '%s%s%s' % (sendTo, subject, body)

   #elDiv = html.Div(children=[errorStringHtml])
   elDiv = html.Div(children=[])

     # put the succinct error message first
   elDiv.children.append(html.H2(errorString))
     # then the email link
   elDiv.children.append(html.A(
      [html.H2('Please Click Here to Email Bug Report to Paul Shannon')],
       title ='email_me',
       href=emailHref,
       target='_blank'))

   elDiv.children.append(html.P(" "))
   elDiv.children.append(html.H2("Context: "))
   #elDiv.children.append(errorStringHtml)
   el = html.Ul(id="list", children=[])
   
   for key in globals.keys():
       el.children.append(html.Li("%s: %s" % (key, globals[key])))

   elDiv.children.append(el)

   return elDiv

#--------------------------------------------------------------------------------
globals = dcc.Store(id="globals",
              data={'release ': versionString})
dashApp.layout = html.Div(id="mainDiv",
                          children=[globals,
                                    html.Div(id="bannerDiv", 
                                             children=[
                                               createAboutDropdownMenu(),
                                               createFaqDropdownMenu()]),
                                    loadTrackerDiv],
                            style={"margin": "5px"})
#----------------------------------------------------------------------
# About->State dropdown menu button displays state in a modal dialog
@callback(
    Output('slexilModal', 'is_open', allow_duplicate=True),
    Output('modalTitle', 'children', allow_duplicate=True),
    Output('modalBody', 'children', allow_duplicate=True),
    Input('examineStateButton', 'n_clicks'),
    State('globals', 'data'),
    prevent_initial_call=True
    )
def displayStateAsList(n_clicks, globals):

    dialogBoxOpen = True
    dialogBoxTitle = "State Variables"
    dialogBoxChildren = html.P("state is empty, no variables yet assigned")
    if globals is None:
       return(dialogBoxOpen, dialogBoxTitle, dialogBoxChildren)

    el = html.Ul(id="list", children=[])
    for key in globals.keys():
       el.children.append(html.Li("%s: %s" % (key, globals[key])))
    dialogBoxChildren = el
    return (dialogBoxOpen, dialogBoxTitle, dialogBoxChildren)
    
#--------------------------------------------------------------------------------
# explain how media URLs work, how and why you might change them
@callback(
    Output('slexilModal', 'is_open', allow_duplicate=True),
    Output('modalTitle',  'children', allow_duplicate=True),
    Output('modalBody',   'children', allow_duplicate=True),
    Input('explainMediaURLsButton', 'n_clicks'),
    State('globals', 'data'),
    prevent_initial_call=True
    )
def explainMediaURLs(n_clicks, data):
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
    Output('modalBody', 'children', allow_duplicate=True),
    Input('explainGlossingAbbreviationsButton', 'n_clicks'),
    State('globals', 'data'),
    prevent_initial_call=True
    )
def explainMorphemeGlossFormat(n_clicks, data):
    el = html.Div(children=["Nothing yet ready on this topic."])
    return True, "Glossing Abbreviations", el
#--------------------------------------------------------------------------------
# FAQ-YAML dropdown menu button explains the basics
@callback(
    Output('slexilModal', 'is_open', allow_duplicate=True),
    Output('modalTitle', 'children', allow_duplicate=True),
    Output('modalBody', 'children', allow_duplicate=True),
    Input('yamlFormatExplainedButton', 'n_clicks'),
    State('globals', 'data'),
    prevent_initial_call=True
    )
def explainYAML(n_clicks, globals):

    dialogBoxOpen = True
    dialogBoxTitle = "YAML: 'Yet Another Markup Language'"
    intro0 = "YAML is a human-readable, easily typed format for interlinear text transcription and annotation."
    intro1 = "The small example shown below, taken from a public domain recitation of Dante's Inferno, is a useful introduction."
    intro2 = "Copy and paste this into your favorite text editor, save as 'inferno.yaml' as plain text - not as a Word doc - and feed it into slexil."    

    dialogBoxChildren = html.Div(id="yamlExplainedDialogBoxDiv",
                                 children=[
                                   html.P(intro0),
                                   html.P(intro1),
                                   html.P(intro2),
                                 html.Pre("""
title: Dante's Inferno
narrator: Roberto Benigni
textEntry: Paul Shannon
mediaFile: https://slexildata.artsrn.ualberta.ca/misc/inferno-threeLines.wav
mimeType: audio/x-wav

lines:

  - html: "<div style='margin:20px; color:red;'><h6>Roberto Benigni recites Dante's Inferno:</h6></div>"

  - startTime: 0
    endTime: 2828
    italianSpeech: Nel mezzo del cammin di nostra vita
    morphemes: [en=il,mezz–o,de=il,cammin–Ø,di,nostr–a,vit–a]
    morpheme-gloss: [in=DEF:MASC:SG,middle-MASC:SG,of=DEF:MASC:SG,journey–MASC:SG,of,our-FEM:SG,life-FEM]
    english: Midway upon the journey of our life

  
  - startTime: 3095
    endTime: 5500
    italianSpeech: mi ritrovai per una selva oscura
    morphemes: [mi,ritrov–ai,per,una,selv–a,oscur–a]
    morpheme-gloss: [I:DAT,found–1SG:INDEF:REM:PAST,for,INDEF:FEM:SG,forest-FEM,dark–FEM:SG]
    english: I found myself within a forest dark

  - startTime: 5624
    endTime: 8033
    italianSpeech: ché la diritta via era smarrita.
    morphemes: [ché,la,diritt–a,vi–a,era,smarr–it–a]
    morpheme-gloss: [that,def:FEM:SG,straight-FEM:SG,path-FEM,be:3SG:IMPF,lose–PARTIC–FEM:SG]
    english: For the straightforward pathway had been lost.
""")])

    return(dialogBoxOpen, dialogBoxTitle, dialogBoxChildren)
    
#--------------------------------------------------------------------------------
# FAQ->EAF dropdown menu button explains the basics
@callback(
    Output('slexilModal', 'is_open', allow_duplicate=True),
    Output('modalTitle', 'children', allow_duplicate=True),
    Output('modalBody', 'children', allow_duplicate=True),
    Input('eafFormatExplainedButton', 'n_clicks'),
    State('globals', 'data'),
    prevent_initial_call=True
    )

def explainEAF(n_clicks, globals):
    dialogBoxOpen = True
    dialogBoxTitle = "EAF: 'The ELAN Annotation Format'"
    intro0 = " is the standard linguistics software tool for transcribing and annotating audio and video speech recordings."
    intro1 = "It is provided for free download: "

    dialogBoxChildren = html.Div(id="yamlExplainedDialogBoxDiv",
                                 children=[
                                   html.A("ELAN", href='https://en.wikipedia.org/wiki/ELAN_software', target="_blank"),
                                   html.Span(intro0),
                                   html.P(),
                                   html.Span(intro1),
                                   html.A("here", href="https://archive.mpi.nl/tla/elan/download", target="_blank"),
                                   html.P(),
                                   html.Button("Download small example EAF file", id="downloadSmallEafButton",
                                               style=buttonStyle),
                                   dcc.Download(id="download-sample-eaf")
                                   ])
    return(dialogBoxOpen, dialogBoxTitle, dialogBoxChildren)
    
#--------------------------------------------------------------------------------
# FAQ->Audio/Video Problemes
@callback(
    Output('slexilModal', 'is_open', allow_duplicate=True),
    Output('modalTitle', 'children', allow_duplicate=True),
    Output('modalBody', 'children', allow_duplicate=True),
    Input('videoAndAudioProblemsExplainedButton', 'n_clicks'),
    prevent_initial_call=True
    )

def explainEAF(n_clicks):
    dialogBoxOpen = True
    dialogBoxTitle = "Some Video/Audio Playback Problems"
    intro0 = "We regularly see that in the Firefox browser, .MOV video files play without audio."
    intro1 = "Some remedies we find useful:"
    remedy1 = "Use another browser, perhaps Chrome or Safari."
    remedy2 = "Or write your video into another format, like .mp4."

    dialogBoxChildren = html.Div(id="videoProblemsDiv",
                                 children=[
                                   html.P(intro0),
                                   html.P(),
                                   html.Ul(children=[html.Li(remedy1),
                                                     html.Li(remedy2)])
                                   ])
    return(dialogBoxOpen, dialogBoxTitle, dialogBoxChildren)
    
#--------------------------------------------------------------------------------

@dashApp.callback(
    Output("download-sample-eaf", "data"),
    Input("downloadSmallEafButton", "n_clicks"),
    prevent_initial_call=True,
    )
def downloadHtml(n_clicks):
    print("--- 23a downloadHtml")
    
    filename = os.path.join(PROJECTS_DIRECTORY,
                            "SLEXIL_DEMO_FILES",
                            "inferno.eaf")
    return dcc.send_file(filename)



# dialog header "Continue..." button closes the dialog
@callback(
    Output('slexilModal', 'is_open', allow_duplicate=True),
    Input('modalDialogContinueButton', 'n_clicks'),
    prevent_initial_call=True
    )
def closeModalDialog(n_clicks):
    return False
#--------------------------------------------------------------------------------

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
    Output('modalBody', 'children', allow_duplicate=True),
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
                  Output('mainTextUploader', 'accept'),
                  Input('fileTypeRadioButtons', 'value'),
                  State('globals', 'data'),
                  State('mainTextUploader', 'style'),
                  prevent_initial_call=True)
def handleFileTypeSelection(fileType,  globals, uploaderStyle):
    print("handleFileTypeSelection: %s" % fileType)
    print("--- globals:")
    if not globals:
        globals = {}
    print(globals)
    #pdb.set_trace()
    globals['fileType'] = fileType
    uploaderStyle['display'] =  'inline-block'
    uploadFileType = ".%s" % fileType
    return globals, uploaderStyle, uploadFileType


uploaderStyle = {'width': '400px',
                 'height': '70px',
                 'lineHeight': '60px',
                 'borderWidth': '1px',
                 'borderStyle': 'solid',
                 'borderRadius': '5px',
                 'textAlign': 'center',
                 'fontSize': '24px',
                 'margin': '10px',
                 'marginLeft': '30px',
                 'display': 'none',
                 'background-color': '#F5FAF3',
                 ':hover': {
                    'background-color': 'lightblue'
                     }
                 }

simpleTextDisplayStyle = {'fontSize': '32px',
                          'marginLeft': '200px'
                          }

  # accept string (.eaf or .yaml) set in callback
  # function handleFileTypeSelection

mainTextLoaderDiv = html.Div(id="mainTextLoaderDiv",
                        children = [
                           dcc.Upload(
                              id='mainTextUploader',
                              children=html.Div(
                                  id='fileSelectorDiv',
                                  children = ['Drag and Drop or ',
                                              html.A('Select File')
                                              ]),
                              style=uploaderStyle,
                              multiple=False
                              )])

dashApp.layout.children.append(mainTextLoaderDiv)
#--------------------------------------------------------------------------------
@dashApp.callback(Output('createHtmlButtonDiv', 'style', allow_duplicate=True),
                  Output('downloadHtmlButtonDiv', 'style', allow_duplicate=True),
                  Output('analyzeButtonDiv', 'style'),
                  Output('analyzeButton', 'children'),    
                  Output('globals', 'data', allow_duplicate=True),

                  Output('slexilModal',   'is_open',  allow_duplicate=True),
                  Output('modalTitle',    'children', allow_duplicate=True),
                  Output('modalBody', 'children', allow_duplicate=True),

                  Input('mainTextUploader', 'contents'),
                  State('mainTextUploader', 'filename'),
                  State('mainTextUploader', 'last_modified'),
                  State('analyzeButtonDiv', 'style'),
                  State('createHtmlButtonDiv', 'style'),
                  State('downloadHtmlButtonDiv', 'style'),
                  State('globals', 'data'),
                  prevent_initial_call=True)

def handleMainTextUpload(contents, filename, date, analyzeButtonDivStyle,
                         createHtmlButtonDivStyle,
                         downloadHtmlButtonDivStyle,
                         globals):

    globals['mainTextFilename'] = filename
    projectName = globals['projectName']
    projectTitle = globals['projectTitle']
    projectDirectory = os.path.join(PROJECTS_DIRECTORY, projectName)
    mainTextFilePath = os.path.join(projectDirectory, filename)
    analyzeButtonDivStyle['display'] = 'inline-block'
    globals['mainTextFilePath'] = mainTextFilePath

      # expected return values
    errorBoxOpen = False
    errorBoxChildren = None
    errorBoxTitle = None
    createHtmlButtonDivStyle['display'] = 'none'      # always hide this
    downloadHtmlButtonDivStyle['display'] = 'none'    # always hide this
    analyzeButtonDivStyle['display'] = 'inline-block' # assume success
    buttonLabel = "Assess %s file" % globals['fileType']

    try: 
        saveUploadedFile(contents, projectName, filename)
    except Exception as e:
       errorBoxOpen = True
       errorBoxTitle = "parse error"
       errorString = getExceptionTracebackString(e)
       errorBoxChildren = errorString
       analyzeButtonDivStyle['display'] = 'none'
       buttonLabel = "bug!"
       return (createHtmlButtonDivStyle,
               downloadHtmlButtonDivStyle,
               analyzeButtonDivStyle,
               buttonLabel,
               globals,
               errorBoxOpen,
               errorBoxTitle,
               errorBoxChildren)
       
    return (createHtmlButtonDivStyle,
            downloadHtmlButtonDivStyle,
            analyzeButtonDivStyle,
            buttonLabel,
            globals,
            errorBoxOpen,
            errorBoxTitle,
            errorBoxChildren)
   
#--------------------------------------------------------------------------------
def saveUploadedFile(contents, projectName, filename):

   print("saveUploadedFile: %s, %s" % (projectName, filename))
   print("content length: %d" % len(contents))
   
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

from slexil.newYamlParser import NewYamlParser
from slexil.eafParser import extractAllTimeAlignedTierIDs
#--------------------------------------------------------------------------------
analyzeButtonStyle = {"margin": "15px",
                      "margin-left": "30px",
                      "fontSize": "20px",
                      "border": "1px solid gray",
                      "borderRadius": "10px"
                      }


#--------------------------------------------------------------------------------
analyzeButtonDiv = html.Div(id="analyzeButtonDiv",
                            style={'display': 'none'},
                            children=[html.Button('Assess',
                                                  id='analyzeButton',
                                                  style=analyzeButtonStyle)]
                            )
dashApp.layout.children.append(analyzeButtonDiv)
#--------------------------------------------------------------------------------
@dashApp.callback(Output('globals',       'data',     allow_duplicate=True),
                  Output('slexilModal',   'is_open',  allow_duplicate=True),
                  Output('modalTitle',    'children', allow_duplicate=True),
                  Output('modalBody',     'children', allow_duplicate=True),
                  Output('createHtmlButtonDiv', 'style', allow_duplicate=True),
                  Output('analyzeButtonDiv', 'style', allow_duplicate=True),

                  [Input('analyzeButton', 'n_clicks')],
                  State('globals', 'data'),
                  State('createHtmlButtonDiv', 'style'),
                  State('analyzeButtonDiv', 'style'),
                  prevent_initial_call=True)
def analyze(n_clicks,  globals, createHtmlDivStyle, analyzeButtonDivStyle):

   #print("--- analyze %s" % globals['mainTextFilename'])

   errorBoxOpen = False
   errorBoxChildren = None
   errorBoxTitle = None
   createHtmlDivStyle['display'] = 'none' # pessimistic: assume failure here

   fileType = globals['fileType']
   mainTextFilePath = globals['mainTextFilePath']
   #print("%s has format %s" % (mainTextFilePath, fileType))
   mediaURL = "unknown"
   timeAlignedTierCount = 1 # only possibility with current YAML format
   try:
      if fileType == "EAF":
         p = EafParser(mainTextFilePath, verbose=False,
                       fixOverlappingTimeSegments=False)
         p.run()
         tbl = p.getTierTable()
         mediaURL = p.getMediaURL()
         timeAlignedTiers = extractAllTimeAlignedTierIDs(mainTextFilePath)
         if len(timeAlignedTiers) > 1:
            tierNamesString = " ".join(timeAlignedTiers)
            #errorMessage = html.Div(children=[
            #   html.P("%d time-aligned tiers found: %s" % (len(timeAlignedTiers), tierNamesString)),
            #   html.P("""Slexil currently supports only one time-aligned tier. 
            #             Email a bug report (see below) if you wish to request 
            #             such support in a future release.""")])
            msg = "%d time-aligned tiers found: %s,  " %\
                    (len(timeAlignedTiers), tierNamesString)
            msg += " but Slexil currently supports only one time-aligned tier.  "
            msg += "Email a bug report (see below) if you wish to request "
            msg += "such support in a future release."
            raise Exception(msg)
         yaml = p.toYAML("a", "b", "c")
         yamlFile = os.path.join(globals['projectPath'],
                                 "%s.yaml" % globals['projectName'])
         p.writeYAML(yaml, yamlFile)
         globals['yamlFileName'] = yamlFile
      elif fileType == "YAML":
         p = NewYamlParser(mainTextFilePath)
         tbl = p.getTierTable()
         mediaURL = p.getMediaURL()
         p.checkLines()
      formattedTable = dbc.Table.from_dataframe(tbl)
      errorBoxOpen = True
      errorBoxChildren = html.Div(children=[html.P("media url: %s" % mediaURL),
                                            html.P("time-aligned tier count: %d" %
                                                   timeAlignedTierCount),
                                            html.P(formattedTable)])
      errorBoxTitle = "Valid Structure"
      createHtmlDivStyle['display'] = 'inline-block'
      analyzeButtonDivStyle['display'] = 'inline-block'
      return (globals, errorBoxOpen, errorBoxTitle, errorBoxChildren,
              createHtmlDivStyle, analyzeButtonDivStyle)

   except Exception as e:
      errorBoxOpen = True
      errorBoxTitle = "%s PARSING ERROR" % globals['fileType']
      (traceBackString, errorString) = getExceptionTracebackString(e)
      if type(errorString) is list:
         errorString = errorString[0]
      if "reason" in dir(e):  # perhaps only in XMLSchemaValidationError
         errorString = e.reason
      errorStringHtml = html.P(errorString)
      #pdb.set_trace()
      htmlErrorMessage = createHtmlErrorReportWithEmailLink(globals,
                                                            errorString,
                                                            errorStringHtml,
                                                            traceBackString)
      errorBoxChildren = dbc.ModalBody(htmlErrorMessage)
      analyzeButtonDivStyle['display'] = 'none'
      return (globals, errorBoxOpen, errorBoxTitle, errorBoxChildren,
              createHtmlDivStyle, analyzeButtonDivStyle)

#--------------------------------------------------------------------------------

from slexil.yamlToText import YamlToText
from slexil.morphemeGlossAbbreviations import MorphemeGlossAbbreviations


createHtmlButtonDiv = html.Div(id="createHtmlButtonDiv",
                               style={'display': 'none'},
                               children=[html.Button('Create HTML',
                                                     id='createHtmlButton',
                                                     style=buttonStyle)]
                               )

#--------------------------------------------------------------------------------
dashApp.layout.children.append(createHtmlButtonDiv)
#--------------------------------------------------------------------------------
@dashApp.callback(Output('downloadHtmlButtonDiv', 'style'),
                  Output('downloadHtmlButton', 'children'),
                  Output('globals', 'data', allow_duplicate=True),

                  Output('slexilModal',   'is_open',  allow_duplicate=True),
                  Output('modalTitle',    'children', allow_duplicate=True),
                  Output('modalBody', 'children', allow_duplicate=True),

                  [Input('createHtmlButton', 'n_clicks')],
                  State('downloadHtmlButtonDiv', 'style'),
                  State('globals', 'data'),
                  prevent_initial_call=True)
def createHtml(n_clicks, downloadHtmlButtonDivStyle, globals):

   print("--- runSlexil, n_clicks: %d" % n_clicks)
   title = globals['projectTitle']

      # expected return values
   errorBoxOpen = False
   errorBoxChildren = None
   errorBoxTitle = None

   downloadHtmlButtonDivStyle['display'] = 'inline-block'
   downloadHtmlButtonLabel = "Download %s.html" % globals['projectTitle']

   projectName = globals['projectName']
   projectDirectory = os.path.join(PROJECTS_DIRECTORY, globals['projectName'])
   fileType = globals['fileType']
   if fileType == "YAML":
      yamlFileName = globals['mainTextFilePath']
   elif fileType == "EAF":
      yamlFileName = globals['yamlFileName']

   try:
      htmlFileName = createHtmlFromYaml(yamlFileName, title,
                                        projectName, projectDirectory)
   except Exception as e:
      errorBoxOpen = True
      errorBoxTitle = "Slexil ERROR! in createHtml function"
      (traceBackString, errorString) = getExceptionTracebackString(e)
      errorStringHtml = html.P(errorString)
      htmlErrorMessage = createHtmlErrorReportWithEmailLink(globals,
                                                            errorString,
                                                            errorStringHtml,
                                                            traceBackString)
      errorBoxChildren = dbc.ModalBody(htmlErrorMessage)
      downloadHtmlButtonDivStyle['display'] = 'none'
      downloadHtmlButtonLabel = "" # ignored
      return (downloadHtmlButtonDivStyle, downloadHtmlButtonLabel,
              globals, errorBoxOpen,
              errorBoxTitle, errorBoxChildren)
      
   globals['htmlFileName'] = htmlFileName
   return (downloadHtmlButtonDivStyle, downloadHtmlButtonLabel,
           globals, errorBoxOpen,
           errorBoxTitle, errorBoxChildren)
           
        
#--------------------------------------------------------------------------------
#def createHtmlFromEAF(eafFile, title, projectName, projectDirectory):
#
#   yamlFileName = globals['yamlFileName']
#   htmlFileName = createHtmlFromYaml(yamlFileName, title, projectName, projectDirectory)
#   return htmlFilename
#
#--------------------------------------------------------------------------------
def createHtmlFromYaml(yamlFile, title, projectName, projectDirectory):

   mga = MorphemeGlossAbbreviations()

   print("--- makeHtml.py: createHtmlFromYaml")

   text = YamlToText(yamlFile,
                     grammaticalTerms=mga.getAll(),
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

#--------------------------------------------------------------------------------

downloadHtmlButtonDiv = html.Div(id="downloadHtmlButtonDiv",
                               style={'display': 'none'},
                               children=[html.Button('Download HTML',
                                                     id='downloadHtmlButton',
                                                     style=buttonStyle),
                                    dcc.Download(id="download-html")])

dashApp.layout.children.append(downloadHtmlButtonDiv)

#--------------------------------------------------------------------------------
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



dashApp.layout.children.append(modalLoadSpinnerWatcher)

#m4_include(28.loadAbbreviations.py)
#m4_include(26.loadAudio.py)
#m4_include(createWebPage.py)
#m4_include(23.makeHtml.py)
#m4_include(24.displayAndDownload.py)
#----------------------------------------------------------------------
if __name__ == '__main__':
    port = 9002
    dashApp.run(host='0.0.0.0', debug=True, port=port)
