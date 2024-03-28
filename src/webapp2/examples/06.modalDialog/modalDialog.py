# from https://dash-bootstrap-components.opensource.faculty.ai/docs/components/modal/
import dash_bootstrap_components as dbc
import flask
from dash import Dash, dcc, html, dash_table, Input, Output, State, callback
from dash.exceptions import PreventUpdate

app = flask.Flask(__name__)
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
dashApp = Dash(__name__, server=app, url_base_pathname='/',
#                external_stylesheets=external_stylesheets)
                 external_stylesheets=[dbc.themes.BOOTSTRAP])

dashApp.title = "modal dialog"

modal = html.Div(
    [dbc.Button("Open modal", id="modalOpenButton", n_clicks=0),
     dbc.Modal([dbc.ModalHeader(dbc.ModalTitle("Header")),
                dbc.ModalBody("This is the content of the modal"),
                dbc.ModalFooter(
                    dbc.Button(
                        "Close", id="modalCloseButton", className="ms-auto", n_clicks=0
                    ))],
               id="modal",
               is_open=False,
               )],
     style={"margin": "100px"}
     ) # modal div

dashApp.layout=modal

@callback(
    Output("modal", "is_open"),
    Input("modalOpenButton", "n_clicks"),
    Input("modalCloseButton", "n_clicks"),
    [State("modal", "is_open")],
    )
def toggle_modal(n_open, n_close, is_open):
    if n_open or n_close:
        return not is_open
    return is_open


if __name__ == '__main__':
    print("=============================")
    port = 9009
    print("starting main.py on port %d" % port)
    app.run(host='0.0.0.0', debug=True, port=port)
    print("=============================")
