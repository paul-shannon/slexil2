from dash import html, Dash, callback, dcc, Input, Output
import io, traceback
import dash_bootstrap_components as dbc

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
         dbc.ModalBody("", id='placeholderModal'),
                       #style={"overflow": "auto", "width":"800px"}),
         dbc.ModalFooter(
             dbc.Button("Close", id="closeButton", className="ms-auto",n_clicks=0,))],
         id="modalExample",
         centered=True,
         is_open=False,
         size="lg",
         fullscreen=False,
         scrollable=True,
         ),
     ],
    )


app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    html.H1('Modal Example Dash App'), 
    html.Button("Modulo zero", id="moduloZeroButton", n_clicks=0,
                style={"margin": "20px"}),
    modalDiv
    ])


@callback(
   Output('modalExample', 'is_open', allow_duplicate=True),
   Output('placeholderModal', 'children', allow_duplicate=True),
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
      #modalContents = "error!"
      modalContents = get_exception_traceback_str(e)
   return modalOpen, modalContents
#   if divisor == 0:
#       return True, n_clicks
#   else:
#       return False, n_clicks

@callback(
    Output('modalExample', 'is_open', allow_duplicate=True),
    Input('closeButton', 'n_clicks'),
    prevent_initial_call=True
    )
def close_modal(_):
    return False

if __name__ == '__main__':
    port = 9013
    app.run(host='0.0.0.0', debug=True, port=port)

    
