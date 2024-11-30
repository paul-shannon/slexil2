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

                  Output('slexilModal',   'is_open',  allow_duplicate=True),
                  Output('modalTitle',    'children', allow_duplicate=True),
                  Output('modalContents', 'children', allow_duplicate=True),

                  [Input('createHtmlButton', 'n_clicks')],
                  State('downloadHtmlButtonDiv', 'style'),
                  State('globals', 'data'),
                  prevent_initial_call=True)
def createHtml(n_clicks, buttonDivStyle, globals):

   print("--- runSlexil, n_clicks: %d" % n_clicks)
   title = globals['projectTitle']

      # expected return values
   errorBoxOpen = False
   errorBoxChildren = None
   errorBoxTitle = None

   buttonDivStyle['display'] = 'inline-block'
   buttonLabel = "Download %s.html" % globals['projectTitle']

   projectName = globals['projectName']
   projectDirectory = os.path.join(PROJECTS_DIRECTORY, globals['projectName'])
   fileType = globals['fileType']
   if fileType == "YAML":
      yamlFileName = globals['mainTextFilePath']
   elif fileType == "EAF":
      yamlFileName = globals['yamlFileName']

   try:
      htmlFileName = createHtmlFromYaml(yamlFileName, title,
                                        projectName, projectDirectory)
   except Exception as e:
      errorBoxOpen = True
      errorBoxTitle = "Slexil ERROR! in createHTML function"
      errorString = getExceptionTracebackString(e)
      htmlErrorMessage = createHtmlErrorReportWithEmailLink(globals, errorString)
      errorBoxChildren = dbc.ModalBody(htmlErrorMessage)
      buttonDivStyle['display'] = 'none'
      buttonLabel = "" # ignored
      return (buttonDivStyle, buttonLabel, globals, errorBoxOpen,
              errorBoxTitle, errorBoxChildren)
      
   globals['htmlFileName'] = htmlFileName
   return (buttonDivStyle, buttonLabel, globals, errorBoxOpen,
           errorBoxTitle, errorBoxChildren)
           
        
#--------------------------------------------------------------------------------
def createHtmlErrorReportWithEmailLink(globals, errorString):

   sendTo = 'mailto:paul.thurmond.shannon@gmail.com'
   subject = '?subject=slexil bug report'
   bodyLeadIn = '&body='
   bodyText = ""
   for key in globals.keys():
       bodyText += "%s: %s\n" % (key, globals[key])
   bodyText += "\n\n%s" % errorString
   bodyTextCRLF = bodyText.replace("\n", "%0D%0A")
   body = "%s%s" % (bodyLeadIn, bodyTextCRLF)
   emailHref = '%s%s%s' % (sendTo, subject, body)
   el = html.Ul(id="list", children=[])
   for key in globals.keys():
       el.children.append(html.Li("%s: %s" % (key, globals[key])))
   el.children.append(html.A(
      [html.H1('Email Slexil Bug Report to Paul Shannon')],
       title ='email_me',
       href=emailHref,
       target='_blank'))

   return el

#--------------------------------------------------------------------------------
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

