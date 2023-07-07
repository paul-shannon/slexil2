import os 
import flask
import dash
from dash.dependencies import Input, Output, State
from dash import dcc, html, dash_table

import pandas as pd

app = flask.Flask(__name__)
dashApp = dash.Dash(__name__, server = app, url_base_pathname = '/')
dashApp.title = "fubar"

@app.route("/hello")
def hello():
	return "Hello, welcome to a simple route"

@app.route("/<filename>")
def junk(filename):
    return flask.send_file(filename)


@app.route('/PROJECTS/<path:urlpath>')
def displayNewPage(urlpath):
	print("route to displayNewPage")
	

dashApp.layout = html.Div([
    html.Div(id="runDiv",
             children=html.Div(
                [html.Button("Display Page", id='displayPageButton', className="submit"),
                 html.Br(),
                 html.Button("display page 2", id='displayPage2Button', className="submit"),
                 html.Div(id="scratchPad"),
                 html.Div(id="scratchPad2"),
                 html.A('open preview', id="previewLink", href='', target='_blank')
                ]
             ))])



@dashApp.callback(Output('scratchPad', 'children'),
                  [Input('displayPageButton', 'n_clicks')],
                  prevent_initial_call=True)
def displayPage(n_clicks):
    if(not n_clicks == None):
       print("displayPage: %d" % n_clicks)
       return dcc.Location(pathname="/hello", id="someid_doesnt_matter")
	
@dashApp.callback(Output('previewLink', 'href'),
                  [Input('displayPage2Button', 'n_clicks')],
                  prevent_initial_call=True)
def updatePreviewLink(n_clicks):
    print("updatePreviewLink")
    fullPath="junk.html"
    return (fullPath)

if __name__ == '__main__':
    dashApp.run_server(debug=True)

	   
