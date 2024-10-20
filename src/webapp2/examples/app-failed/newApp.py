import flask
import os, io, traceback, pdb
from dash import html, Dash, callback, dcc, Input, Output, State, dash_table
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify
import base64
from slexil.eafParser import EafParser

#-------------------------------------------------------
dbcStyle = dbc.themes.BOOTSTRAP
styleSheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', dbcStyle]

#--------------------------------------------------------------------------------
# the webapp requires a PROJECTS_DIRECTORY in the current working directory
# each individual project, one for each text, is created as a subdirectory here

PROJECTS_DIRECTORY = "PROJECTS"
try:
    assert(os.path.exists(PROJECTS_DIRECTORY))
except AssertionError:
    os.mkdir(PROJECTS_DIRECTORY)
#--------------------------------------------------------------------------------
def createProjectDirectory(projectName):

   path = os.path.join(PROJECTS_DIRECTORY, projectName)
   if not os.path.exists(path):
      os.mkdir(path)
   return path
      
#--------------------------------------------------------------------------------
app = flask.Flask(__name__)
dashApp = Dash(__name__, server=app, url_base_pathname='/',
               external_stylesheets=styleSheets)
 #              suppress_callback_exceptions=True)
dashApp.title = "webapp2"
#-------------------------------------------------------
def get_exception_traceback_str(exc: Exception) -> str:
    # Ref: https://stackoverflow.com/a/76584117/
    file = io.StringIO()
    traceback.print_exception(exc, file=file)
    return file.getvalue().rstrip()
#-------------------------------------------------------
slexilModalDiv = html.Div(
         [dbc.Modal([
             dbc.ModalHeader(dbc.ModalTitle("SLEXIL Notification",
                                            className="bodyStyle",
                                            id="modalTitle"),
                             close_button=True),
             dbc.ModalBody("", id='modalContents', className="bodyStyle")],
                    id="slexilModal",
                    centered=True,
                    is_open=False,
                    size="xl",    # sm, lg, xl
                    fullscreen=False,
                    scrollable=True
                    )], className="bodyStyle")
#-------------------------------------------------------
navbar = dbc.NavbarSimple(
    id="navbar",
    children=[
        dbc.NavItem(html.Button("Examine State", id="examineStateButton", n_clicks=0,
                                className="enabledButton")),
             ],
    brand="SLEXIL Webapp 2",
    color="#F5FAF3",
    dark=False,
    )
#-------------------------------------------------------
dashApp.layout = html.Div(id="mainDiv",
   children=[navbar,
             #dcc.Loading(id="modalLoadWatcher", type="default", children=slexiModalDiv),
             dcc.Store(id='memoryStore', storage_type='memory'),
             slexilModalDiv,
             #html.Button("Examine State", id="examineStateButton", n_clicks=0,
             #            className="enabledButton"),
             ],className="bodyStyle")
#----------------------------------------------------------------------
@callback(
    Output('slexilModal', 'is_open', allow_duplicate=True),
    Output('modalTitle', 'children', allow_duplicate=True),
    Output('modalContents', 'children', allow_duplicate=True),
    Input('examineStateButton', 'n_clicks'),
    State('memoryStore', 'data'),
    prevent_initial_call=True
    )
def displayStateAsList(n_clicks, data):
    if data is None:
       return(True, "State Variables",
              html.P("state is empty, no variables yet assigned"))
    el = html.Ul(id="list", children=[])
    for key in data.keys():
       el.children.append(html.Li("%s: %s" % (key, data[key])))
    return True, "State Variables", el
#--------------------------------------------------------------------------------
setTitleDiv = html.Div(children=[
                 html.H2('Project Title: ',
                         style={'display':'inline-block', 'marginRight': "20px",
                                'marginLeft': "20px",
                                "fontSize": "24px"}),
                 dcc.Input(id='projectNameInput',type='text',
                           #placeholder='',
                           style={'display':'inline-block', 'fontSize': "24px",
                                  'width': '400px'}),
                 html.Button("Submit", id="setProjectNameButton", n_clicks=0,
                             disabled=True, className="disabledButton"),
                 html.Div(id="projectTitleHelp", children=[
                    DashIconify(icon="feather:info", color="blue",width=30),
                    ], className="helpButtonDiv")
             ])
#----------------------------------------------------------------------
@callback(
    Output('setProjectNameButton', 'className'),
    Output('setProjectNameButton', 'disabled'),
    Input('projectNameInput', 'value'),
    prevent_initial_call=True)
def handleProjectNameInputChars(value):
    s = value.strip()
    characterCount = len(s)
    print("string %s,  size: %d" % (s, len(s)))
    minCharacterCount = 3
    if(characterCount >= minCharacterCount):
        return "enabledButton", False
    else:
        return "disabledButton", True

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

#----------------------------------------------------------------------
@callback(
    Output('memoryStore', 'data'),
    Output('eafLoaderDiv', 'style'),
    Input('setProjectNameButton', 'n_clicks'),
    State('projectNameInput', 'value'),
    State('memoryStore', 'data'),
    prevent_initial_call=True)
def handleSetProjectNameButton(n_clicks, userEnteredString, data):
    print("--- handleSetProjectNameButton: %d, %s" % (n_clicks, userEnteredString))
    title = userEnteredString.strip()
    newProjectName = title.replace(" ", "_")
    projectPath = createProjectDirectory(newProjectName)
    if data is None:
       print("initializing None data")
       data = {}
    data['title'] = title
    data['projectName'] = newProjectName
    data['projectPath'] = projectPath
    return(data, {'display': 'inline-block'})
#--------------------------------------------------------------------------------
dashApp.layout.children.append(setTitleDiv)

#--------------------------------------------------------------------------------
# the webapp requires a PROJECTS_DIRECTORY in the current working directory
# each individual project, one for each text, is created as a subdirectory here
PROJECTS_DIRECTORY = "PROJECTS"
try:
    assert(os.path.exists(PROJECTS_DIRECTORY))
except AssertionError:
    os.mkdir(PROJECTS_DIRECTORY)
#--------------------------------------------------------------------------------
eafDir = "eafs"
files = os.listdir(eafDir)
eafFiles = [f for f in files if f.endswith("eaf")]
eafFiles.sort()
print("eaf count: %d" % len(eafFiles))
#--------------------------------------------------------------------------------
def createProjectDirectory(projectName):

   path = os.path.join(PROJECTS_DIRECTORY, projectName)
   if not os.path.exists(path):
      os.mkdir(path)
   return path
      
#--------------------------------------------------------------------------------
eafModalDiv = html.Div(
    [dbc.Modal([
         dbc.ModalHeader(dbc.ModalTitle("EAF Structure",
                                        className="bodyStyle",
                                        id="eafModalTitle"),
                         close_button=True),
         dbc.ModalBody("", id='eafModalContents', className="bodyStyle")],
         id="eafModalDiv",
         centered=True,
         is_open=False,
         size="xl",    # sm, lg, xl
         fullscreen=False,
         scrollable=True
         )], className="bodyStyle")

#-------------------------------------------------------
loadWatcher = dcc.Loading(id="eafLoadWatcher", type="default",
                          children=slexilModalDiv)
eafLoaderDiv = html.Div(id="eafLoaderDiv",
                        children = [dcc.Upload(
                            id='eafUploader',
                            accept=".eaf",
                            children=html.Div([
                                'Drag and Drop or ',
                                html.A('Select EAF File')
                                ], className="fubar"),
                            className="eafUploader",
                            multiple=False
                            )], style={"display": "none"})
#--------------------------------------------------------------------------------
#dashApp.layout.children.append(loadWatcher)
dashApp.layout.children.append(eafLoaderDiv)
#----------------------------------------------------------------------
@callback(
    Output('memoryStore', 'data', allow_duplicate=True),
    Output('slexilModal', 'is_open', allow_duplicate=True),
    Output('modalTitle', 'children', allow_duplicate=True),
    Output('modalContents', 'children', allow_duplicate=True),
    Input('eafUploader',    'contents'),
    State('eafUploader',    'filename'),
    State('memoryStore', 'data'),
    prevent_initial_call=True)
def analyzeEAF(fileContents, filename, data):
   print("entering analyzeEAF callback")
   if data is None:
      data = {}
   data['eafFileName'] = filename

   try:
      fileData = fileContents.encode("utf8").split(b";base64,")[1]
      fullPath = os.path.join(data['projectPath'], filename)
      with open(fullPath, "wb") as fp:
         fp.write(base64.decodebytes(fileData))
      assert(os.path.isfile(fullPath))
      fileSize = os.path.getsize(fullPath)
      data['eafFullPath'] = fullPath
      data['fileSize'] = fileSize
      parser = EafParser(fullPath, verbose=True, fixOverlappingTimeSegments=False)
      el = html.Ul(id="eafAttributes", children=[]);

      lineCount = parser.getLineCount()
      data["lineCount"] = lineCount
      el.children.append(html.Li("lineCount: %s" % lineCount))

      audioURL = parser.getAudioURL()
      data["audioURL"] = audioURL
      el.children.append(html.Li("audioURL: %s" % audioURL))

      videoURL = parser.getVideoURL()
      data["videoURL"] = videoURL
      el.children.append(html.Li("videoURL: %s" % videoURL))

      timeAlignedTiers = parser.getTimeAlignedTiers()
      data["timeAlignedTiers"] = timeAlignedTiers

      el.children.append(html.Li("time-aligned tiers: %s" % timeAlignedTiers))

      i = 1
      for tal in timeAlignedTiers:
         tierGroup = parser.getTimeAlignedTierFamily(tal)
         title = "tier group %d" % i
         data[title] = tierGroup
         el.children.append(html.Li("%s: %s" % (title, tierGroup)))
         i += 1
      modalOpen = True
      modalContents = el
      modalTitle = "%s info" % data['projectName']
   except BaseException as e:
      modalOpen = True
      modalTitle = "eaf error"
      modalContents = html.Pre(get_exception_traceback_str(e))

   return data, modalOpen, modalTitle, modalContents
   
#--------------------------------------------------------------------------------
dashApp.layout.children.append(loadWatcher)

if __name__ == '__main__':
    port = 8085
    dashApp.run(host='0.0.0.0', debug=False, port=port)

