import flask
from datetime import datetime
import base64
import os, io, traceback, time
from dash import html, Dash, callback, dcc, Input, Output, State, dash_table
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify
from slexil.eafParser import EafParser

dbcStyle = dbc.themes.BOOTSTRAP
styleSheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', dbcStyle]

app = flask.Flask(__name__)
dashApp = Dash(__name__, server=app, url_base_pathname='/',
               external_stylesheets=styleSheets)
dashApp.title = "Slexil 2"

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
    return None
#--------------------------------------------------------------------------------
buttonStyle = {"margin": "20px",
              "font-size": "20px",
              "border": "1px solid brown",
              "border-radius": "10px"
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
eafDir = "eafs"
files = os.listdir(eafDir)
eafFiles = [f for f in files if f.endswith("eaf")]
eafFiles.sort()
print("eaf count: %d" % len(eafFiles))
#-------------------------------------------------------
def createNavBar():

   navbar = dbc.NavbarSimple(
      id="navbar",
      children=[
        dbc.NavItem(html.Button("Examine State", id="examineStateButton", n_clicks=0,
                                className="enabledButton"))],
       brand="SLEXIL Webapp 2",
       color="#F5FAF3",
       dark=False,
       )

   return navbar
#-------------------------------------------------------
def get_exception_traceback_str(exc: Exception) -> str:
    # Ref: https://stackoverflow.com/a/76584117/
    file = io.StringIO()
    traceback.print_exception(exc, file=file)
    return file.getvalue().rstrip()
#-------------------------------------------------------
modalDiv = html.Div(
    [dbc.Modal([
         dbc.ModalHeader(
            dbc.ModalTitle("SLEXIL Notification", id="modalTitle"), close_button=True),
         dbc.ModalBody("", id='modalContents'),
         dbc.ModalFooter(
             dbc.Button("Close", id="modalCloseButton", className="ms-auto",n_clicks=0,))],
         id="slexilModal",
         centered=True,
         is_open=False,
         size="xl",    # sm, lg, xl
         fullscreen=False,
         scrollable=True,
         )])
#-------------------------------------------------------
loadTrackerDiv = html.Div(id="loadTrackerDiv")
dashApp.layout = html.Div(id="mainDiv",
               children=[dcc.Store(id='memoryStore', storage_type='memory'),
                         createNavBar(),
                         dcc.Loading(
                             id="modalLoadWatcher",
                             type="default",
                             children=[modalDiv, loadTrackerDiv])
                         ],
                      style={"margin": "5px"})
#----------------------------------------------------------------------
# navbar button displays state in a modal dialog
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
              dcc.Input(id='projectNameInput',type='text',
                        placeholder='',
                        style={'display':'inline-block', 'fontSize': "24px",
                               'width': '400px'}),
              html.Button("Submit", id="setProjectNameButton", n_clicks=0,
                          disabled=True, className="disabledButton"),
              html.Div(id="projectTitleHelp", children=[
                  DashIconify(icon="feather:info", color="blue",width=30),
              ], style={"display": "inline-block"})
          ],className="bodyStyle")
#----------------------------------------------------------------------
dashApp.layout.children.append(setTitleDiv)
#----------------------------------------------------------------------
@callback(
    Output('setProjectNameButton', 'className'),
    Output('setProjectNameButton', 'disabled'),
    Input('projectNameInput', 'value'),
    prevent_initial_call=True)
def handleProjectNameInputChars(userEnteredString):
    characterCount = len(userEnteredString)
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
    Output('eafLoaderDiv', 'hidden'),
    Input('setProjectNameButton', 'n_clicks'),
    State('projectNameInput', 'value'),
    State('memoryStore', 'data'),
    prevent_initial_call=True)
def handleSetProjectNameButton(n_clicks, userEnteredString, data):
    title = userEnteredString.strip()
    newProjectName = title.replace(" ", "_")
    projectPath = createProjectDirectory(newProjectName)
    if data is None:
       print("initializing None data")
       data = {}
    data['title'] = title
    data['projectName'] = newProjectName
    data['projectPath'] = projectPath
    return(data, False)
#--------------------------------------------------------------------------------

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
                            )], hidden=True)

dashApp.layout.children.append(eafLoaderDiv)
#--------------------------------------------------------------------------------
@callback(
   Output('slexilModal',      'is_open',  allow_duplicate=True),
   Output('modalContents',    'children', allow_duplicate=True),
   Output('memoryStore',      'data',     allow_duplicate=True),
   Output('createWebpageDiv', 'hidden'),
   Input('eafUploader',    'contents'),
   State('eafUploader',    'filename'),
   State('memoryStore',    'data'),
   prevent_initial_call=True)
def eafUploadHandler(fileContents, filename, data):

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
      tbl_tiers = parser.getTierTable()
        # discard the DEFAULT_LOCALE column
      tbl_tiers = tbl_tiers[["TIER_ID", "LINGUISTIC_TYPE_REF", "PARENT_REF", "TIME_ALIGNABLE"]]
      dashTable_tiers = dash_table.DataTable(tbl_tiers.to_dict('records'),
                                             [{"name": i, "id": i} for i in tbl_tiers.columns],
                                             style_cell={'fontSize':20, 'font-family':'courier'})
      print("--- build tier table")
      tierTableDiv = html.Div(id="tierTable",
                               children=[dashTable_tiers],
                                  style = {"width": "95%", "margin": "20",
                                           "overflow": "auto",
                                           "padding": "6px",
                                           "border": "1px solid gray",
                                           "border-radius": "10px"})

      data['tiers'] = tierTableDiv
      modalOpen = False
      modalContents = tierTableDiv
      modalTitle = "EAF Tiers"
      hideCreateWebpageButton = False
   except BaseException as e:
      modalOpen = True
      modalTitle = "eaf error"
      modalContents = html.Pre(get_exception_traceback_str(e))
      hideCreateWebpageButton = True
   return modalOpen, modalContents, data, hideCreateWebpageButton
      


from slexil.eafParser import EafParser
from slexil.text import Text
import os, yaml

def createWebPage(eafFullPath, projectPath, title):

   parser = EafParser(eafFullPath, verbose=False, fixOverlappingTimeSegments=False)
   x = parser.learnTierGuide()
   print(x)
   tierGuideYamlFile = os.path.join(projectPath, "tierGuide.yaml")
   with open(tierGuideYamlFile, 'w') as outfile:
      yaml.dump(x, outfile, default_flow_style=False)
   
   text = Text(xmlFilename=eafFullPath,
               grammaticalTermsFile=None,
               tierGuideFile=tierGuideYamlFile,
               projectDirectory=projectPath,
               verbose=True,
               fontSizeControls = False,
               startLine = None,
               endLine = None,
               pageTitle = title,
               helpFilename = None,
               helpButtonLabel = "",
               kbFilename = None,
               linguisticsFilename = None,
               webpackLinksOnly = False ,
               fixOverlappingTimeSegments = False,
               useTooltips=False)
	
   filename = title.replace(" ", "_")
   filename = "%s.html" % filename
   htmlText = text.toHTML()
   filePath = os.path.join(projectPath, filename)
   print ("writing html to '%s'" % filePath)
   f = open(filePath, "wb")
   f.write(bytes(htmlText, "utf-8"))
   f.close()
   return filePath

#--------------------------------------------------------------------------------
# createWebPage("PROJECTS/x33/inferno-threeLines-outOfTimeOrder.eaf", "PROJECTS/x33", "test")
   

#--------------------------------------------------------------------------------
createWebpageDiv = html.Div(id="createWebpageDiv",
          children=[
              html.Button("Create Web Page", id="createWebpageButton", n_clicks=0,
                          disabled=False, className="enabledButton"),
              html.Div(id="createWebpageHelp", children=[
                  DashIconify(icon="feather:info", color="blue",width=30),
               ], style={"display": "inline-block"}),
             #html.Iframe(id="htmlPreviewDiv",
             #         style={"width": "95%", "height": "400px",
             #                "border": "1px solid blue"})
          ],className="bodyStyle", hidden=True)
#----------------------------------------------------------------------
dashApp.layout.children.append(createWebpageDiv)
#----------------------------------------------------------------------
@callback(
    Output('slexilModal', 'is_open', allow_duplicate=True),
    Output('modalTitle', 'children', allow_duplicate=True),
    Output('modalContents', 'children', allow_duplicate=True),
    Input('createWebpageHelp', 'n_clicks'),
    prevent_initial_call=True
    )
def displayCreateWebpageHelp(n_clicks):
    contents = html.Ul(id="list",
       children=[html.Li("explanation for createWebpage coming soon")
                 ])
    
    return True, "Help for Create Webpage", contents

#----------------------------------------------------------------------
@callback(
   Output('memoryStore', 'data', allow_duplicate=True),
   Output('displayStaticHTMLButton', 'hidden'),
   Output('displayStaticHTMLButton', 'className'),
   Output('downloadWebPageButton', 'hidden'),
   Output('downloadWebPageButton', 'className'),
   Output('loadTrackerDiv', 'children', allow_duplicate=True),
   Output('slexilModal',      'is_open',  allow_duplicate=True),
   Output('modalContents',    'children', allow_duplicate=True),
   Input('createWebpageButton', 'n_clicks'),
   State('memoryStore', 'data'),
   prevent_initial_call=True)
def createWebpageCallback(n_clicks, data):
   if data is None:
      print("initializing None data in 23.makeHtml.py")
      data = {}
      data['webpage creation time'] = currentTime
   try:
      htmlFilePath = createWebPage(data["eafFullPath"], data["projectPath"], data["title"])
      now = datetime.now()
      currentTime = now.strftime("%H:%M:%S")
      modalOpen = False
      modalContents = ""
      nextStepButtonHidden = False
      nextStepButtonClass = "enabledButton"
   except BaseException as e:
      modalOpen = True
      #modalTitle = "create webpage error"
      modalContents = html.Pre(get_exception_traceback_str(e))
      nextStepButtonHidden = True
      nextStepButtonClass = "disabledButton"
    
   return data, nextStepButtonHidden, nextStepButtonClass, nextStepButtonHidden, nextStepButtonClass, "", modalOpen, modalContents
#--------------------------------------------------------------------------------






#--------------------------------------------------------------------------------
downloadAndDisplayDiv = html.Div(id="downloadAndDisplayDiv",
          children=[html.Button("Display", id="displayStaticHTMLButton",
                                n_clicks=0, hidden=True, className="disabledButton"),
                    html.Button("Download Web Page", id="downloadWebPageButton",
                                n_clicks=0, hidden=True, className="disabledButton"),
                    dcc.Download(id="downloader"),
                    html.Iframe(id="displayIFrame",
                                style={"width": "95%", "height": "800px",
                                       "overflow": "auto"})
                    ])
dashApp.layout.children.append(downloadAndDisplayDiv)
#--------------------------------------------------------------------------------
@callback(
    Output('displayIFrame', 'src'),
    Input('displayStaticHTMLButton', 'n_clicks'),
    State('memoryStore', 'data'),
    prevent_initial_call=True
    )
def displayPage(n_clicks, data):
    projectName = data["projectName"]
    htmlFileName = "%s.html" % projectName
    htmlFileFullPath = "PROJECTS/%s/%s" % (projectName, htmlFileName)
    url = "http://127.0.0.1:9020/%s" % htmlFileFullPath
    return url

@callback(
    Output('downloader', 'data'),
    Input('downloadWebPageButton', 'n_clicks'),
    State('memoryStore', 'data'),
    prevent_initial_call=True
    )
def downloadWebPage(n_clicks, data):
    projectName = data["projectName"]
    htmlFileName = "%s.html" % projectName
    htmlFileFullPath = "PROJECTS/%s/%s" % (projectName, htmlFileName)
    return dcc.send_file(htmlFileFullPath)

#--------------------------------------------------------------------------------
if __name__ == '__main__':
    port = 9020
    dashApp.run(host='0.0.0.0', debug=True, port=port)

#----------------------------------------------------------------------
@callback(
    Output('slexilModal', 'is_open', allow_duplicate=True),
    Input('modalCloseButton', 'n_clicks'),
    prevent_initial_call=True
    )
def close_modal(_):
    return False
#----------------------------------------------------------------------
if __name__ == '__main__':
    port = 9018
    dashApp.run(host='0.0.0.0', debug=True, port=port)
