from dash import html, Dash, callback, dcc, Input, Output
import dash_bootstrap_components as dbc

modalDiv = html.Div([
    dbc.Modal([
         dbc.ModalHeader(dbc.ModalTitle("Modal Example"), close_button=True),
         dbc.ModalBody("Hi, i'm a modal", id='mainBody'),
         dbc.ModalBody("", id='placeholderModal'),
         dbc.ModalFooter(
             dbc.Button(
                 "Close",
                 id="closeButton",
                  className="ms-auto",
                  n_clicks=0,
                 ))],
            id="modalExample",
            centered=True,
            is_open=False,
        ),
    ])

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    html.H1('Modal Example Dash App'), 
    html.Button("NYC", id="NYCButton", n_clicks=0, style={"margin": "20px"}),
    html.Button("MTL", id="MTLButton", n_clicks=0, style={"margin": "20px"}),
    html.Button("SF", id="SFButton", n_clicks=0, style={"margin": "20px"}),
    html.Button("Zero Divide", id="zeroDivideButton", n_clicks=0,
                style={"margin": "20px"}),
    modalDiv
    ])

@callback(
    Output('modalExample', 'is_open', allow_duplicate=True),
    Output('placeholderModal', 'children', allow_duplicate=True),
    Input('NYCButton', 'n_clicks'),
    prevent_initial_call=True
    )
def trigger_dynamic_modal(n_clicks):
    return True, "NYC"

@callback(
    Output('modalExample', 'is_open', allow_duplicate=True),
    Output('placeholderModal', 'children', allow_duplicate=True),
    Input('SFButton', 'n_clicks'),
    prevent_initial_call=True
    )
def trigger_dynamic_modal(n_clicks):
    return True, "SF"

@callback(
    Output('modalExample', 'is_open', allow_duplicate=True),
    Output('placeholderModal', 'children', allow_duplicate=True),
    Input('MTLButton', 'n_clicks'),
    prevent_initial_call=True
    )
def trigger_dynamic_modal(n_clicks):
    return True, "MTL"

@callback(
    Output('modalExample', 'is_open', allow_duplicate=True),
    Output('placeholderModal', 'children', allow_duplicate=True),
    Input('zeroDivideButton', 'n_clicks'),
    prevent_initial_call=True
    )
def trigger_dynamic_modal(n_clicks):
    if n_clicks % 2 == 0:
        return True, n_clicks
    else:
        return False, n_clicks

@callback(
    Output('modalExample', 'is_open', allow_duplicate=True),
    Input('closeButton', 'n_clicks'),
    prevent_initial_call=True
    )
def close_modal(_):
    return False

if __name__ == '__main__':
    port = 9012
    app.run(host='0.0.0.0', debug=True, port=port)

    
