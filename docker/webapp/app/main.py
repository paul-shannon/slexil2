import base64
import datetime
import io

import slexil
from text import *
import flask
import dash
from dash.dependencies import Input, Output, State
from dash import dcc, html, dash_table
import webbrowser 
import pandas as pd

uploaderStyle = {'width': '60%',
                 'height': '60px',
                 'lineHeight': '60px',
                 'borderWidth': '1px',
                 'borderStyle': 'solid',
                 'borderRadius': '5px',
                 'textAlign': 'center',
                 'font-size': "24px",
                 'margin': '10px',
                 'margin-left': '100px'
                 }

simpleTextDisplayStyle = {"font-size": "32px",
                          "margin-left": "200px"
                          }
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = flask.Flask(__name__)
dash_app = dash.Dash(__name__, server = app, url_base_pathname = '/')

dash_app.layout = html.Div([
    dcc.Upload(
        id='eafFilename-select',
        children=html.Div([
            'EAF: Drag and Drop or ',
            html.A('Select File')
            ]),
        style=uploaderStyle
        ),
    html.Div(id='eafFilename-display',
             style=simpleTextDisplayStyle),
    dcc.Upload(
        id='tierGuideFilename-select',
        children=html.Div([
            'tierGuide.yaml: Drag and Drop or ',
            html.A('Select File')
            ]),
        style=uploaderStyle
        ),
    html.Div(id='tierGuideFilename-display',
             style=simpleTextDisplayStyle),
    dcc.Upload(
        id='grammaticalTermsFilename-select',
        children=html.Div([
            'grammaticalTerms.yaml: Drag and Drop or ',
            html.A('Select File')
            ]),
        style=uploaderStyle
        ),
    html.Div(id='grammaticalTermsFilename-display',
             style=simpleTextDisplayStyle),
    html.Button('Run', id='run-slexil-button', n_clicks=0,
                style={"font-size": "32px",
                       "margin": "20px",
                       "margin-left": "300px"}),
    html.Button('Download HTML file', id='download-htmlFile-button', n_clicks=0,
                style={"font-size": "32px",
                       "margin": "20px",
                       "margin-left": "300px"}),
    dcc.Download(id="downloadHTML"),
    html.Div(id='slexilExecutionTrace-display',
             style=simpleTextDisplayStyle)

])

def parseEAF(filename):
	print("--- from parseEAF, filename = %s" % filename)
	return(filename)

def parseTierGuide(filename):
	print("--- from parseTierGuide, filename = %s" % filename)
	return(filename)

def parseGrammaticalTerms(filename):
	print("--- from parseGrammaticalTerms, filename = %s" % filename)
	return(filename)

def eafToHTML():
    slexilText = Text("inferno-threeLines.eaf", "grammaticalTerms.txt",
                      "tierGuide.yaml", "./", True, False, None, None, None, None)
    htmlText = slexilText.toHTML()
    filename = "inferno.html"
    f = open(filename, "w")
    f.write(htmlText)
    f.close()
    #webbrowser.open_new_tab("https://google.com")
    #return "tried to display inferno.html"

    #return(htmlText)

#--------------------------------------------------------------------------------
@dash_app.callback(Output('eafFilename-display', 'children'),
              Input('eafFilename-select', 'contents'),
              State('eafFilename-select', 'filename'),
              State('eafFilename-select', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if(list_of_contents is not None):
       print("update_output")
       print("names: %s" % list_of_names)
       children = [parseEAF(list_of_names)]
       return children
#--------------------------------------------------------------------------------
@dash_app.callback(Output('tierGuideFilename-display', 'children'),
              Input('tierGuideFilename-select', 'contents'),
              State('tierGuideFilename-select', 'filename'),
              State('tierGuideFilename-select', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if(list_of_contents is not None):
       print("update_output")
       print("names: %s" % list_of_names)
       tierGuideText = base64.b64decode(list_of_contents)
       print(grammaticalTermsText)
       children = [parseTierGuide(list_of_names)]
       return children
#--------------------------------------------------------------------------------
@dash_app.callback(Output('grammaticalTermsFilename-display', 'children'),
              Input('grammaticalTermsFilename-select', 'contents'),
              State('grammaticalTermsFilename-select', 'filename'),
              State('grammaticalTermsFilename-select', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if(list_of_contents is not None):
       print("update_output")
       print("names: %s" % list_of_names)
       grammaticalTermsText = base64.b64decode(list_of_contents).decode("utf-8")
       print(grammaticalTermsText)
       children = [parseGrammaticalTerms(list_of_names)]
       return children
#--------------------------------------------------------------------------------
@dash_app.callback(Output('slexilExecutionTrace-display', 'children'),
				   Input('run-slexil-button', 'n_clicks'),
                   prevent_initial_call=True)
def display_status(button):
      print("display_status callback")
      children = [eafToHTML()]
      return children
	
#--------------------------------------------------------------------------------
@dash_app.callback(
    Output("downloadHTML", "data"),
    Input("download-htmlFile-button", "n_clicks"),
    prevent_initial_call=True)
def downloadFile(n_clicks):
    filename = "inferno.html"
    f = open(filename, "r+")
    htmlText = f.read()
    print("--- about to download %s with %d characters" % (filename, len(htmlText)))
    return dict(content=htmlText, filename=filename)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8008)

	
