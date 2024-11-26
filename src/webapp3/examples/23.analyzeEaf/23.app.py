import flask
import os, io, traceback, pdb
from dash import html, Dash, callback, dcc, Input, Output, State, dash_table
import dash_bootstrap_components as dbc

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
modalDiv = html.Div(
    [dbc.Modal([
         dbc.ModalHeader(dbc.ModalTitle("SLEXIL Notification",
                                        className="bodyStyle",
                                        id="modalTitle"),
                         close_button=True),
         dbc.ModalBody("", id='modalContents', className="bodyStyle"),
         ],
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
             #dcc.Loading(id="modalLoadWatcher", type="default", children=modalDiv),
             dcc.Store(id='memoryStore', storage_type='memory'),
             modalDiv,
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

from slexil.eafParser import EafParser
eafFiles = os.listdir("eafs/")
eafFiles.sort()

analyzeEafDiv = html.Div(id="analyzeEafDiv",
     children=[dcc.Dropdown(eafFiles, id='eafFileSelector',
              style={"fontSize": "24px", "width": "500px"})])
     
dashApp.layout.children.append(analyzeEafDiv)

@callback(
    Output('memoryStore', 'data', allow_duplicate=True),
    Output('slexilModal', 'is_open', allow_duplicate=True),
    Output('modalTitle', 'children', allow_duplicate=True),
    Output('modalContents', 'children', allow_duplicate=True),
    Input('eafFileSelector', 'value'),
    State('memoryStore', 'data'),
    prevent_initial_call=True)
def analyzeEAF(filename, data):
   print("entering analyzeEAF callback")
   filename = os.path.join("eafs", filename)
   parser = EafParser(filename, verbose=False, fixOverlappingTimeSegments=False)
   el = html.Ul(id="eafAttributes", children=[]);
   if data is None:
      data = {}

   el.children.append(html.Li("lineCount: %s" % parser.getLineCount()))
   el.children.append(html.Li("audioURL: %s" % parser.getAudioURL()))
   el.children.append(html.Li("videoURL: %s" % parser.getVideoURL()))
   timeAlignedTiers = parser.getTimeAlignedTiers()
   el.children.append(html.Li("time-aligned tiers: %s" % timeAlignedTiers))
   i = 1
   for tal in timeAlignedTiers:
      tierFamily = parser.getTimeAlignedTierFamily(tal)
      el.children.append(html.Li("  tier group %d: %s" % (i, tierFamily)))
      i += 1

   return data, True, "Analysis of %s" % filename, el
   





if __name__ == '__main__':
    port = 8083
    dashApp.run(host='0.0.0.0', debug=True, port=port)
