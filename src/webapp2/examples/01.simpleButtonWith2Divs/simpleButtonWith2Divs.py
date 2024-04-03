from dash import Dash, dcc, html, Input, Output, State, callback

app = Dash(__name__)
app.title = "example from web"

bigStyle = {"margin": "20px",
            "font-size": "24px",
            "border": "1px solid brown"
            }

app.layout = html.Div([
    html.Div(dcc.Input(id='inputWidget', type='text', style=bigStyle)),
    html.Button('Submit', id='submitButton', n_clicks=0, style=bigStyle),
    html.Div(id='textOutputDiv',
             children='Enter a value and press submit', style=bigStyle)
])


@callback(
    Output('textOutputDiv', 'children'),
    Input('submitButton', 'n_clicks'),
    State('inputWidget', 'value'),
    prevent_initial_call=True
    )
def update_output(n_clicks, value):
    return 'The input value was "{}" and the button has been clicked {} times'.format(
        value,
        n_clicks
    )


if __name__ == '__main__':
    app.run(debug=True)
    
