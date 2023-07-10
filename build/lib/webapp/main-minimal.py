import base64
import datetime
import io
import os 
import slexil
from text import *


import flask
import dash
from dash.dependencies import Input, Output, State
from dash import dcc, html, dash_table

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
dashApp = dash.Dash(__name__, server = app, url_base_pathname = '/', 
                    external_stylesheets=external_stylesheets)

# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

@app.route('/PROJECTS/<path:urlpath>')
def openPreview(urlpath):
    print("--- urlpath: %s" % urlpath)
    fullPath = os.path.join("PROJECTS", urlpath)
    return flask.send_file(os.path.join(fullPath))
	


dashApp.layout = html.Div([
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
    html.Div(id='hidden-div', style={'display':'none'}),
    html.Div(id="runDiv",
             children=html.Div(
                [html.Button("Create HTML", id='runSlexilButton', className="submit"),
                html.A('open preview', id="previewLink", href='', target='_blank'),
                html.Button("Display",   id='displayHTMLButton',  n_clicks=0, className="btn"),
                html.Button("Download",  id="downloadHTMLButton", n_clicks=0, className="btn"),
                html.Div(id="runResults-display")])),
#    html.Div(id="afterActionButtonDiv",
#             children=html.Div([
#                html.Button("Display",   id='displayHTMLButton',  n_clicks=0),
#                html.Button("Download", id="downloadHTMLButton", n_clicks=0)
#                ]))
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
@dashApp.callback(Output('eafFilename-display', 'children'),
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
@dashApp.callback(Output('tierGuideFilename-display', 'children'),
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
@dashApp.callback(Output('grammaticalTermsFilename-display', 'children'),
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
@dashApp.callback(Output('runResults-display', 'children', allow_duplicate=True),
                  [Input('runSlexilButton', 'n_clicks')],
                  prevent_initial_call=True)
def runSlexil(n_clicks):
    if(not n_clicks == None):
       print("runSlexil: %d" % n_clicks)
       return(runSlexilDemo())

@dashApp.callback(Output('previewLink', 'href'),
                  [Input('displayHTMLButton', 'n_clicks')],
                  prevent_initial_call=True)
def displayHTML(href, n_clicks):
         print("displayHTML")
        
         return("http://localhost:8050/PROJECTS/fubar.html")
## see https://stackoverflow.com/questions/75725718/redirect-to-a-url-in-dash

@dashApp.callback(Output('previewLink', 'href'),
                  [Input('displayHTMLButton', 'n_clicks')],
                  prevent_initial_call=True)
def displayHTML(href, n_clicks):
         print("displayHTML")
        
         return("http://localhost:8050/PROJECTS/fubar.html")

@dashApp.callback(Output('hidden-div', 'children', allow_duplicate=True),
                  [Input('downloadHTMLButton', 'n_clicks')],
                  prevent_initial_call=True)
def downloadHTML(n_clicks):
		print("downloadHTML")

# html.Button("Display",   id='displayHTMLButton',  n_clicks=0, className="btn"),
# html.Button("Download",  id="downloadHTMLButton", n_clicks=0, className="btn"),




def runSlexilDemo():
    print("--- running slexil demo")
    projectDirectory = "PROJECTS"
    dataDir = "/Users/paul/github/slexil2/testData/inferno"
    elanXmlFilename = os.path.join(dataDir, "inferno-threeLines.eaf")
    tierGuideFile = os.path.join(dataDir, "tierGuide.yaml")
    grammaticalTermsFile = os.path.join(dataDir, "grammaticalTerms.txt")
    fontSizeControls = False
    startLine = None
    endLine = None
    kbFilename = None
    linguisticsFilename = None

    text = Text(elanXmlFilename,
                grammaticalTermsFile=grammaticalTermsFile,
                tierGuideFile=tierGuideFile,
                projectDirectory=projectDirectory,
                verbose=True,
                fontSizeControls = fontSizeControls,
                startLine = startLine,
                endLine = endLine,
                kbFilename = kbFilename,
                linguisticsFilename = linguisticsFilename)

    print(text.getTierSummary())
    htmlDoc = text.toHTML()
    webpageAt = "PROJECTS/fubar.html"
    absolutePath = os.path.abspath(webpageAt)
    print("webpageAt: %s" % webpageAt)
    with open(absolutePath, "w") as file:
        file.write(htmlDoc)
        file.close()

    return(webpageAt)

if __name__ == '__main__':
    dashApp.run_server(debug=True)

	
