import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Modal component
modal = dbc.Modal(
    [
        dbc.ModalHeader(dbc.ModalTitle("Error")),
        dbc.ModalBody("An error occurred."),
    ],
    id="error-modal",
    is_open=False,
)

app.layout = html.Div(
    [
        dcc.Input(id="input-value", type="number"),
        html.Button("Calculate", id="calculate-button"),
        modal,
    ]
)

@app.callback(
    Output("error-modal", "is_open"),
    Output("error-modal", "children"),
    Input("calculate-button", "n_clicks"),
    State("input-value", "value"),
)
def calculate(n_clicks, value):
    if n_clicks:
        try:
            # Perform your calculations here
            result = 10 / value
        except Exception as e:
            return True, dbc.ModalBody(f"Error: {e}")
    return False, None

if __name__ == "__main__":
    app.run_server(debug=True, port=8051)
    
