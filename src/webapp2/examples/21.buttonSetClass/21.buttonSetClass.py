from dash import Dash, dcc, html, Input, Output, State, callback

app = Dash(__name__)
app.title = "button set className"


bigStyle = {"margin": "20px",
            "font-size": "24px",
            "border": "1px solid brown",
            "width": "300px",
            "height": "300px"
            }

app.layout = html.Div([
    html.Button('Submit', className="liveButton", id='submitButton',
                n_clicks=0),
    dcc.Dropdown(id='toggleButton',
                 options=[{'value': True, 'label': 'Disable'},
                          {'value': False, 'label': 'Enable'}],
                 style={"font-size": "24px", "width": "400px",
                        "height":"80px"}),
    html.Div(id='textOutputDiv',style=bigStyle)
    ])


@callback(
    Output('textOutputDiv', 'children'),
    Input('submitButton', 'n_clicks'),
    prevent_initial_call=True
    )
def handleSubmit(n_clicks):
    return n_clicks

@callback(
    Output('submitButton', 'className'),
    Output('submitButton', 'disabled'),
    Input('toggleButton', 'value'),
    prevent_initial_call=True
    )
def update_output(disabled):
    print("disabled: %s" % disabled)
    newClassName = "disabledButton"
    if not disabled:
       newClassName = "liveButton"
    return newClassName, disabled

if __name__ == '__main__':
    port = 9999
    app.run(host='0.0.0.0', debug=True, port=port)
    
