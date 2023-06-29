import flask
import dash
from dash import dcc, html
import flask

app = flask.Flask(__name__)
dash_app = dash.Dash(__name__, server = app, url_base_pathname = '/')

dash_app.layout = html.Div(
    [html.Div([html.H2("SLEXIL webapp (just a stub for now) in a Docker container",
					   style={"margin": "100px",
							  "text-align": "center"})])])

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=80)
