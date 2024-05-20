from dash import Dash, dcc, html, Input, Output, callback
import time

app = Dash(__name__)
inputStyle = {"font-size": "24px",
              "padding": "10px",
              "width": "300px",
              "margin": "50px"}

app.layout = html.Div(
    children=[
        html.H3("Edit text input to see loading state"),
        dcc.Input(id="loading-input-1",
                  value='Input triggers local spinner',
                  style=inputStyle),
        dcc.Loading(
            id="loading-1",
            type="default",
            children=html.Div(id="loading-output-1",
                              style={"border": "1px solid red",
                                     "height": "100px"})
            )
        ],
    style = {"font-size": "24px"}
    )

#------------------------------------------------------------
@callback(Output("loading-output-1", "children"),
          Input("loading-input-1", "value"),
          prevent_initial_call=True
          )
def input_triggers_spinner(value):
    time.sleep(3)
    return value
#------------------------------------------------------------
if __name__ == "__main__":
    port = 9017
    app.run(host='0.0.0.0', debug=True, port=port)


    
