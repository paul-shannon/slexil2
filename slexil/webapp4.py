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

import base64
from zipfile import ZipFile
import time
import soundfile as soundfile
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import flask
import xmlschema
from xml.etree import ElementTree as etree
import pdb
from dash.dependencies import Input, Output, State
from shutil import copy
from text import *
from aboutTexts import AboutTexts

# ----------------------------------------------------------------------------------------------------
UPLOAD_DIRECTORY = "UPLOADS"
PROJECTS_DIRECTORY = "PROJECTS"
HTMLFILE = ""
# ----------------------------------------------------------------------------------------------------
# the webapp requires a PROJECTS_DIRECTORY in the current working directory
#
try:
    assert (os.path.exists(PROJECTS_DIRECTORY))
except AssertionError:
    os.mkdir(PROJECTS_DIRECTORY)

# ----------------------------------------------------------------------------------------------------

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', dbc.themes.BOOTSTRAP]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config['suppress_callback_exceptions'] = True
app.title = "SLEXIL"

app.scripts.config.serve_locally = True
server = app.server


# ------------------------------------------------------------------------------------------------------------------------
# this route handles the download of zipped up "demo input" zip file,
# in this case, infernoDemo.zip, which a new slexil user can run through the webapp to
# learn the ropes
# we may want to further qualify the route path to something like '/demos/<filename>'
# for better separation in the slexil webapp directory structure
# ----------------------------------------------------------------------------------------------------
@app.server.route('/demos/<filename>')
def downloadZip(filename):
    print("==== download zip: %s" % filename)
    path = os.path.join("demos", filename)
    return flask.send_file(path,
                           mimetype='application/zip',
                           as_attachment=True)


# ----------------------------------------------------------------------------------------------------
@app.server.route('/PROJECTS/<path:urlpath>')
def downloadProjectZipFile(urlpath):
    print("=== entering download ZIP file app.server.route")
    fullPath = os.path.join("PROJECTS", urlpath)
    dirname = os.path.dirname(fullPath)
    filename = os.path.basename(fullPath)
    if urlpath[-4:] == "html" or urlpath[-3:] == "css":
        print("=== populate textArea from %s" % urlpath)
        return flask.send_file(os.path.join(fullPath))
    elif urlpath[-3:] == "wav":
        print("=== call wav file from %s" % urlpath)
        return flask.send_file(os.path.join(fullPath))
    elif urlpath[-3:] == "ogg":
        print("=== call ogg file from %s" % urlpath)
        return flask.send_file(os.path.join(fullPath))
    elif urlpath[-2:] == "js":
        print("=== call javascript file from %s" % urlpath)
        return flask.send_file(os.path.join(fullPath))
    if urlpath[-3:] == 'zip':
        print("=== serve_static_file")
        print("urlpath:  %s" % urlpath)
        print("about to send %s, %s" % (dirname, filename))
        return flask.send_file(fullPath,
                               mimetype='application/zip',
                               as_attachment=True)


# ----------------------------------------------------------------------------------------------------
def create_setTitleTab():
    setTitleInput = dcc.Input(id="setTitleTextInput",
                              placeholder='enter convenient, concise text title here, no spaces please!',
                              value="",
                              className="titleInput")
    setTitleButton = html.Button(type="submit", id='setTitleButton', children="submit", className="button")

    children = [setTitleButton, setTitleInput]

    div = html.Div(children=children, id='setTitleDiv', className='selectionBox')

    return div


# ----------------------------------------------------------------------------------------------------
def create_eafUploader():
    hyperLink = html.A(id='upload-eaf-link', children='select file')
    uploader = dcc.Upload(children=['Drag and drop or ', hyperLink], id='upload-eaf-file', multiple=False, disabled=1)

    return uploader


# ----------------------------------------------------------------------------------------------------
def create_eafUploaderTab():
    children = [html.Div("Add .eaf file", className="stepTitle"),
                html.Div([create_eafUploader()], className="dragDropArea"),
                # html.Div("*Required",className="requiredLabel"),
                dcc.Loading("This can take a minute or two for large texts.", id="eafuploadStatus",
                            className="timewarning")
                ]

    div = html.Div(children=children, id='eafUploaderDiv', className="selectionBox")

    return div


# ----------------------------------------------------------------------------------------------------
def create_soundFileUploader():
    hyperLink = html.A(id='upload-sound-link', children='select file')
    uploader = dcc.Upload(id='upload-sound-file', children=['Drag and drop or ', hyperLink], multiple=False, disabled=1)

    return uploader


# ----------------------------------------------------------------------------------------------------
def create_soundFileUploaderTab():
    children = [html.Div("Add sound file", className="stepTitle"),
                html.Div([create_soundFileUploader()], className="dragDropArea"),
                dcc.Loading(children="This can take a minute or two for large files.", id="soundUploadStatus",
                            className="timewarning")
                ]

    div = html.Div(children=children, id='soundFileUploaderDiv', className="selectionBox")

    return div


# ----------------------------------------------------------------------------------------------------
def create_grammaticalTermsUploaderTab():
    children = [html.Div("Add abbreviations", className="stepTitle"),
                html.Div([create_grammaticalTermsFileUploader()], className="dragDropArea"),
                html.Div(id='grammaticalTermsUploadStatus', className="information")
                ]

    div = html.Div(children=children, id='grammaticalTermsFileUploaderDiv', className="selectionBox")

    return div


# ----------------------------------------------------------------------------------------------------
def create_grammaticalTermsFileUploader():
    hyperLink = html.A(id='upload-grammaticalTerms-link', children='select file')
    uploader = dcc.Upload(id='upload-grammaticalTerms-file', children=['Drag and drop or ', hyperLink], multiple=False,
                          disabled=1)

    return uploader


# ----------------------------------------------------------------------------------------------------
def create_webPageCreationTab():
    createAndDisplayButton = html.Button('Make page', id='createAndDisplayWebPageButton',
                                         className="button", disabled=1)

    downloadLinkAndButton = html.A(id="downloadURL",
                                   children=[html.Button('Download',
                                                         id="downloadAssembledTextButton",
                                                         className='button', disabled=1)],
                                   href='')

    previewLink = html.A('open preview', id="previewLink", href='', target='_blank')
    createWebpageStatus = html.Div(id="createWebPageStatus", children=[previewLink, "  in a new tab"],
                                   className="previewoff")

    errorMessages = html.Span(id="createPageErrorMessages", children="", className="warningOff")

    children = [html.Hr(className="divider"),
                html.Div(children=[createAndDisplayButton, downloadLinkAndButton, createWebpageStatus, errorMessages],
                         className="webFrameButtonBox"),
                html.Div("This can take a minute or two for large texts.", id="webPageCreationStatus",
                         className="progresstimewarning")]

    div = html.Div(children=children, id='createWebPageDiv')

    return div


# ----------------------------------------------------------------------------------------------------
def create_tierMapGui():
    dropDownMenus = html.Div("table will go here", id="tierMappingMenus")

    saveTierMappingChoicesButton = html.Button('save', id='saveTierMappingSelectionsButton',
                                               className="button")

    tierMappingChoicesResultDisplay = html.Span(id="tierMappingChoicesResultDisplay", children="",
                                                style={"border": 1, "margin-left": 10})
    div = html.Div(children=[dropDownMenus,
                             html.Br(),
                             saveTierMappingChoicesButton,
                             tierMappingChoicesResultDisplay],
                   id='tierMapGui-div', className="tierDiv")

    return div


# ----------------------------------------------------------------------------------------------------
def create_componentsUploaderTab():
    children = [create_eafUploaderTab(),
                create_soundFileUploaderTab(),
                create_grammaticalTermsUploaderTab()
                ]
    div = html.Div(children=children, id='uploadComponents-div', className='tierDiv')

    return div


# ----------------------------------------------------------------------------------------------------
def create_webpageBuilderTab():
    children = [create_tierMapGui(),
                create_webPageCreationTab()
                ]
    div = html.Div(children=children, id='buildPage-div', className='tierDiv')

    return div


# ----------------------------------------------------------------------------------------------------
def createAppTab():
    intro = create_introduction()

    children = [intro,
                html.Details([html.Summary('Set title', className="summary"), html.Div(create_setTitleTab())],
                             className="allDivs", open="1"),
                html.Details(
                    [html.Summary('Upload components', className="summary"), html.Div(create_componentsUploaderTab())],
                    className="allDivs"),
                html.Details(
                    [html.Summary('Create webpage', className="summary"), html.Div(create_webpageBuilderTab())],
                    className="allDivs"),
                ]
    div = html.Div(id="webapp", className="null", children=children)
    return div


# ----------------------------------------------------------------------------------------------------
def createAboutTab():
    aboutTab = AboutTexts()
    innerdiv = aboutTab.getMainDiv()
    return innerdiv


# ----------------------------------------------------------------------------------------------------
def create_allDivs():
    children = [
        html.H4("", className="banner", id='pageTitleH4'),
        dcc.Tabs(
            id="tabs",
            value='appTab',
            className='tabbar',
            children=[
                dcc.Tab(
                    label='SLEXIL',
                    value='appTab',
                    className="tabbutton",
                    selected_className="tabselected"),
                dcc.Tab(
                    label='About SLEXIL',
                    value='aboutTab',
                    className="tabbutton",
                    selected_className="tabbutton",
                    id="aboutTab")
            ]),
        html.Div(id='tab_contents')
    ]

    div = html.Div(children=children, id='main-div', className="mainDiv")

    return div


# ----------------------------------------------------------------------------------------------------
def create_introduction():
    text = dcc.Markdown('''**SLEXIL** is software for creating animated HTML files from texts prepared 
                        in [ELAN](https://tla.mpi.nl/tools/tla-tools/elan/). Users can access this site to upload the 
                        .eaf and .wav portions of ELAN projects and download an HTML file and accompanying CSS, JavaScript, 
                        and parsed audio files that can be embedded on a webpage or viewed in a browser on any computer. 
                        You can find a [video tutorial] (https://youtu.be/7b99pkhQibs) on using SLEXIL on YouTube 
                        or download a demo project to practice with by clicking on the **Download Demo** button.''')

    button = html.Button('DOWNLOAD DEMO', className='demoButton')
    contents = [html.A(button, href='demos/infernoDemo.zip', className="buttonCell"),
                html.Div(id="intro", children=[text], className="introText")]
    div = html.Div(children=contents, className='introduction', id='preamble')

    return div


# ----------------------------------------------------------------------------------------------------

def createPulldownMenu(menuName, tierChoices):
    options = []
    for item in tierChoices:
        newElement = {"label": item, "value": item}
        options.append(newElement)

    idName = "tierGuideMenu-%s" % menuName
    menu = dcc.Dropdown(options=options, clearable=True, id=idName, className="tierMenuPulldown")
    return (menu)


# ----------------------------------------------------------------------------------------------------
def createTierMappingMenus(eafFilename):
    print("=== createTierMappingMenus: %s [exists: %s]" % (eafFilename, os.path.exists(eafFilename)))
    dropDownMenus = html.H5("☠️ failure in extracting tierIDs from %s" % eafFilename)

    if (os.path.exists(eafFilename)):
        tmpDoc = etree.parse(eafFilename)
        userProvidedTierNamesToAssignToStandardTiers = [tier.attrib["TIER_ID"] for tier in tmpDoc.findall("TIER")]
        print(userProvidedTierNamesToAssignToStandardTiers)

        tierChoices = userProvidedTierNamesToAssignToStandardTiers

        dropDownMenus = html.Table(id="tierMappingMenus", children=[
            html.Tr([html.Th("Standard interlinear tiers", className="first"),
                     html.Th("(e.g., from Totonac)", className="second"),
                     html.Th("Select ELAN tier", className="third")]),
            html.Tr([html.Td(children=[
                html.Div("line", style={'display': 'inline-block'}),
                html.Div("*", style={'display': 'inline-block', 'color': 'red'})]),
                html.Td("tanhe:x’a'ha:ma:lhtzá'"), html.Td(createPulldownMenu("speech", tierChoices))]),
            html.Tr([html.Td("alternate transcription"), html.Td("taŋʔeːš’a̰ʔaːmaːɬtsá̰"),
                     html.Td(createPulldownMenu("transcription2", tierChoices))]),
            html.Tr([html.Td("morphological analysis"), html.Td("taŋʔeː–š’a̰ʔáː–maːɬ=tsá̰"),
                     html.Td(createPulldownMenu("morpheme", tierChoices))]),
            html.Tr([html.Td("morphemic glosses"),
                     html.Td(children=[
                         html.Div("basin–", style={'display': 'inline-block'}),
                         html.Div("shine", style={'display': 'inline-block'}),
                         html.Div("–prog", style={'font-variant': 'small-caps', 'display': 'inline-block'}),
                         html.Div("=now", style={'font-variant': 'small-caps', 'display': 'inline-block'})
                     ]),
                     html.Td(createPulldownMenu("morphemeGloss", tierChoices))]),
            html.Tr([html.Td(children=[
                html.Div("translation", style={'display': 'inline-block'}),
                html.Div("*", style={'display': 'inline-block', 'color': 'red'})]),
                html.Td("‘The horizon is growing light.’"), html.Td(createPulldownMenu("translation", tierChoices))]),
            html.Tr([html.Td("second translation"), html.Td("‘Está aclarando donde sale el sol.’"),
                     html.Td(createPulldownMenu("translation2", tierChoices))])
        ], className="tiermap"
                                   )

    saveTierMappingChoicesButton = html.Button('save', id='saveTierMappingSelectionsButton',
                                               className="button")

    tierMappingChoicesResultDisplay = html.Span(id="tierMappingChoicesResultDisplay", children="",
                                                style={"border": 1, "margin-left": 10, "font-size": "12pt"})
    requiredTiersFootnote = html.Span("*Required", id='requiredTiersFootnote', className="warningfootnote")

    children = [dropDownMenus,
                html.Br(),
                saveTierMappingChoicesButton,
                tierMappingChoicesResultDisplay,
                requiredTiersFootnote]

    enclosingDiv = html.Div(children=children)
    return (enclosingDiv)


# ----------------------------------------------------------------------------------------------------
progressBar = dbc.Progress("Working ...", id='progress', value=0, striped=True, animated=True, style={'display': 'inline'})
app.layout = html.Div(
    children=[
        create_allDivs(),
        html.P(id='projectTitle_hiddenStorage', children="", style={'display': 'none'}),
        html.P(id='projectDirectory_hiddenStorage', children="", style={'display': 'none'}),
        html.P(id='eaf_filename_hiddenStorage', children="", style={'display': 'none'}),
        html.P(id='sound_filename_hiddenStorage', children="", style={'display': 'none'}),
        html.P(id='audioPhraseDirectory_hiddenStorage', children="", style={'display': 'none'}),
        html.P(id='grammaticalTerms_filename_hiddenStorage', children="", style={'display': 'none'}),
        html.P(id='tierGuide_filename_hiddenStorage', children="", style={'display': 'none'}),
        html.P(id='speechTier_hiddenStorage', children="", style={'display': 'none'}),
        html.P(id='transcription2Tier_hiddenStorage', children="", style={'display': 'none'}),
        html.P(id='morphemeTier_hiddenStorage', children="", style={'display': 'none'}),
        html.P(id='morphemeGlossTier_hiddenStorage', children="", style={'display': 'none'}),
        html.P(id='translationTier_hiddenStorage', children="", style={'display': 'none'}),
        html.P(id='translation2Tier_hiddenStorage', children="", style={'display': 'none'}),
        html.P(id='createPageErrorMessages_hiddenStorage', children="", style={'display': 'none'}),
        html.P(id='progressBarStatus_hiddenStorage', children="", style={'display': 'none'}),
        html.P(id='progressBar_hiddenStorage', children=[progressBar], style={'display': 'none'})
    ],
    className="row",
    id='outerDiv'
)


# ----------------------------------------------------------------------------------------------------
@app.callback(Output('tab_contents', 'children'),
              [Input('tabs', 'value')])
def fillTab(tab):
    print("==== filling in tab")
    if tab == 'appTab':
        child = createAppTab()
    elif tab == 'aboutTab':
        child = createAboutTab()
    return child


# ----------------------------------------------------------------------------------------------------
@app.callback([Output('eafuploadStatus', 'children'),
               Output('eafuploadStatus', 'className'),
               Output('eaf_filename_hiddenStorage', 'children'),
               Output('upload-sound-file', 'disabled')],
              [Input('upload-eaf-file', 'contents')],
              [State('upload-eaf-file', 'filename'),
               State('projectDirectory_hiddenStorage', 'children')])
def on_eafUpload(contents, name, projectDirectory):
    if name is None:
        return ("This can take a minute or two for large texts.", "timewarning", "", 1)
    print("on_eafUpload, name: %s" % name)
    # print("len(contents) = %d" %len(contents))
    # data = contents.encode("utf8")
    # print("data is ", data)#.split(b";base64,")[1]
    data = contents.encode("utf8").split(b";base64,")[1]
    # print("len(data) = %d" %len(data))
    filename = os.path.join(projectDirectory, name)
    if not filename[-4:] == '.eaf':
        eaf_validationMessage = '☠️ Please select a valid ELAN project (.eaf) file.'
        return eaf_validationMessage, "timewarning", '', 1
    with open(filename, "wb") as fp:
        fp.write(base64.decodebytes(data))
    print("Filename: %s" %filename)
    assert(os.path.isfile(filename))
    fileSize = os.path.getsize(filename)
    print("eaf file size: %d" % fileSize)
    schema = xmlschema.XMLSchema('http://www.mpi.nl/tools/elan/EAFv3.0.xsd')
    try:
        validXML = schema.is_valid(filename)
    except etree.ParseError as e:
        import xml.parsers.expat
        error = xml.parsers.expat.errors.messages[e.code]
        eaf_validationMessage = "☠️ XML parsing error: %s [File: %s]" % (error, name)
        return eaf_validationMessage, "timewarning", '', 1
    eaf_validationMessage = "👍︎ File %s (%d bytes) is valid." % (name, fileSize)
    if (not validXML):
        try:
            schema.validate(filename)
        except xmlschema.XMLSchemaValidationError as e:
            failureReason = e.reason
            eaf_validationMessage = "☠️ XML parsing error: %s [File: %s]" % (failureReason, name)
            return eaf_validationMessage, "timewarning", '', 1
        # eaf_validationMessage = "👍︎ File %s (%d bytes) is valid." % (name, fileSize)
    print("=== enabling next sequence (Upload audio)")
    return eaf_validationMessage, "information", filename, 0


# ----------------------------------------------------------------------------------------------------
@app.callback([Output('soundUploadStatus', 'children'),
               Output('soundUploadStatus', 'className'),
               Output('sound_filename_hiddenStorage', 'children')],
              [Input('upload-sound-file', 'contents')],
              [State('upload-sound-file', 'filename'),
               State('projectDirectory_hiddenStorage', 'children')])
def on_soundUpload(contents, name, projectDirectory):
    if name is None:
        return "This can take a minute or two for large files.", "timewarning", ""
    print("=== on_soundUpload")
    data = contents.encode("utf8").split(b";base64,")[1]
    filename = os.path.join(projectDirectory, name)
    print("=== opening file")
    with open(filename, "wb") as fp:
        fp.write(base64.decodebytes(data))
    fileSize = os.path.getsize(filename)
    errorMessage = ""
    validSound = True
    try:
        mtx, rate = soundfile.read(filename)
    except (ValueError, RuntimeError) as e:
        print("exeption in .wav file: %s" % e)
        rate = -1
        validSound = False
        errorMessage = str(e)
    print("sound file size: %d, rate: %d" % (fileSize, rate))
    if validSound:
        sound_validationMessage = "👍︎ Sound file: %s (%d bytes), " % (name, fileSize)
        # extractionMessage = extractSoundPhrases(name, eafilename, projectDirectory)
        # sound_validationMessage += extractionMessage
        return sound_validationMessage, "information", filename
    else:
        if "Unsupported bit depth: the wav file has 24-bit data" in errorMessage:
            sound_validationMessage = "☠️ File %s (%d byes) has 24-bit data, must be minimum 32-bit." % (
                name, fileSize)
        elif "File contains data in an unknown format" in errorMessage:
            sound_validationMessage = "☠️ File %s unsupported format (see About SLEXIL)." % (
                name)
        else:
            sound_validationMessage = "☠️ Bad sound file: %s [File: %s (%d bytes)]" % (errorMessage, name, fileSize)
        return sound_validationMessage, "timewarning", filename


# ----------------------------------------------------------------------------------------------------
@app.callback(
    [Output('grammaticalTermsUploadStatus', 'children'),
     Output('grammaticalTermsUploadStatus', 'className'),
     Output('grammaticalTerms_filename_hiddenStorage', 'children')],
    [Input('upload-grammaticalTerms-file', 'contents')],
    [State('upload-grammaticalTerms-file', 'filename'),
     State('projectDirectory_hiddenStorage', 'children')]
)
def on_grammaticalTermsUpload(contents, name, projectDirectory):
    if name is None:
        return "", "warningOff", ""
    print("=== on_grammaticalTermsUpload")
    filename = os.path.join(projectDirectory, name)
    if filename[-4:] == '.eaf':
        return "☠️ Please select a text file, not the ELAN project file (.eaf).", "timewarning", ""
    encodedString = contents.encode("utf8").split(b";base64,")[1]
    decodedString = base64.b64decode(encodedString)
    try:
        s = decodedString.decode('utf-8')
    except UnicodeDecodeError:
        return "☠️ Please select a text (UTF-8) file.", "timewarning", ""
    s = s.replace("\t", "")
    with open(filename, "w") as fp:
        fp.write(s)
        fp.close()
    print("grammatical terms file: %s" % filename)
    return "👍 Uploaded abbreviations file: %s" % (name), "information", filename


# ----------------------------------------------------------------------------------------------------
@app.callback(
    Output('tierMapGui-div', 'children'),
    [Input("eaf_filename_hiddenStorage", 'children')],
    [State('tierMapGui-div', 'children')])
def createTierMappingMenusCallback(eafFilename, oldchildren):
    print("=== createTierMappingMenusCallback, eaf_filename_hiddenStorage trigger")
    if (eafFilename == ""):
        return ("")
    print("=== extract tier ids from %s" % (eafFilename))
    if oldchildren != '':
        print("the current children of tierMapGui are %s" % oldchildren)
    return (createTierMappingMenus(eafFilename))


# ----------------------------------------------------------------------------------------------------
@app.callback(
    Output('audioPhraseDirectory_hiddenStorage', 'children'),
    [Input('associateEAFAndSoundInfoTextArea', 'value')])
def update_output(value):
    print("=== callback triggered by associateEAFAndSoundTextArea change: %s" % value)
    phraseDirectory = value.split(":")[0]
    return (phraseDirectory)


# ----------------------------------------------------------------------------------------------------
@app.callback(
    [Output('webPageCreationStatus', 'className'),
     Output('webPageCreationStatus', 'children'),
     Output('progress', 'value')],
    [Input('createAndDisplayWebPageButton', 'n_clicks')],
    [State('progressBar_hiddenStorage','children')]
)
def show_progressBar(n_clicks,progressBar):
    print("=== show progress bar callback")
    if n_clicks == None:
        return 'progresstimewarning','This can take a minute or two for large texts.',0
    children = progressBar #[dbc.Progress("Working ...",id='progress', value=25,striped=True, animated=True, style={'display': 'inline'})]
    return 'progressbar', children, 50


# ----------------------------------------------------------------------------------------------------
@app.callback(
    Output('progress','barClassName'),
    [Input('progressBarStatus_hiddenStorage', 'children')]
)
def hide_progressBar(children):
    print("=== hide progress bar callback")
    if children == "done":
        return "previewoff"
    else:
        return ""

# ----------------------------------------------------------------------------------------------------
@app.callback(
    [Output('previewLink', 'href'),
     Output('downloadAssembledTextButton', 'disabled'),
     Output('createPageErrorMessages_hiddenStorage', 'children'),
     Output('createWebPageStatus', 'className'),
     Output('progressBarStatus_hiddenStorage', 'children')],
    [Input('progress', 'value')],
    [State('sound_filename_hiddenStorage', 'children'),
     State('eaf_filename_hiddenStorage', 'children'),
     State('projectDirectory_hiddenStorage', 'children'),
     State('grammaticalTerms_filename_hiddenStorage', 'children'),
     State('projectTitle_hiddenStorage', 'children')])
def createWebPageCallback(progressBarValue, soundFileName, eafFileName, projectDirectory,
                          grammaticalTermsFile, projectTitle):
    if progressBarValue == 0:
        return ("", 1, "", "previewoff","")
    print("=== create web page callback")
    print("eaf: %s" % eafFileName)
    tierGuide = os.path.join(projectDirectory, "tierGuide.yaml")
    # pdb.set_trace()
    if (grammaticalTermsFile == ""):
        grammaticalTermsFile = None
    else:
        print("grammaticalTermsFile: %s" % grammaticalTermsFile)

    htmlDoc = createWebPage(eafFileName, projectDirectory, grammaticalTermsFile,
                            tierGuide, soundFileName)

    webpageAt = os.path.join(projectDirectory, "%s.html" % projectTitle)
    absolutePath = os.path.abspath(webpageAt)
    print("webpage: %s" % webpageAt)
    with open(absolutePath, "w") as file:
        file.write(htmlDoc)
    errorLog = os.path.abspath(os.path.join(projectDirectory, "ERRORS.log"))
    errorMessage = ''
    if os.path.isfile(errorLog):
        with open(errorLog) as elog:
            logContents = elog.read()
            if "WARNING" in logContents:
                errorMessage = "Wrote file. Check error log for formatting issues."

    createZipFile(projectDirectory, projectTitle)
    # newButtonState = 0
    print("=== activating hyperLink to %s" % webpageAt)
    # pdb.set_trace()
    print("=== leaving web page callback")
    return (webpageAt, 0, errorMessage, "previewon","done")


# ----------------------------------------------------------------------------------------------------
@app.callback(
    [Output('createPageErrorMessages', 'children'),
     Output('createPageErrorMessages', 'className')],
    [Input('createPageErrorMessages_hiddenStorage', 'children')]
)
def setCreatePageErrorMessages(errorMessage):
    if len(errorMessage) == 0:
        className = 'warningOff'
    else:
        className = 'formatWarningOn'
    return (errorMessage, className)


# ----------------------------------------------------------------------------------------------------
@app.callback(
    [Output('projectTitle_hiddenStorage', 'children'),
     Output('upload-eaf-file', 'disabled'),
     Output('upload-grammaticalTerms-file', 'disabled')],
    [Input('setTitleButton', 'n_clicks')],
    [State('setTitleTextInput', 'value')]
)
def setTitle(n_clicks, newTitle):
    print("=== title callback")
    if n_clicks is None:
        print("n_clicks is None")
        return "", 1, 1
    if len(newTitle) == 0:
        print("no title provided")
        return "", 1, 1
    print("nClicks: %d, currentTitle: %s" % (n_clicks, newTitle))
    print("=== set project title")
    print("=== enable next button in sequence (upload .eaf file)")
    newTitle = newTitle.strip()
    newTitle = newTitle.replace(" ", "_")
    return newTitle, 0, 0


# ----------------------------------------------------------------------------------------------------
@app.callback(
    Output('projectDirectory_hiddenStorage', 'children'),
    [Input('projectTitle_hiddenStorage', 'children')]
)
def update_output(projectTitle):
    if (len(projectTitle) == 0):
        return ('')
    print("=== project title has been set, now create project directory: '%s'" % projectTitle)
    projectDirectory = os.path.join(PROJECTS_DIRECTORY, projectTitle)
    print("=== creating projectDirectory if needed: %s" % projectDirectory)
    if (not os.path.exists(projectDirectory)):
        os.mkdir(projectDirectory)
    print("=== creating logger and setting destination for log file: %s" % projectDirectory)
    return (projectDirectory)


# ----------------------------------------------------------------------------------------------------
@app.callback(
    Output('pageTitleH4', 'children'),
    [Input('projectDirectory_hiddenStorage', 'children')]
)
def update_pageTitle(projectDirectory):
    if (len(projectDirectory) == 0):
        return ('')
    print("=== projectDirectory_hiddenStorage has been set, now change project pageTitle: '%s'" % projectDirectory)
    newProjectTitle = projectDirectory.replace(PROJECTS_DIRECTORY, "")
    newProjectTitle = newProjectTitle.replace("/", "")
    print("IJAL Upload: %s" % newProjectTitle)
    return ('')


# ----------------------------------------------------------------------------------------------------
@app.callback(
    Output('speechTier_hiddenStorage', 'children'),
    [Input('tierGuideMenu-speech', 'value')])
def updateSpeechTier(value):
    if not value:
        value = ''
    print("speech tier user name: %s" % value)
    return value


# ----------------------------------------------------------------------------------------------------
@app.callback(
    Output('translationTier_hiddenStorage', 'children'),
    [Input('tierGuideMenu-translation', 'value')])
def updateTranslationTier(value):
    if not value:
        value = ''
    print("translation tier user name: %s" % value)
    return value


# ----------------------------------------------------------------------------------------------------
@app.callback(
    Output('morphemeTier_hiddenStorage', 'children'),
    [Input('tierGuideMenu-morpheme', 'value')])
def updateMorphemeTier(value):
    if not value:
        value = ''
    print("morpheme tier user name: %s" % value)
    return value


# ----------------------------------------------------------------------------------------------------
@app.callback(
    Output('morphemeGlossTier_hiddenStorage', 'children'),
    [Input('tierGuideMenu-morphemeGloss', 'value')])
def updateMorphemeGlossTier(value):
    if not value:
        value = ''
    print("morphemeGloss tier user name: %s" % value)
    return value


# ----------------------------------------------------------------------------------------------------
@app.callback(
    Output('translation2Tier_hiddenStorage', 'children'),
    [Input('tierGuideMenu-translation2', 'value')])
def updateTranslation2Tier(value):
    if not value:
        value = ''
    print("translation2 tier user name: %s" % value)
    return value


# ----------------------------------------------------------------------------------------------------
@app.callback(
    Output('transcription2Tier_hiddenStorage', 'children'),
    [Input('tierGuideMenu-transcription2', 'value')])
def updateTranscription2Tier(value):
    if not value:
        value = ''
    print("transcription2 tier user name: %s" % value)
    return value


# ----------------------------------------------------------------------------------------------------
@app.callback(
    [Output('tierMappingChoicesResultDisplay', 'children'),
     Output('tierGuide_filename_hiddenStorage', 'children'),
     Output('createAndDisplayWebPageButton', 'disabled')],
    [Input('saveTierMappingSelectionsButton', 'n_clicks')],
    [State('speechTier_hiddenStorage', 'children'),
     State('transcription2Tier_hiddenStorage', 'children'),
     State('morphemeTier_hiddenStorage', 'children'),
     State('morphemeGlossTier_hiddenStorage', 'children'),
     State('translationTier_hiddenStorage', 'children'),
     State('translation2Tier_hiddenStorage', 'children'),
     State('projectDirectory_hiddenStorage', 'children')])
def saveTierMappingSelection(n_clicks, speechTier, transcription2Tier, morphemeTier, morphemeGlossTier, translationTier,
                             translation2Tier, projectDirectory):
    if n_clicks is None:
        return ("", "", 1)
    print("== save tierMappingSelections")
    if len(speechTier) == 0:
        print("speechTier not mapped")
        return ("☠️ You must specify a tier for the first line.", "", 1)

    if len(translationTier) == 0:
        print("translationTier not mapped")
        return ("☠️ You must specify a tier for the translation.", "", 1)

    if len(morphemeTier) != 0 and len(morphemeGlossTier) == 0:
        print("morpheme tier but no morphemeGlossTier")
        return ("☠️ You must specify the tier for the morpheme glosses.", "", 1)

    if len(morphemeTier) == 0 and len(morphemeGlossTier) != 0:
        print("morpheme tier but no morphemeGlossTier")
        return ("☠️ You must specify the tier where the line is parsed.", "", 1)

    print("tierGuide.yaml contains")
    print("   speechTier: %s" % speechTier)
    print("   transcription2Tier: %s" % transcription2Tier)
    print("   morphemeTier: %s" % morphemeTier)
    print("   morphemeGlossTier: %s" % morphemeGlossTier)
    print("   translationTier: %s" % translationTier)
    print("   translation2Tier: %s" % translation2Tier)
    saveTierGuide(projectDirectory, speechTier, transcription2Tier, morphemeTier, morphemeGlossTier, translationTier,
                  translation2Tier)
    return ("👍 Your selections have been saved.", "tierGuide.yaml", 0)


# ----------------------------------------------------------------------------------------------------
@app.callback(Output('saveWebpageProgressTextArea', 'children'),
              [Input('confirmDownLoadObject', 'submit_n_clicks')],
              [State('projectTitle_hiddenStorage', 'children')])
def confirmDownload(submit_n_clicks, projectTitle):
    if not submit_n_clicks:
        return ''
    print("creating zip file")
    fullPath = createZipFile(projectTitle)
    return ("saved web page: %s" % fullPath)


# ----------------------------------------------------------------------------------------------------
# there can be multiple dash callbacks triggered by the same Input event.
# here we execute a second change to the webpage, returning the path to the project-specific
# webpage.zip, which is written into the href field of the html.A (or link) which nests the
# assembleTextButton
# ----------------------------------------------------------------------------------------------------
@app.callback(Output('downloadURL', 'href'),
              [Input('projectDirectory_hiddenStorage', 'children')],
              [State('projectTitle_hiddenStorage', 'children')])
def updateDownloadTextButtonHref(directory, projectTitle):
    print("=== projectDirectory_hiddenStorage changed, updateDownloadTextButtonHref: %s" % directory)
    projectTitle += '.zip'
    print(projectTitle)
    pathToZip = os.path.join(directory, projectTitle)
    return (pathToZip)


# ----------------------------------------------------------------------------------------------------
def saveTierGuide(projectDirectory, speechTier, transcription2Tier, morphemeTier, morphemeGlossTier, translationTier,
                  translation2Tier):
    tierDict = {"speech": speechTier,
                "transcription2": transcription2Tier,
                "morpheme": morphemeTier,
                "morphemeGloss": morphemeGlossTier,
                "translation": translationTier,
                "translation2": translation2Tier}

    filename = os.path.join(projectDirectory, "tierGuide.yaml")

    with open(filename, 'w') as outfile:
        yaml.dump(tierDict, outfile, default_flow_style=False)

    print("saved tierMap to %s" % filename)


# ----------------------------------------------------------------------------------------------------
def createWebPage(eafFileName, projectDirectory, grammaticalTermsFileName, tierGuideFileName, soundFileName):
    print("=== entering createWebPage")
    audioDirectoryRelativePath = "audio"
    print("eafFileName: %s" % eafFileName)
    print("projectDirectory: %s" % projectDirectory)
    print("audioDirectoryRelativePath: %s" % audioDirectoryRelativePath)
    print("grammaticalTermsFile: %s" % grammaticalTermsFileName)
    print("tierGuideFile: %s" % tierGuideFileName)
    print("soundFile: %s" % soundFileName)

    text = Text(eafFileName,
                soundFileName,
                grammaticalTermsFileName,
                tierGuideFileName,
                projectDirectory)
    print("=== leaving createWebPage")
    # pdb.set_trace()
    return (text.toHTML())


# ----------------------------------------------------------------------------------------------------
def createZipFile(projectDir, projectTitle):
    print("=== entering createZipFile")
    currentDirectoryOnEntry = os.getcwd()
    os.chdir(projectDir)
    print(projectDir)

    audioDir = "audio"
    filesToSave = [os.path.join("audio", f) for f in os.listdir(audioDir)]  # if f.endswith('.wav')]
    filesToSave.insert(0, "%s.html" % projectTitle)

    # zipfile is named for project
    zipFilename = "%s.zip" % projectTitle
    zipFilenameFullPath = os.path.join(currentDirectoryOnEntry, projectDir, zipFilename)
    zipHandle = ZipFile(zipFilename, 'w')

    # filesToSave includes ijal.css, ijalUtils.js
    CSSfile = os.path.join(currentDirectoryOnEntry, "ijal.css")
    scriptFile = os.path.join(currentDirectoryOnEntry, "ijalUtils.js")
    jqueryFile = os.path.join(currentDirectoryOnEntry, "jquery-3.3.1.min.js")
    copy(CSSfile, os.getcwd())
    copy(scriptFile, os.getcwd())
    copy(jqueryFile, os.getcwd())
    filesToSave.append("ijal.css")
    filesToSave.append("ijalUtils.js")
    filesToSave.append("jquery-3.3.1.min.js")
    if os.path.isfile("ERRORS.log"):
        print("=== adding errors log to .zip file")
        errorLog = ("ERRORS.log")
        filesToSave.append(errorLog)

    for file in filesToSave:
        zipHandle.write(file)

    zipHandle.close()

    os.chdir(currentDirectoryOnEntry)
    print(zipFilenameFullPath)
    return (zipFilenameFullPath)


# ----------------------------------------------------------------------------------------------------
# enable these lines for running from bash and python
if __name__ == "__main__":
    app.run_server(host='0.0.0.0', port=60041)

# enable these lines if running with gunicorn
# if __name__ == "__main__":
#     server = app.server
#     app.run()
