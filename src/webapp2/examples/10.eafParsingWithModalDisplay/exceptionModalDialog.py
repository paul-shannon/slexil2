from dash import html, Dash, callback, dcc, Input, Output
import io, traceback
import dash_bootstrap_components as dbc
from slexil.eafParser import EafParser

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
         #dbc.ModalBody("Hi, i'm a modal", id='mainBody'),
         dbc.ModalBody("", id='modalContents'),
                       #style={"overflow": "auto", "width":"800px"}),
         dbc.ModalFooter(
             dbc.Button("Close", id="closeButton", className="ms-auto",n_clicks=0,))],
         id="slexilModal",
         centered=True,
         is_open=False,
         size="lg",
         fullscreen=False,
         scrollable=True,
         )])
#-------------------------------------------------------
app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

buttonStyle={"margin": "10px", "padding": "20px"}
app.layout = html.Div([
    html.H1('SLEXIL EAF Parsing Demo'), 
    html.Button("Modulo zero", id="moduloZeroButton", n_clicks=0, style=buttonStyle),
    html.Button("Good EAF",   id="goodEafButton", n_clicks=0, style=buttonStyle),
    html.Button("Broken EAF", id="brokenEafButton", n_clicks=0, style=buttonStyle),
    modalDiv],
    style={"margin": "50px"})
#----------------------------------------------------------------------
@callback(
   Output('slexilModal', 'is_open', allow_duplicate=True),
   Output('modalContents', 'children', allow_duplicate=True),
   Input('moduloZeroButton', 'n_clicks'),
   prevent_initial_call=True
   )
def trigger_dynamic_modal(n_clicks):
   divisor = n_clicks % 2
   modalOpen = False
   modalContents = "no message"
   try:
      x = 5 / divisor
   except Exception as e:
      modalOpen = True
      modalContents = html.Pre(get_exception_traceback_str(e))
   return modalOpen, modalContents
#----------------------------------------------------------------------
@callback(
    Output('slexilModal', 'is_open', allow_duplicate=True),
    Input('closeButton', 'n_clicks'),
    prevent_initial_call=True
    )
def close_modal(_):
    return False
#----------------------------------------------------------------------
@callback(
    Output('slexilModal', 'is_open', allow_duplicate=True),
    Output('modalContents', 'children', allow_duplicate=True),
    Input('goodEafButton', 'n_clicks'),
    prevent_initial_call=True
    )
def handleGoodEAF(n_clicks):
    success = True
    f = "inferno-threeLines.eaf"
    try:
       parser = EafParser(f, verbose=True, fixOverlappingTimeSegments=False)
       tbl = parser.getTierTable()
       #dashTable = dash_table.DataTable(tbl.to_dict('records'),
       #                                 [{"name": i, "id": i} for i in tbl.columns])
       return True, "good eaf? %s %s" % (success, f)
    except BaseException as e:
       success = False
       print("--- exception caught")
       print(e.args[2])

#----------------------------------------------------------------------
@callback(
    Output('slexilModal', 'is_open', allow_duplicate=True),
    Output('modalContents', 'children', allow_duplicate=True),
    Input('brokenEafButton', 'n_clicks'),
    prevent_initial_call=True
    )
def handleGoodEAF(n_clicks):
    success = True
    f = "inferno-misnamedParentRef.eaf"
    try:
       parser = EafParser(f, verbose=True, fixOverlappingTimeSegments=False)
       return True, "%s is a legal eaf" % f
    except BaseException as e:
       success = False
       modalContents = get_exception_traceback_str(e)
       return True, html.Pre(modalContents)

#----------------------------------------------------------------------
if __name__ == '__main__':
    port = 9013
    app.run(host='0.0.0.0', debug=True, port=port)

    
