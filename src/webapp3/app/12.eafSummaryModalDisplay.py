import flask
import os, io, traceback
from dash import html, Dash, callback, dcc, Input, Output, State, dash_table
import dash_bootstrap_components as dbc
from slexil.eafParser import EafParser
dbcStyle = dbc.themes.BOOTSTRAP
#styleSheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', dbcStyle]
styleSheets = [dbcStyle]

app = flask.Flask(__name__)
dashApp = Dash(__name__, server=app, url_base_pathname='/',
                external_stylesheets=external_stylesheets)
dashApp.title = "input with button"

app = Dash(external_stylesheets=styleSheets)
app.title = "EAF Summaries"   
#buttonStyle={"margin": "10px", "padding": "20px"}
buttonStyle = {"margin": "20px",
              "font-size": "20px",
              "border": "1px solid brown",
              "border-radius": "10px"
              }

eafDir = "eafs"
files = os.listdir(eafDir)
eafFiles = [f for f in files if f.endswith("eaf")]
eafFiles.sort()
#-------------------------------------------------------
def get_exception_traceback_str(exc: Exception) -> str:
    # Ref: https://stackoverflow.com/a/76584117/
    file = io.StringIO()
    traceback.print_exception(exc, file=file)
    return file.getvalue().rstrip()
#-------------------------------------------------------
modalDiv = html.Div(
    [dbc.Modal([
         dbc.ModalHeader(dbc.ModalTitle("SLEXIL Notification"), close_button=True),
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
               children=[html.H1('SLEXIL EAF Parsing Demo'), 
                         dcc.Dropdown(eafFiles,
                                      # 'inferno-threeLines.eaf',
                                      id='eafChooser',
                                      style={"width": "400px"}),
                         html.Button("Summarize EAF", id="summarizeEafButton", n_clicks=0, style=buttonStyle),
                         dcc.Loading(
                             id="modalLoadWatcher",
                             type="default",
                             children=modalDiv)
                         ],
                      style={"margin": "50px"})
#----------------------------------------------------------------------
@callback(
    Output('slexilModal', 'is_open', allow_duplicate=True),
    Output('modalContents', 'children', allow_duplicate=True),
    Input('summarizeEafButton', 'n_clicks'),
    State('eafChooser', 'value'),
    prevent_initial_call=True
    )
def summarizeEaf(n_clicks, eafFilename):
    print("--- %s" % eafFilename)
    eafFilePath = "%s/%s" % (eafDir, eafFilename)
    try:
       parser = EafParser(eafFilePath, verbose=True, fixOverlappingTimeSegments=False)
       tbl_tiers = parser.getTierTable()
       dashTable_tiers = dash_table.DataTable(tbl_tiers.to_dict('records'),
                                              [{"name": i, "id": i} for i in tbl_tiers.columns],
                                              style_cell={'fontSize':20, 'font-family':'courier'})
       tierTableDiv = html.Div(id="tierTable",
                               children=[dashTable_tiers],
                               style = {"width": "95%", "margin": "20",
                                        "overflow": "auto",
                                        "padding": "6px",
                                        "border": "1px solid gray",
                                        "border-radius": "10px"})
       tbl_line0 = parser.getAllLinesTable()[0]
       dashTable_lines = dash_table.DataTable(tbl_line0.to_dict('records'),
                                              [{"name": i, "id": i} for i in tbl_line0.columns],
                                              style_cell={'fontSize':18, 'font-family':'courier'})
       lineTableDiv = html.Div(id="lineTable",
                               children=[dashTable_lines],
                               style = {"width": "95%", "margin": "20",
                                        "margin-top": "40px",
                                        "padding": "6px",
                                        "overflow": "auto",
                                        "border": "1px solid gray",
                                        "border-radius": "10px"})
       return True, [tierTableDiv] #, lineTableDiv]
    except BaseException as e:
       success = False
       modalContents = get_exception_traceback_str(e)
       return True, html.Pre(modalContents)


    
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
    port = 80
    dashApp.run(host='0.0.0.0', debug=True, port=port)
