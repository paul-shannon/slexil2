import flask
import os, io, traceback, time
from dash import html, Dash, callback, dcc, Input, Output, State, dash_table
import dash_bootstrap_components as dbc
from slexil.eafParser import EafParser
dbcStyle = dbc.themes.BOOTSTRAP
styleSheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', dbcStyle]

app = flask.Flask(__name__)
dashApp = Dash(__name__, server=app, url_base_pathname='/',
                external_stylesheets=styleSheets)
dashApp.title = "input with button"

#buttonStyle={"margin": "10px", "padding": "20px"}
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
dashApp.layout = html.Div(id="mainDiv",
               children=[dcc.Store(id='memoryStore', storage_type='memory'),
                         createNavBar(),
                         dcc.Loading(
                             id="modalLoadWatcher",
                             type="default",
                             children=modalDiv)
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
    print("sleeping in display state")
    time.sleep(3)
    if data is None:
       return(True, "State Variables",
              html.P("state is empty, no variables yet assigned"))
    el = html.Ul(id="list", children=[])
    for key in data.keys():
       el.children.append(html.Li("%s: %s" % (key, data[key])))
    return True, "State Variables", el
#--------------------------------------------------------------------------------
import flask
import os, io, traceback
from dash import html, Dash, callback, dcc, Input, Output, State, dash_table
import dash_bootstrap_components as dbc
from slexil.eafParser import EafParser
from dash_iconify import DashIconify

dbcStyle = dbc.themes.BOOTSTRAP
styleSheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', dbcStyle]

#--------------------------------------------------------------------------------
def createProjectDirectory(projectName):

   path = os.path.join(PROJECTS_DIRECTORY, projectName)
   if not os.path.exists(path):
      os.mkdir(path)
   return path
      
#--------------------------------------------------------------------------------
setTitleDiv = html.Div(id="setTitleDiv",
          children=[
              html.H2('Project Title: ',
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
    print("string size: %d" % characterCount)
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
    return(data)
#--------------------------------------------------------------------------------

#m4_include(12.eafSummaryModalDisplay.py)
#m4_include(22.loadEAF.py)

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
