import flask
import time
import slexil
from datetime import datetime
import base64
import zipfile
import os, io, traceback, time
from dash import html, Dash, callback, dcc, Input, Output, State, dash_table
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify
from slexil.eafParser import EafParser
appVersion = "2.5.2"
versionString = "version: %s, %s" % (slexil.__version__, appVersion)
dbcStyle = dbc.themes.BOOTSTRAP
styleSheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', dbcStyle]

app = flask.Flask(__name__)
dashApp = Dash(__name__, server=app, url_base_pathname='/',
               external_stylesheets=styleSheets)
dashApp.title = "Slexil 2"

#--------------------------------------------------------------------------------
def runBigDemo():

  projectPath = os.path.join("PROJECTS", "timingTest")
  fullPath = os.path.join(projectPath, "4EthelAnita230503Slexil.eaf")
  htmlFile = createWebPage(fullPath, projectPath, "timingTest")
  
#--------------------------------------------------------------------------------
@app.route('/test')
def runTest():

   startTime = time.time()
   runBigDemo()
   endTime = time.time()
   elapsedTime = endTime - startTime
   return "ran slexil webapp2 demo in %s seconds\n" % round(elapsedTime, 2)

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
       return flask.send_file(os.path.join(fullPath))
    else:
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

   dropdown = dbc.DropdownMenu(
      label="Options",
      in_navbar=True,
      align_end=True,
      size="lg",
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


   navbar = dbc.NavbarSimple(
      id="navbar",
      children=[dropdown],
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
         dbc.ModalBody("", id='modalContents')
         ],
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
# explain how media URLs work, how and why you might change them
@callback(
    Output('slexilModal', 'is_open', allow_duplicate=True),
    Output('modalTitle', 'children', allow_duplicate=True),
    Output('modalContents', 'children', allow_duplicate=True),
    Input('explainMediaURLsButton', 'n_clicks'),
    State('memoryStore', 'data'),
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
    State('memoryStore', 'data'),
    prevent_initial_call=True
    )
def displayStateAsList(n_clicks, data):
    el = html.Div(children=["Nothing yet ready on this topic."])
    return True, "Glossing Abbreviations", el
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
      parser.xmlValid()
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
      


#--------------------------------------------------------------------------------
audioLoaderDiv = html.Div(id="audioLoaderDiv",
                          children=[
                              dcc.Upload(
                                  id='audioUploader',
                                  accept=".wav",
                                  children=html.Div([
                                      'Drag and Drop or ',
                                      html.A('Select Audio file')
                                  ], className="fubar"),
                                  className="eafUploader",
                                  multiple=False
                              )], hidden=False)

dashApp.layout.children.append(audioLoaderDiv)
#--------------------------------------------------------------------------------
@callback(
   Output('slexilModal',      'is_open',  allow_duplicate=True),
   Output('modalContents',    'children', allow_duplicate=True),
   Output('memoryStore',      'data',     allow_duplicate=True),
   #Output('createWebpageDiv', 'hidden'),
   Input('audioUploader',    'contents'),
   State('audioUploader',    'filename'),
   State('memoryStore',      'data'),
   prevent_initial_call=True)
def audioUploadHandler(fileContents, filename, data):

   print("=== soundUploadHandler")

   if filename is None:
       return("","",1)

   if data is None:
      data = {}

   data['audioFileName'] = filename;
   modalOpen = False
   modalContents = ""
   
   try:
      fileData = fileContents.encode("utf8").split(b";base64,")[1]
      fullPath = os.path.join(data['projectPath'], filename)
      with open(fullPath, "wb") as fp:
         fp.write(base64.decodebytes(fileData))

      assert(os.path.isfile(fullPath))
      fileSize = os.path.getsize(fullPath)
      data['audioFullPath'] = fullPath
      data['audioFileSize'] = fileSize
      #rate, mtx = wavfile.read(fullPath)
      #data["audioSamplingRate"] = rate
      #print(mtx)

   except BaseException as e:
      modalOpen = True
      modalTitle = "audio upload error"
      modalContents = html.Pre(get_exception_traceback_str(e))

   return modalOpen, modalContents, data





 # data = contents.encode("utf8").split(b";base64,")[1]
    # filename = os.path.join(projectDirectory, name)
    # if not filename[-4:] == ".wav" and not filename[-4:] == ".WAV":
    # 	sound_validationMessage = "Please select a WAVE (.wav) file."
    # 	return sound_validationMessage, "", 1
    # with open(filename, "wb") as fp:
    #    fp.write(base64.decodebytes(data))
    #    fileSize = os.path.getsize(filename)
    #    errorMessage = ""
    #    validSound = True
    #    try:
    #       rate, mtx = wavfile.read(filename)
    #    except ValueError as e:
    #       print("exeption in wavfile: %s" % e)
    #       rate = -1
    #       validSound = False
    #       errorMessage = str(e)
    #    print("sound file size: %d, rate: %d" % (fileSize, rate))
    #    if validSound:
    #    	  sound_validationMessage = "Sound file: %s (%d bytes)" % (name, fileSize)
    #    	  newButtonState = 0
    #    	  return sound_validationMessage, filename, newButtonState
    #    else:
    #    	  if "Unsupported bit depth: the wav file has 24-bit data" in errorMessage:
    #            sound_validationMessage = "File %s (%d byes) has 24-bit data, must be minimum 32-bit."  % (name, fileSize)
    #    	  else:
    #            sound_validationMessage = "ERROR: %s [File: %s (%d bytes)]" % (errorMessage, name, fileSize)
    #    	  newButtonState = 1
    

# from slexil.eafParser import EafParser
from slexil.learnTierGuide import LearnTierGuide
from slexil.text import Text
import os, yaml

def createWebPage(eafFullPath, projectPath, title, preferredMediaURL=None):

   ltg = LearnTierGuide(eafFullPath, verbose=False)
   x = ltg.learnTierGuide()
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
	
   if preferredMediaURL:
       text.setPreferredMediaURL(preferredMediaURL)
       
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
   Output('previewButton', 'hidden'),
   Output('previewButton', 'className'),
   Output('downloadHtmlButton', 'hidden'),
   Output('downloadHtmlButton', 'className'),
   Output('downloadZipFileButton', 'hidden'),
   Output('downloadZipFileButton', 'className'),
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
   previewButtonHidden = False
   previewButtonClass = "enabledButton"
   downloadZipButtonHidden = True
   downloadZipButtonClass = "disabledButton"
   try:
      preferredMediaURL = None
      if "audioFileName" in data.keys():
          preferredMediaURL = data["audioFileName"]
      htmlFilePath = createWebPage(data["eafFullPath"],
                                   data["projectPath"],
                                   data["title"],
                                   preferredMediaURL)
      now = datetime.now()
      currentTime = now.strftime("%H:%M:%S")
      modalOpen = False
      modalContents = ""
      downloadHtmlButtonHidden = False
      downloadHtmlButtonClass = "enabledButton"
      if "audioFileName" in data.keys():
         downloadZipButtonHidden = False
         downloadZipButtonClass = "enabledButton"
   except BaseException as e:
      modalOpen = True
      #modalTitle = "create webpage error"
      modalContents = html.Pre(get_exception_traceback_str(e))
   results = [data, previewButtonHidden,
              previewButtonClass,
              downloadHtmlButtonHidden, downloadHtmlButtonClass,
              downloadZipButtonHidden, downloadZipButtonClass, "",
              modalOpen, modalContents]
   return results
#--------------------------------------------------------------------------------






#--------------------------------------------------------------------------------
downloadAndDisplayDiv = html.Div(id="downloadAndDisplayDiv",
          children=[html.Button("Preview", id="previewButton",
                                n_clicks=0, hidden=True, className="disabledButton"),
                    html.Button("Download Web Page", id="downloadHtmlButton",
                                n_clicks=0, hidden=True, className="disabledButton"),
                    html.Button("Download Web Page with Audio",
                                id="downloadZipFileButton",
                                n_clicks=0, hidden=True, className="disabledButton"),
                    dcc.Download(id="htmlDownloader"),
                    dcc.Download(id="zipDownloader"),
                    html.Iframe(id="displayIFrame",
                                style={"width": "95%", "height": "800px",
                                       "overflow": "auto"})
                    ])
dashApp.layout.children.append(downloadAndDisplayDiv)
#--------------------------------------------------------------------------------
def createZipFile(projectDir, projectTitle, audioFile):
    print("=== entering createZipFile")
    currentDirectoryOnEntry = os.getcwd()
    os.chdir(projectDir)
    print(projectDir)
    filesToSave = []
    filesToSave.insert(0, "%s.html" % projectTitle)
    filesToSave.append(audioFile)

    # zipfile is named for project
    zipFilename = "%s.zip" % projectTitle
    zipFilenameFullPath = os.path.join(currentDirectoryOnEntry, projectDir, zipFilename)
    zipHandle = zipfile.ZipFile(zipFilename, 'w')
    for file in filesToSave:
        zipHandle.write(file)

    zipHandle.close()

    return zipFilenameFullPath

#--------------------------------------------------------------------------------
@callback(
    Output('displayIFrame', 'src'),
    Input('previewButton', 'n_clicks'),
    State('memoryStore', 'data'),
    prevent_initial_call=True
    )
def displayPage(n_clicks, data):
    projectName = data["projectName"]
    htmlFileName = "%s.html" % projectName
    htmlFileFullPath = "PROJECTS/%s/%s" % (projectName, htmlFileName)
    url = "%s" % htmlFileFullPath
    return url

@callback(
    Output('htmlDownloader', 'data'),
    Input('downloadHtmlButton', 'n_clicks'),
    State('memoryStore', 'data'),
    prevent_initial_call=True
    )
def downloadWebPage(n_clicks, data):
    projectName = data["projectName"]
    htmlFileName = "%s.html" % projectName
    htmlFileFullPath = "PROJECTS/%s/%s" % (projectName, htmlFileName)
    return dcc.send_file(htmlFileFullPath)

@callback(
    Output('zipDownloader', 'data'),
    Input('downloadZipFileButton', 'n_clicks'),
    State('memoryStore', 'data'),
    prevent_initial_call=True
    )
def downloadZip(n_clicks, data):
    projectName = data["projectName"]
    projectDir =  "PROJECTS/%s" % projectName
    audioFile = data["audioFileName"]
    zipFilePath = createZipFile(projectDir, projectName, audioFile)
    return dcc.send_file(zipFilePath)

#--------------------------------------------------------------------------------

#----------------------------------------------------------------------
if __name__ == '__main__':
    port = 9002
    dashApp.run(host='0.0.0.0', debug=True, port=port)
