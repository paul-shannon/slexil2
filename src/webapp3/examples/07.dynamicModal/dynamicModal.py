from dash import html, Dash, callback, dcc, Input, Output
import dash_bootstrap_components as dbc

modal = html.Div([
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Modal Example"), close_button=True),
                dbc.ModalBody("Hi, i'm a modal", id='mainBody'),
                dbc.ModalBody("", id='placeholderModal'),
                dbc.ModalFooter(
                    dbc.Button(
                        "Close",
                        id="closeButton",
                        className="ms-auto",
                        n_clicks=0,
                    )
                ),
            ],
            id="modalExample",
            centered=True,
            is_open=False,
        ),
    ])

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    html.H1('Modal Example Dash App'), 
    dcc.Dropdown(['NYC', 'MTL', 'SF'], 'NYC', id='demo-dropdown'),
    modal
])

@callback(
    Output('modalExample', 'is_open'),
    Output('placeholderModal', 'children'),
    Input('demo-dropdown', 'value'),
    prevent_initial_call=True
)
def trigger_dynamic_modal(dropdown_value:str):
    return True, dropdown_value

@callback(
    Output('modalExample', 'is_open', allow_duplicate=True),
    Input('closeButton', 'n_clicks'),
    prevent_initial_call=True
)
def close_modal(_):
    return False

if __name__ == '__main__':
    port = 9010
    app.run(host='0.0.0.0', debug=True, port=port)

    
