
'''
******************************************************************
SLEXIL—Software Linking Elan XML to Illuminated Language
Copyright (C) 2019 Paul Shannon and David Beck

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

The full version of the GNU General Public License is found at
<https://www.gnu.org/licenses/>.

Information about the software can be obtained by contacting
david.beck at ualberta.ca.
******************************************************************
'''

import datetime
import base64
import pdb
import xmlschema
import os
import scipy.io.wavfile as wavfile
import dash
import pandas as pd
import dash_table
import yaml
import io
import webbrowser
from flask import Flask
import flask
from textwrap import dedent
from zipfile import *
from shutil import copy
#----------------------------------------------------------------------------------------------------
import sys
#sys.path.append("../ijal_interlinear")
from audioExtractor import *
from text import *
#----------------------------------------------------------------------------------------------------
UPLOAD_DIRECTORY = "UPLOADS"
PROJECTS_DIRECTORY = "PROJECTS"
#----------------------------------------------------------------------------------------------------
# the webapp requires a PROJECTS_DIRECTORY in the current working directory.  this is
#
assert(os.path.exists(PROJECTS_DIRECTORY))

#----------------------------------------------------------------------------------------------------
from dash.dependencies import Input, Output, State
from dash import dcc
from dash import html


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)#, static_folder='PROJECTS')
app.config['suppress_callback_exceptions'] = True
app.title = "SLEXIL"

app.scripts.config.serve_locally = True

#------------------------------------------------------------------------------------------------------------------------
# this route handles the download of zipped up "demo input" zip file,
# in this case, infernoDemo.zip, which a new slexil user can run through the webapp to
# learn the ropes
# we may want to further qualify the route path to something like '/demos/<filename>'
# for better separation in the slexil webapp directory structure
#----------------------------------------------------------------------------------------------------
@app.server.route('/demos/<filename>')
def downloadZip(filename):
    path = os.path.join("demos", filename)
    return flask.send_file(path,
                           mimetype='application/zip',
                           as_attachment=True)

#----------------------------------------------------------------------------------------------------
# this route handles the download of zipped up assembled slexil projects
# which, by convention, are  ./PROJECTS/<someName>/webpage.zip:
#    PROJECTS/daylight/webpage.zip
#    PROJECTS/loco/webpage.zip
# we do not actually do the assembly here in this demo exploratory app. instead an appropriate
# file has been placed, ahead of time, in the appropriate directory.
#----------------------------------------------------------------------------------------------------
@app.server.route('/PROJECTS/<path:urlpath>')
def downloadProjectZipFile(urlpath):
#    if urlpath[-1] != 'p':
#       return()
#    if urlpath[-1] == 'p':
   print("--- serve_static_file")
   print("urlpath:  %s" % urlpath)
   fullPath = os.path.join("PROJECTS", urlpath)
   dirname = os.path.dirname(fullPath)
   filename = os.path.basename(fullPath)
   print("about to send %s, %s" % (dirname, filename))
   return flask.send_file(fullPath,
						  mimetype='application/zip',
						  as_attachment=True)

#----------------------------------------------------------------------------------------------------
def create_eafUploader():

    uploader = dcc.Upload(id='upload-eaf-file',
                          children=html.Div(html.A(id='upload-eaf-link',children='select file',className='fakebutton')),
                          multiple=False,disabled=1)

    return uploader

#----------------------------------------------------------------------------------------------------
def create_setTitleTab():

   setTitleInput = dcc.Input(id="setTitleTextInput",
                         placeholder='enter convenient, concise text title here, no spaces please!',
                         value="",
                         className="titleInput")

   setTitleButton = html.Button(id='setTitleButton', type='submit', children='Submit',className="button")

   children = [setTitleButton, setTitleInput]

   div = html.Div(children=children, id='setTitleDiv',className='selectionBox')

   return div

#----------------------------------------------------------------------------------------------------
def create_eafUploaderTab():

   textArea = dcc.Textarea(id="eafUploadTextArea",
                           placeholder='xml validation results go here',
                           value="",
                           className="uploadtextarea")

   children = [html.Div([create_eafUploader()]),
               textArea,html.Div(""),
               html.Div("This can take a minute or two for large texts.",className="timewarning")
               ]

   div = html.Div(children=children, id='eafUploaderDiv', className="selectionBox")

   return div

#----------------------------------------------------------------------------------------------------
def create_soundFileUploader():

    uploader = dcc.Upload(id='upload-sound-file',
                          children=html.Div(html.A(id='upload-sound-link',children='select file', className='fakebutton')),
                          multiple=False,disabled=1)

    return uploader

#----------------------------------------------------------------------------------------------------
def create_soundFileUploaderTab():

   textArea = dcc.Textarea(id="soundFileUploadTextArea",
                           placeholder='sound file validation results go here',
                           value="",
                           className="textarea")
   button =  html.Button('Get lines', id='extractSoundsByPhraseButton', className='button',disabled=1)
   
   textArea2 = dcc.Textarea(id="associateEAFAndSoundInfoTextArea",
                           placeholder='parse into lines based on .eaf',
                           value="",
                           className='textarea')   
                           
   children = [html.Div([create_soundFileUploader()]),
               textArea,
               button, 
               textArea2
               ]

   div = html.Div(children=children, id='soundFileUploaderDiv',className="selectionBox")

   return div

#----------------------------------------------------------------------------------------------------
def create_grammaticalTermsUploaderTab():

   textArea = dcc.Textarea(id="grammaticalTermsUploadTextArea",
                           placeholder='upload a text file listing abbreviations (optional)',
                           value="",
                           className="textarea")

   #button =  html.Button('No Grammatical Terms', id='noGrammaticalTermsButton', className="button")

   children = [html.Div([create_grammaticalTermsFileUploader()]),
               textArea
               ]

   div = html.Div(children=children, id='grammaticalTermsFileUploaderDiv',className="selectionBox")

   return div

#----------------------------------------------------------------------------------------------------
def create_grammaticalTermsFileUploader():

    uploader = dcc.Upload(id='upload-grammaticalTerms-file',
                          children=html.Div(html.A(id='upload-grammaticalTerms-link',children='select file', className='fakebutton')),
                          multiple=False,disabled=1)

    return uploader

#----------------------------------------------------------------------------------------------------
def create_webPageCreationTab():

   createAndDisplayButton =  html.Button('Show page', id='createAndDisplayWebPageButton',
                                         className="button",disabled=1)

   downloadLinkAndButton = html.A(id="downloadURL",
                                  children=[html.Button('Download',
                                                        id="downloadAssembledTextButton",
                                                        className='button',disabled=1)], 
                                  href='')

   createWebpageStatus = html.Span(id="createWebPageStatus", children="cwpita", style={'display': 'none'})

   webPageIframe = html.Iframe(id="storyIFrame", src="Story goes here.", className="webpageFrame")
   
   errorMessages = html.Span(id="createPageErrorMessages", children="", className="warningOff")

   buttonDiv = html.Div(children=[createAndDisplayButton, downloadLinkAndButton,errorMessages],
                        className="webFrameButtonBox")

   children = [buttonDiv,
               createWebpageStatus,
               html.Br(), 
               webPageIframe]

   div = html.Div(children=children, id='createWebPageDiv')

   return div

#----------------------------------------------------------------------------------------------------
def create_tierMapGui():

   dropDownMenus = html.Div("table will go here",id="tierMappingMenus")

   saveTierMappingChoicesButton = html.Button('Save Choices', id='saveTierMappingSelectionsButton',
                                       className="button")

   tierMappingChoicesResultDisplay = html.Span(id="tierMappingChoicesResultDisplay", children="",
                                               style={"border": 1, "margin-left": 10})
   div = html.Div(children=[dropDownMenus,
   							html.Br(),
   							saveTierMappingChoicesButton,
                            tierMappingChoicesResultDisplay],
                  			id='tierMapGui-div',className="tierDiv")

   return div

#----------------------------------------------------------------------------------------------------
def create_allDivs():

   children = [
       html.H4("", className="banner", id='pageTitleH4'),
       html.Div(create_introduction(), className="introduction"),
       html.Details([html.Summary('Set title',className="summary"), html.Div(create_setTitleTab())], className="allDivs",open="1"),
       html.Details([html.Summary('Upload .eaf file',className="summary"), html.Div(create_eafUploaderTab())], className="allDivs"),
       html.Details([html.Summary('Create tier guide',className="summary"), html.Div(create_tierMapGui())], className="allDivs"),
       html.Details([html.Summary('Upload audio file',className="summary"), html.Div(create_soundFileUploaderTab())], className="allDivs"),
       html.Details([html.Summary('Upload abbreviations',className="summary"), html.Div(create_grammaticalTermsUploaderTab())], className="allDivs"),
       html.Details([html.Summary('Create Web Page',className="summary"), html.Div(create_webPageCreationTab())], className="allDivs")]

   div = html.Div(children=children, id='main-div', className="mainDiv")

   return div

#----------------------------------------------------------------------------------------------------
def create_introduction():

   text = dcc.Markdown("**SLEXIL** is software for creating animated HTML files from texts prepared "
           "in [ELAN](https://tla.mpi.nl/tools/tla-tools/elan/). Users can use this site to upload the .eaf and .wav portions of "
           "ELAN projects and download an HTML file and accompanying CSS, JavaScript, "
           "and parsed audio files that can be embedded on a webpage or viewed in a "
           "browser on any computer. There is a video tutorial on YouTube and you can "
           "download a demo by clicking on the button to the right.")

   cell1 = html.Td(text,className='introduction')
   cell2 = html.Td(html.A(html.Button('Download Demo',className='button'),href='demos/infernoDemo.zip'),className="buttonCell")
   row = [html.Tr(children=[cell1,cell2])]

   div = html.Table(children=row, id='preamble')

   return div

#----------------------------------------------------------------------------------------------------

def createPulldownMenu(menuName, tierChoices):

   options = []
   for item in tierChoices:
       newElement={"label": item, "value": item}
       options.append(newElement)

   idName = "tierGuideMenu-%s" % menuName
   menu = dcc.Dropdown(options=options, clearable=True, id=idName, className="tierMenuPulldown")
   return(menu)

#----------------------------------------------------------------------------------------------------
def createTierMappingMenus(eafFilename):

   print("--- createTierMappingMenus: %s [exists: %s]" % (eafFilename, os.path.exists(eafFilename)))
   dropDownMenus = html.H5("failure in extracting tierIDs from %s" % eafFilename)

   if(os.path.exists(eafFilename)):
      tmpDoc = etree.parse(eafFilename)
      userProvidedTierNamesToAssignToStandardTiers = [tier.attrib["TIER_ID"] for tier in tmpDoc.findall("TIER")]
      print(userProvidedTierNamesToAssignToStandardTiers)

      tierChoices = userProvidedTierNamesToAssignToStandardTiers
      #tierChoices = ["pending EAF file selection"]

      dropDownMenus = html.Table(id="tierMappingMenus", children=[
         html.Tr([html.Th("Standard interlinear tiers",className="first"), html.Th("(e.g., from Totonac)",className="second"), html.Th("Select ELAN tier",className="third")]),
         html.Tr([html.Td(children=[
         		  					html.Div("line",style={'display':'inline-block'}),
         		  					html.Div("*",style={'display':'inline-block','color':'red'})]), 
         		  html.Td("tanhe:x’a'ha:ma:lhtzá'"), html.Td(createPulldownMenu("speech", tierChoices))]),
         html.Tr([html.Td("alternate transcription"), html.Td("taŋʔeːš’a̰ʔaːmaːɬtsá̰"), html.Td(createPulldownMenu("transcription2", tierChoices))]),
         html.Tr([html.Td("morphological analysis"), html.Td("taŋʔeː–š’a̰ʔáː–maːɬ=tsá̰"), html.Td(createPulldownMenu("morpheme", tierChoices))]),
         html.Tr([html.Td("morpheme glosses"), 
         		  html.Td(children=[
             						html.Div("basin–",style={'display':'inline-block'}),
             						html.Div("shine",style={'display':'inline-block'}),
             						html.Div("–prog",style={'font-variant':'small-caps','display':'inline-block'}),
             						html.Div("=now",style={'font-variant':'small-caps','display':'inline-block'})
             					  ]), 
             	  html.Td(createPulldownMenu("morphemeGloss", tierChoices))]),
         html.Tr([html.Td(children=[
         							html.Div("translation",style={'display':'inline-block'}),
         							html.Div("*",style={'display':'inline-block','color':'red'})]), 
         		  html.Td("‘The horizon is growing light.’"), html.Td(createPulldownMenu("translation", tierChoices))]),
         html.Tr([html.Td("second translation"), html.Td("‘Está aclarando donde sale el sol.’"), html.Td(createPulldownMenu("translation2", tierChoices))])
         ], className="tiermap"
         )

   saveTierMappingChoicesButton = html.Button('Save Choices', id='saveTierMappingSelectionsButton',
                                       className="button")

   tierMappingChoicesResultDisplay = html.Span(id="tierMappingChoicesResultDisplay", children="",
                                               style={"border": 1, "margin-left": 10})
   requiredTiersFootnote = html.Span("*Required",id='requiredTiersFootnote',className="warningfootnote")
   
   children =[dropDownMenus,
   			  html.Br(), 
   			  saveTierMappingChoicesButton, 
   			  tierMappingChoicesResultDisplay,
   			  requiredTiersFootnote]

   enclosingDiv = html.Div(children=children)
   #return dropDownMenus
   return(enclosingDiv)

#----------------------------------------------------------------------------------------------------
def parse_eaf_upload(contents, filename, date):

   print("filename selected: %s" % filename)
   #pdb.set_trace()
   content_type, content_string = contents.split(',')
   nchar = len(content_string)
   print("%s (%s): %d characters" % (filename, content_type, nchar))
   return(nchar)

#----------------------------------------------------------------------------------------------------
app.layout = html.Div(
    children=[
        create_allDivs(),
        html.P(id='projectTitle_hiddenStorage',              children="", style={'display': 'none'}),
        html.P(id='projectDirectory_hiddenStorage',          children="", style={'display': 'none'}),
        html.P(id='eaf_filename_hiddenStorage',              children="", style={'display': 'none'}),
        html.P(id='sound_filename_hiddenStorage',            children="", style={'display': 'none'}),
        html.P(id='audioPhraseDirectory_hiddenStorage',      children="", style={'display': 'none'}),
        html.P(id='grammaticalTerms_filename_hiddenStorage', children="", style={'display': 'none'}),
        html.P(id='tierGuide_filename_hiddenStorage',        children="", style={'display': 'none'}),
        html.P(id='speechTier_hiddenStorage',                children="", style={'display': 'none'}),
        html.P(id='transcription2Tier_hiddenStorage',        children="", style={'display': 'none'}),      
        html.P(id='morphemeTier_hiddenStorage',              children="", style={'display': 'none'}),
        html.P(id='morphemeGlossTier_hiddenStorage',         children="", style={'display': 'none'}),       
        html.P(id='translationTier_hiddenStorage',           children="", style={'display': 'none'}),
        html.P(id='translation2Tier_hiddenStorage',          children="", style={'display': 'none'}),
        html.P(id='temporaryTitle_hiddenStorage',            children="", style={'display': 'none'}),
        html.P(id='createPageErrorMessages_hiddenStorage',   children="", style={'display': 'none'}),
        html.P(id='audioStartandStopTimes_hiddenStorage',    children='', style={'display': 'none'})
        ],
    className="row",
    id='outerDiv'
    )

#----------------------------------------------------------------------------------------------------
@app.callback([Output('eafUploadTextArea', 'value'),
			  Output('eaf_filename_hiddenStorage', 'children')],
              [Input('upload-eaf-file', 'contents')],
              [State('upload-eaf-file', 'filename'),
               State('upload-eaf-file', 'last_modified'),
               State('projectDirectory_hiddenStorage', 'children')])
def on_eafUpload(contents, name, date, projectDirectory):
    if name is None:
        return("","")
    print("on_eafUpload, name: %s" % name)
    data = contents.encode("utf8").split(b";base64,")[1]
    filename = os.path.join(projectDirectory, name)
    if not filename[-4:] == '.eaf':
    	eaf_validationMessage = 'Please select an ELAN project (.eaf) file.'
    	return eaf_validationMessage, ''
    with open(filename, "wb") as fp:
         fp.write(base64.decodebytes(data))
         fileSize = os.path.getsize(filename)
         print("eaf file size: %d" % fileSize)
         schema = xmlschema.XMLSchema('http://www.mpi.nl/tools/elan/EAFv3.0.xsd')
         validXML = schema.is_valid(filename)
         eaf_validationMessage = "File %s (%d bytes) is valid XML." % (name, fileSize)
         if(not validXML):
            try:
               schema.validate(filename)
            except xmlschema.XMLSchemaValidationError as e:
               failureReason = e.reason
               eaf_validationMessage = "XML parsing error: %s [File: %s]" % (failureReason, filename)
         return eaf_validationMessage, filename

#----------------------------------------------------------------------------------------------------
@app.callback([Output('soundFileUploadTextArea', 'value'),
			   Output('sound_filename_hiddenStorage', 'children'),
			   Output('extractSoundsByPhraseButton','disabled')],
              [Input('upload-sound-file', 'contents')],
              [State('upload-sound-file', 'filename'),
               State('upload-sound-file', 'last_modified'),
               State('projectDirectory_hiddenStorage', 'children')])
def on_soundUpload(contents, name, date, projectDirectory):
    if name is None:
        return("","",1)
    print("=== on_soundUpload")
    data = contents.encode("utf8").split(b";base64,")[1]
    filename = os.path.join(projectDirectory, name)
    if not filename[-4:] == ".wav" and not filename[-4:] == ".WAV":
    	sound_validationMessage = "Please select a WAVE (.wav) file."
    	return sound_validationMessage, "", 1
    with open(filename, "wb") as fp:
       fp.write(base64.decodebytes(data))
       fileSize = os.path.getsize(filename)
       errorMessage = ""
       validSound = True
       try:
          rate, mtx = wavfile.read(filename)
       except ValueError as e:
          print("exeption in wavfile: %s" % e)
          rate = -1
          validSound = False
          errorMessage = str(e)
       print("sound file size: %d, rate: %d" % (fileSize, rate))
       if validSound:
       	  sound_validationMessage = "Sound file: %s (%d bytes)" % (name, fileSize)
       	  newButtonState = 0
       	  return sound_validationMessage, filename, newButtonState
       else:
       	  if "Unsupported bit depth: the wav file has 24-bit data" in errorMessage:
               sound_validationMessage = "File %s (%d byes) has 24-bit data, must be minimum 32-bit."  % (name, fileSize)
       	  else:
               sound_validationMessage = "ERROR: %s [File: %s (%d bytes)]" % (errorMessage, name, fileSize)
       	  newButtonState = 1
       	  return sound_validationMessage, filename, newButtonState

#----------------------------------------------------------------------------------------------------
@app.callback(Output('tierMapUploadTextArea', 'value'),
              [Input('upload-tierMap-file', 'contents')],
              [State('upload-tierMap-file', 'filename'),
               State('upload-tierMap-file', 'last_modified'),
               State('projectDirectory_hiddenStorage', 'children')])
def on_tierMapUpload(contents, name, date, projectDirectory):
    if name is None:
        return("")
    print("=== on_tierMapUpload")
    encodedString = contents.encode("utf8").split(b";base64,")[1]
    decodedString = base64.b64decode(encodedString)
    s = decodedString.decode('utf-8')
    yaml_list = yaml.load(s)
    filename = os.path.join(projectDirectory, name)
    with open(filename, "w") as fp:
       fp.write(s)
       fp.close()

    return("%s:\n %s" % (filename, s))

#----------------------------------------------------------------------------------------------------
@app.callback(Output('grammaticalTermsUploadTextArea', 'value'),
              [Input('upload-grammaticalTerms-file', 'contents')],
              [State('upload-grammaticalTerms-file', 'filename'),
               State('upload-grammaticalTerms-file', 'last_modified'),
               State('projectDirectory_hiddenStorage', 'children')])
def on_grammaticalTermsUpload(contents, name, date, projectDirectory):
	if name is None:
		return("")
	print("=== on_grammaticalTermsUpload")
	filename = os.path.join(projectDirectory, name)
	if filename[-4:] == '.eaf':
		return "Please select a text file, not the ELAN project file (.eaf)."
	encodedString = contents.encode("utf8").split(b";base64,")[1]
	decodedString = base64.b64decode(encodedString)
	try:
		s = decodedString.decode('utf-8')
	except UnicodeDecodeError:
		return "Please select a text (UTF-8) file.",1		
	s_NoTabs = s.replace("\t","")
	yaml_list = yaml.load(s_NoTabs)
	with open(filename, "w") as fp:
		fp.write(s)
		fp.close()
	return("Abbreviations file: %s" % (name))

#----------------------------------------------------------------------------------------------------
@app.callback(
    [Output('associateEAFAndSoundInfoTextArea', 'value'),
     Output('upload-grammaticalTerms-link','className'),
     Output('upload-grammaticalTerms-file','disabled'),
     Output('createAndDisplayWebPageButton','disabled')],
    [Input('extractSoundsByPhraseButton', 'n_clicks')],
    [State('sound_filename_hiddenStorage', 'children'),
     State('eaf_filename_hiddenStorage',   'children'),
     State('projectTitle_hiddenStorage',   'children'),
     State('projectDirectory_hiddenStorage', 'children')
    ])
def on_extractSoundPhrases(n_clicks, soundFileName, eafFileName, projectTitle, projectDirectory):
    if n_clicks is None:
        return("","fakebutton",1,1)
    print("=== on_extractSoundPhrases")
    print("n_clicks: %d" % n_clicks)
    if soundFileName is None:
        return("")
    if eafFileName is None:
        return("")
    soundFileName = soundFileName
    soundFile = os.path.basename(soundFileName)
    eafFileName = eafFileName
    eafFileFullPath = eafFileName # os.path.join(UPLOAD_DIRECTORY, eafFileName)
    soundFileFullPath = soundFileName # os.path.join(UPLOAD_DIRECTORY, soundFileName)
    print("soundFileName: %s" % soundFileName)
    print("eafFileName: %s" % eafFileName)
    phraseFileCount = extractPhrases(soundFileFullPath, eafFileFullPath, projectDirectory)
    print("after extractPhrases, enable next button in sequence (upload abbreviations)")
    newButtonState = 'fakebuttonEnabled'
    return("File %s parsed into %d phrases in audio directory." %(soundFile, phraseFileCount),newButtonState,0,0)

#----------------------------------------------------------------------------------------------------
@app.callback(
    Output('tierMapGui-div', 'children'),
    [Input("eaf_filename_hiddenStorage", 'children')],
    [State('tierMapGui-div', 'children')])
def createTierMappingMenusCallback(eafFilename,oldchildren):
    print("createTierMappingMenusCallback, eaf_filename_hiddenStorage trigger")
    if(eafFilename == ""):
       return("")
    print("=== extract tier ids from %s" % (eafFilename))
    #return(html.H4("infinite loop?"))
    print("the current children of tierMapGui are %s" %(oldchildren))
    return(createTierMappingMenus(eafFilename))

#----------------------------------------------------------------------------------------------------
@app.callback(
    Output('audioPhraseDirectory_hiddenStorage', 'children'),
    [Input('associateEAFAndSoundInfoTextArea', 'value')])
def update_output(value):
    print("=== callback triggered by associateEAFAndSoundTextArea change: %s" % value)
    phraseDirectory = value.split(":")[0]
    return(phraseDirectory)

#----------------------------------------------------------------------------------------------------
@app.callback(
    Output('grammaticalTerms_filename_hiddenStorage', 'children'),
    [Input('grammaticalTermsUploadTextArea', 'value')])
def update_output(value):
    print("=== callback triggered by grammaticalTermsUploadTextArea change: %s" % value)
    if value != "":
        grammaticalTermsPath = value.split(":")[1]
        grammaticalTermsFile = os.path.basename(grammaticalTermsPath).strip()
        return(grammaticalTermsFile)
    else:
        return ("")

#----------------------------------------------------------------------------------------------------
@app.callback(
    Output('tierGuide_filename_hiddenStorage', 'children'),
    [Input('tierMapUploadTextArea', 'value')])
def update_output(value):
    print("=== callback triggered by grammaticalTermsUploadTextArea change: %s" % value)
    tierGuideFile  = value.split(":")[0]
    return(tierGuideFile)

#----------------------------------------------------------------------------------------------------
@app.callback(
    [Output('createWebPageStatus', 'children'),
     Output('downloadAssembledTextButton','disabled'),
     Output('createPageErrorMessages_hiddenStorage','children')],
     #Output('storyIFrame','src')],
    [Input('createAndDisplayWebPageButton', 'n_clicks')],
    [State('sound_filename_hiddenStorage', 'children'),
     State('eaf_filename_hiddenStorage',   'children'),
     State('projectDirectory_hiddenStorage', 'children'),
     State('grammaticalTerms_filename_hiddenStorage', 'children'),
     State('projectTitle_hiddenStorage', 'children')])
def createWebPageCallback(n_clicks, soundFileName, eafFileName, projectDirectory,
                          grammaticalTermsFile,projectTitle):
    if n_clicks is None:
        return("",1,"","")
    print("=== create web page callback")
    print("        eaf: %s" % eafFileName)
    print(" audio phrases in: %s/audio" % projectDirectory)
    if(grammaticalTermsFile == ""):
        grammaticalTermsFile = None
    try:
        html = createWebPage(eafFileName, projectDirectory, grammaticalTermsFile,
                         os.path.join(projectDirectory, "tierGuide.yaml"),soundFileName)
    except TooManyMorphsError as e:
        print("EAF error: There are more morphs (%d) than glosses (%d) in line %s." %(e.morphs,e.glosses,e.lineNumber))
        errorMessage = "EAF error: There are more morphs (%d) than glosses (%d) in line %s." %(e.morphs,e.glosses,e.lineNumber)
        return("",1,errorMessage)
    except TooManyGlossesError as e:
        print("EAF error: There are more glosses (%d) than morphs (%d) in line %s." %(e.glosses,e.morphs,e.lineNumber))
        errorMessage = "EAF error: There are more glosses (%d) than morphs (%d) in line %s." %(e.glosses,e.morphs,e.lineNumber)
        return("",1,errorMessage)
    except EmptyTiersError as e:
        print("There are empty tiers or incomplete glosses after line %s" %e.lineNumber)
        errorMessage = "EAF error: There are empty tiers or incomplete glosses after line %s." %e.lineNumber
        return("",1,errorMessage)
    webpageAt = os.path.join(projectDirectory, "%s.html" %projectTitle)
    absolutePath = os.path.abspath(webpageAt)
    print(" webpage: %s" %webpageAt)
    file = open(absolutePath, "w")
    file.write(html)
    file.close()
    errorLog = os.path.abspath(os.path.join(projectDirectory, "ERRORS.log"))
    if os.path.isfile(errorLog):
        with open(errorLog) as elog:
        	logContents = elog.read()
        	if "WARNING" in logContents:
        		return("wrote file",0,"Wrote file. Check error log for formatting issues.")
    		
    createZipFile(projectDirectory,projectTitle)
    newButtonState = 0
    print("=== leaving web page callback")
    return("wrote file",newButtonState,"")#,webpageAt)

#----------------------------------------------------------------------------------------------------
@app.callback(
    Output('storyIFrame', 'src'),
    [Input('createWebPageStatus', 'children')],
    [State('projectDirectory_hiddenStorage', 'children'),
     State('projectTitle_hiddenStorage', 'children')])
def displayText(createWebPageStatus, projectDirectory, projectTitle):
   print("=== displayText '%s'" % createWebPageStatus)
   if createWebPageStatus is None:
      return("")
   if(len(createWebPageStatus) == 0):
      return("")
   pathToHTML = os.path.join(projectDirectory, "%s.html" %projectTitle)
   print("=== storyIFrame display %s" %pathToHTML)
   return(pathToHTML)

#----------------------------------------------------------------------------------------------------
@app.callback(
	[Output('createPageErrorMessages', 'children'),
	 Output('createPageErrorMessages', 'className')],
	[Input('createPageErrorMessages_hiddenStorage','children')]
	)
def setCreatePageErrorMessages(errorMessage):
	if len(errorMessage) == 0:
		className = 'warningOff'
	else:
		className = 'warningOn'
	return(errorMessage,className)
		
#----------------------------------------------------------------------------------------------------
@app.callback(
	Output('temporaryTitle_hiddenStorage', 'children'),
	[Input('setTitleTextInput', 'value')]
	)
def trackUserInputInSetTitle(typing):
	return(typing)	
	
#----------------------------------------------------------------------------------------------------
@app.callback(
    [Output('projectTitle_hiddenStorage', 'children'),
     Output('upload-eaf-link','className'),
     Output('upload-eaf-file','disabled')],
    [Input('setTitleButton', 'n_clicks'),
     Input('temporaryTitle_hiddenStorage', 'children')]
     #Input('setTitleTextInput', 'value')]
    )
def setTitle(n_clicks, newTitle):
	print("=== title callback")
	if n_clicks is None:
		print("n_clicks is None")
		return("","fakebutton",1)
	if len(newTitle) == 0:
		print("no title provided")
		return("","fakebutton",1)
	print("nClicks: %d, currentTitle: %s" % (n_clicks, newTitle))
	print("--- set project title")
	print("enable next button in sequence (upload .eaf file)")
	newButtonState = "fakebuttonEnabled"
	newTitle=newTitle.strip()
	return(newTitle,newButtonState,0)

#----------------------------------------------------------------------------------------------------
@app.callback(
    Output('projectDirectory_hiddenStorage', 'children'),
    [Input('projectTitle_hiddenStorage', 'children')]
    )
def update_output(projectTitle):
    if(len(projectTitle) == 0):
        return('')
    print("=== project title has been set, now create project directory: '%s'" % projectTitle)
    projectDirectory = os.path.join(PROJECTS_DIRECTORY, projectTitle)
    print("   creating projectDirectory if needed: %s" % projectDirectory)
    if(not os.path.exists(projectDirectory)):
        os.mkdir(projectDirectory)
    print("=== creating logger and setting destination for log file: %s" % projectDirectory)
    return(projectDirectory)

#----------------------------------------------------------------------------------------------------
@app.callback(
    Output('pageTitleH4', 'children'),
    [Input('projectDirectory_hiddenStorage', 'children')]
    )
def update_pageTitle(projectDirectory):
    if(len(projectDirectory) == 0):
        return('')
    print("=== projectDirectory_hiddenStorage has been set, now change project pageTitle: '%s'" % projectDirectory)
    #pdb.set_trace()
    newProjectTitle = projectDirectory.replace(PROJECTS_DIRECTORY, "")
    newProjectTitle = newProjectTitle.replace("/", "")
    print("IJAL Upload: %s" % newProjectTitle)
    return('')

#----------------------------------------------------------------------------------------------------
@app.callback(
    Output('speechTier_hiddenStorage', 'children'),
    [Input('tierGuideMenu-speech', 'value')])
def updateSpeechTier(value):
    if not value:
      value = ''    
    print("speech tier user name: %s" % value)
    return value

#----------------------------------------------------------------------------------------------------
@app.callback(
    Output('translationTier_hiddenStorage', 'children'),
    [Input('tierGuideMenu-translation', 'value')])
def updateTranslationTier(value):
    if not value:
      value = ''    
    print("translation tier user name: %s" % value)
    return value

#----------------------------------------------------------------------------------------------------
@app.callback(
    Output('morphemeTier_hiddenStorage', 'children'),
    [Input('tierGuideMenu-morpheme', 'value')])
def updateMorphemeTier(value):
    if not value:
      value = ''    
    print("morpheme tier user name: %s" % value)
    return value

#----------------------------------------------------------------------------------------------------
@app.callback(
    Output('morphemeGlossTier_hiddenStorage', 'children'),
    [Input('tierGuideMenu-morphemeGloss', 'value')])
def updateMorphemeGlossTier(value):
    if not value:
      value = ''    
    print("morphemeGloss tier user name: %s" % value)
    return value

#----------------------------------------------------------------------------------------------------
@app.callback(
    Output('translation2Tier_hiddenStorage', 'children'),
    [Input('tierGuideMenu-translation2', 'value')])
def updateTranslation2Tier(value):
    if not value:
      value = ''    
    print("translation2 tier user name: %s" % value)
    return value

#----------------------------------------------------------------------------------------------------
@app.callback(
    Output('transcription2Tier_hiddenStorage', 'children'),
    [Input('tierGuideMenu-transcription2', 'value')])
def updateTranscription2Tier(value):
    if not value:
      value = ''    
    print("transcription2 tier user name: %s" % value)
    return value

#----------------------------------------------------------------------------------------------------
@app.callback(
    [Output('tierMappingChoicesResultDisplay', 'children'),
     Output('upload-sound-link','className'),
     Output('upload-sound-file','disabled')],
    [Input('saveTierMappingSelectionsButton', 'n_clicks')],
    [State('speechTier_hiddenStorage',        'children'),
     State('transcription2Tier_hiddenStorage',   'children'),
     State('morphemeTier_hiddenStorage',      'children'),
     State('morphemeGlossTier_hiddenStorage', 'children'),
     State('translationTier_hiddenStorage',   'children'),
     State('translation2Tier_hiddenStorage',   'children'),
     State('projectDirectory_hiddenStorage',  'children')])
def saveTierMappingSelection(n_clicks, speechTier, transcription2Tier, morphemeTier, morphemeGlossTier, translationTier, translation2Tier, projectDirectory):
    if n_clicks is None:
        return("","fakebutton",1)
    print("saveTierMappingSelectionsButton: %d" % n_clicks)
    if len(speechTier) == 0:
        print("speechTier not mapped")
        return("You must specify a tier for the first line.","fakebutton",1)

    if len(translationTier) == 0:
        print("translationTier not mapped")
        return("You must specify a tier for the translation.","fakebutton",1)
        
    if len(morphemeTier) != 0 and len(morphemeGlossTier) == 0:
    	print("morpheme tier but no morphemeGlossTier")
    	return("You must specify the tier for the morpheme glosses.","fakebutton",1)
    	
    if len(morphemeTier) == 0 and len(morphemeGlossTier) != 0:
    	print("morpheme tier but no morphemeGlossTier")
    	return("You must specify the tier where the line is parsed.","fakebutton",1)

    print("time to write tierGuide.yaml")
    print("speechTier: %s" % speechTier)
    print("transcription2Tier: %s" % transcription2Tier)
    print("morphemeTier: %s" % morphemeTier)
    print("morphemeGlossTier: %s" % morphemeGlossTier)
    print("translationTier: %s" % translationTier)
    print("translation2Tier: %s" % translation2Tier)
    saveTierGuide(projectDirectory, speechTier, transcription2Tier, morphemeTier, morphemeGlossTier, translationTier, translation2Tier)
    print("enabling next button in sequence (Upload audio select file)")
    newButtonState = "fakebuttonEnabled"   
    return("Your selections have been saved.",newButtonState,0)

#----------------------------------------------------------------------------------------------------
@app.callback(Output('saveWebpageProgressTextArea', 'children'),
              [Input('confirmDownLoadObject', 'submit_n_clicks')],
              [State('projectTitle_hiddenStorage', 'children')])
def confirmDownload(submit_n_clicks, projectTitle):
    if not submit_n_clicks:
        return ''
    print("creating zip file")
    fullPath = createZipFile(projectTitle)
    return("saved web page: %s" % fullPath)

#----------------------------------------------------------------------------------------------------
# there can be multiple dash callbacks triggered by the same Input event.
# here we execute a second change to the webpage, returning the path to the project-specific
# webpage.zip, which is written into the href field of the html.A (or link) which nests the
# assembleTextButton
#----------------------------------------------------------------------------------------------------
@app.callback(Output('downloadURL', 'href'),
              [Input('projectDirectory_hiddenStorage', 'children')],
              [State('projectTitle_hiddenStorage', 'children')])
def updateDownloadTextButtonHref(directory,projectTitle):
   print("============= projectDirectory_hiddenStorage changed, updateDownloadTextButtonHref: %s" % directory)
   projectTitle += '.zip'
   print(projectTitle)
   pathToZip = os.path.join(directory,projectTitle)
   return(pathToZip)
   #return("%s/webpage.zip" % directory)


#----------------------------------------------------------------------------------------------------
def saveTierGuide(projectDirectory, speechTier, transcription2Tier, morphemeTier, morphemeGlossTier, translationTier, translation2Tier):

    dict = {"speech": speechTier,
            "transcription2": transcription2Tier,
            "morpheme": morphemeTier,
            "morphemeGloss": morphemeGlossTier,
            "translation": translationTier,
            "translation2": translation2Tier}
	
    filename =  os.path.join(projectDirectory, "tierGuide.yaml")

    with open(filename, 'w') as outfile:
        yaml.dump(dict, outfile, default_flow_style=False)

    print("saved tierMap to %s" % filename)

#----------------------------------------------------------------------------------------------------
def extractPhrases(soundFileFullPath, eafFileFullPath, projectDirectory):

    print("------- entering extractPhrases")
    print("soundFileFullPath: %s" % soundFileFullPath)
    print("projectDirectory: %s" % projectDirectory)
    audioDirectory = os.path.join(projectDirectory, "audio")

    if not os.path.exists(audioDirectory):
        os.makedirs(audioDirectory)
    copy(soundFileFullPath,audioDirectory)
    ea = AudioExtractor(soundFileFullPath, eafFileFullPath, audioDirectory)
    assert(ea.validInputs)
    ea.extract(quiet=True)
    phraseFileCount = len(os.listdir(audioDirectory))
    return(phraseFileCount)

#----------------------------------------------------------------------------------------------------
def createWebPage(eafFileName, projectDirectory, grammaticalTermsFileName, tierGuideFileName, soundFileName):

    print("-------- entering createWebPage")
    audioDirectoryRelativePath = "audio"
    print("eafFileName: %s" % eafFileName)
    print("projectDirectory: %s" % projectDirectory)
    print("audioDirectoryRelativePath: %s" % audioDirectoryRelativePath)
    print("grammaticalTermsFile: %s" % grammaticalTermsFileName)
    print("tierGuideFile: %s" % tierGuideFileName)
    if grammaticalTermsFileName != None:
    	grammaticalTermsFileName= os.path.join(projectDirectory,grammaticalTermsFileName)

    text = Text(eafFileName,
                soundFileName,
                grammaticalTermsFileName,
                tierGuideFileName,
                projectDirectory)
    print("-------- leaving createWebPage")
    return(text.toHTML())

#----------------------------------------------------------------------------------------------------
def createZipFile(projectDir,projectTitle):

   currentDirectoryOnEntry = os.getcwd()
   #projectDir = os.path.join(PROJECTS_DIRECTORY, projectName)
   os.chdir(projectDir)
   print(projectDir)

   audioDir = "audio"
   filesToSave = [os.path.join("audio", f) for f in os.listdir(audioDir) if f.endswith('.wav')]
   filesToSave.insert(0, "%s.html" %projectTitle)
   
   #zipfile is named for project
   zipFilename = "%s.zip" %projectTitle
   zipFilenameFullPath = os.path.join(currentDirectoryOnEntry, projectDir, zipFilename)
   zipHandle = ZipFile(zipFilename, 'w')

   #filesToSave includes ijal.css, ijalUtils.js
   CSSfile = os.path.join(currentDirectoryOnEntry,"ijal.css")
   scriptFile = os.path.join(currentDirectoryOnEntry,"ijalUtils.js")
   jqueryFile = os.path.join(currentDirectoryOnEntry,"jquery-3.3.1.min.js")
#    iconFile = os.path.join(currentDirectoryOnEntry,"speaker.png")
   copy(CSSfile, os.getcwd())
   copy(scriptFile, os.getcwd())
   copy(jqueryFile, os.getcwd())
#    copy(iconFile, os.getcwd())
   filesToSave.append("ijal.css")
   filesToSave.append("ijalUtils.js")
   filesToSave.append("jquery-3.3.1.min.js")
#    filesToSave.append("speaker.png")
   if os.path.isfile("ERRORS.log"):
      print("===  adding errors log to .zip file")
      errorLog = ("ERRORS.log")
      #copy(errorLog, os.getcwd())
      filesToSave.append("ERRORS.log")

   for file in filesToSave:
      zipHandle.write(file)

   zipHandle.close()

   os.chdir(currentDirectoryOnEntry)
   return(zipFilenameFullPath)

#----------------------------------------------------------------------------------------------------
server = app.server

if __name__ == "__main__":
   
   app.run_server(host='0.0.0.0', port=60041)
