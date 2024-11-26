from slexil.yamlToText import YamlToText


buttonDiv = html.Div(id="buttonDiv",
             style={"margin": "20px"},
             children=[
                 html.Div(id="createHtmlButtonDiv",
                          style={'display': 'none'},
                          children=[html.Button('Create HTML',
                                                id='createHtmlButton',
                                                style=buttonStyle)]
                          ),
                 html.Div(id="downloadHtmlButtonDiv",
                          style={'display': 'none'},
                          children=[html.Button("Download HTML",
                                                id="downloadHtmlButton",
                                                style=buttonStyle),
                                    dcc.Download(id="download-html")]),
                 html.Div(id="downloadYamlButtonDiv",
                          style={'display': 'none'},
                          children=[html.Button("Download YAML",
                                                id="btn-download-txt",
                                                className="button"),
                                    dcc.Download(id="download-yaml")],
                          )
                 ])

#--------------------------------------------------------------------------------
dashApp.layout.children.append(buttonDiv)
#--------------------------------------------------------------------------------
@dashApp.callback(Output('downloadHtmlButtonDiv', 'style'),
                  Output('downloadHtmlButton', 'children'),
                  Output('globals', 'data', allow_duplicate=True),
                  [Input('createHtmlButton', 'n_clicks')],
                  State('downloadHtmlButtonDiv', 'style'),
                  State('globals', 'data'),
                  prevent_initial_call=True)
def createHtml(n_clicks, buttonDivStyle, globals):

   print("--- runSlexil, n_clicks: %d" % n_clicks)
   title = globals['projectTitle']

   buttonDivStyle['display'] = 'inline-block'
   buttonLabel = "Download %s.html" % globals['projectTitle']

   projectName = globals['projectName']
   projectDirectory = os.path.join(PROJECTS_DIRECTORY, globals['projectName'])
   fileType = globals['fileType']
   if fileType == "YAML":
      yamlFileName = globals['mainTextFilePath']
   elif fileType == "EAF":
      yamlFileName = globals['yamlFileName']
   htmlFileName = createHtmlFromYaml(yamlFileName, title,
                                     projectName, projectDirectory)
   globals['htmlFileName'] = htmlFileName
   return buttonDivStyle, buttonLabel, globals
        
def createHtmlFromEAF(eafFile, title, projectName, projectDirectory):

   yamlFileName = globals['yamlFileName']
   htmlFileName = createHtmlFromYaml(yamlFileName, title, projectName, projectDirectory)
   return htmlFilename

def createHtmlFromYaml(yamlFile, title, projectName, projectDirectory):

   text = YamlToText(yamlFile,
                     grammaticalTerms=[],
                     projectDirectory=projectDirectory,
                     verbose = False,
                     fontSizeControls = True,
                     startLine = None,
                     endLine = None,
                     pageTitle = title,
                     helpFilename = None,
                     helpButtonLabel = None,
                     kbFilename = None,
                     linguisticsFilename = None,
                     fixOverlappingTimeSegments = False,
                     webpackLinksOnly=False,
                     useTooltips=False)
   htmlText = text.toHTML()
   htmlFileName = os.path.join(projectDirectory, "%s.html" % projectName)
   print("--- writing html file for at %s" % htmlFileName)
   with open(htmlFileName, "w") as file:
       file.write(htmlText)
   return htmlFileName


@dashApp.callback(
    Output("download-html", "data"),
    Input("downloadHtmlButton", "n_clicks"),
    State("globals", "data"),
    prevent_initial_call=True,
    )
def downloadHtml(n_clicks, globals):
    print("--- 23a downloadHtml")
    
    filename = os.path.join(PROJECTS_DIRECTORY,
                            globals['projectName'],
                            "%s.html" % globals['projectName'])
    return dcc.send_file(filename)

