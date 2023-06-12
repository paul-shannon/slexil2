import base64
import datetime
import io

import dash
from dash.dependencies import Input, Output, State
from dash import dcc, html, dash_table

import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Upload(
        id='eafFilename-select',
        children=html.Div([
            'EAF: Drag and Drop or ',
            html.A('Select File')
            ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'solid',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
            }
        ),
    html.Div(id='eafFilename-display'),
    dcc.Upload(
        id='tierGuideFilename-select',
        children=html.Div([
            'tierGuide.yaml: Drag and Drop or ',
            html.A('Select File')
            ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'solid',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
            }
        ),
    html.Div(id='tierGuideFilename-display'),
    dcc.Upload(
        id='grammaticalTermsFilename-select',
        children=html.Div([
            'grammaticalTerms.yaml: Drag and Drop or ',
            html.A('Select File')
            ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'solid',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
            }
        ),
    html.Div(id='grammaticalTermsFilename-display'),
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

#--------------------------------------------------------------------------------
@app.callback(Output('eafFilename-display', 'children'),
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
@app.callback(Output('tierGuideFilename-display', 'children'),
              Input('tierGuideFilename-select', 'contents'),
              State('tierGuideFilename-select', 'filename'),
              State('tierGuideFilename-select', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if(list_of_contents is not None):
       print("update_output")
       print("names: %s" % list_of_names)
       children = [parseTierGuide(list_of_names)]
       return children
#--------------------------------------------------------------------------------
@app.callback(Output('grammaticalTermsFilename-display', 'children'),
              Input('grammaticalTermsFilename-select', 'contents'),
              State('grammaticalTermsFilename-select', 'filename'),
              State('grammaticalTermsFilename-select', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if(list_of_contents is not None):
       print("update_output")
       print("names: %s" % list_of_names)
       children = [parseGrammaticalTerms(list_of_names)]
       return children
#--------------------------------------------------------------------------------

if __name__ == '__main__':
    app.run_server(debug=True)

	
