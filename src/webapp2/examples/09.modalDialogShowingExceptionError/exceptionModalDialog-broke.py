# from https://dash-bootstrap-components.opensource.faculty.ai/docs/components/modal/
import traceback, sys, io

import dash_bootstrap_components as dbc
import flask
from dash import Dash, dcc, html, dash_table, Input, Output, State, callback
from dash.exceptions import PreventUpdate

app = flask.Flask(__name__)
external_stylesheets = [#'https://codepen.io/chriddyp/pen/bWLwgP.css',
                        dbc.themes.BOOTSTRAP]
dashApp = Dash(__name__, server=app, url_base_pathname='/',
                 external_stylesheets=external_stylesheets)

dashApp.title = "modal dialog"

#-------------------------------------------------------
def get_exception_traceback_str(exc: Exception) -> str:
    # Ref: https://stackoverflow.com/a/76584117/
    file = io.StringIO()
    traceback.print_exception(exc, file=file)
    return file.getvalue().rstrip()
#-------------------------------------------------------
modalDiv = html.Div([
    dbc.Modal([
         dbc.ModalHeader(dbc.ModalTitle("Modal Example"), close_button=True),
         dbc.ModalBody("Hi, i'm a modal", id='mainBody'),
         dbc.ModalBody("", id='dynamicModalBody'),
         dbc.ModalFooter(
             dbc.Button(
                 "Close",
                 id="closeButton",
                  className="ms-auto",
                  n_clicks=0,
                 ))],
            id="modalDialog",
            centered=True,
            is_open=True,
        ),
    ])


dashApp.layout=html.Div(
    id="mainDiv",
    children=[
       dcc.Store(id='memoryStore', storage_type='memory'),
       html.H4("Click Button to generate an exception"),
       html.Button("Zero Divide", id="zeroDivideButton", n_clicks=0),
       html.Button("Good Divide", id="goodDivideButton", n_clicks=0),
       modalDiv],
    style={"margin": "100px"}
    )

@callback(
    Output("modalDialog", "is_open", allow_duplicate=True),
    Output("dynamicModalBody", "children", allow_duplicate=True),
    Input("zeroDivideButton", "n_clicks"),
    prevent_initial_call=True
    )
def doZeroDivide(n_clicks, data):
    if n_clicks % 2 == 0:
        return True, n_clicks
    else:
        return False, n_clicks

if __name__ == '__main__':
    print("=============================")
    port = 9009
    print("starting main.py on port %d" % port)
    app.run(host='0.0.0.0', debug=True, port=port)
    print("=============================")
