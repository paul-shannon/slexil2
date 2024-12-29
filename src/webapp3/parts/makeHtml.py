from slexil.yamlToText import YamlToText
from slexil.morphemeGlossAbbreviations import MorphemeGlossAbbreviations


createHtmlButtonDiv = html.Div(id="createHtmlButtonDiv",
                               style={'display': 'none'},
                               children=[html.Button('Create HTML',
                                                     id='createHtmlButton',
                                                     style=buttonStyle)]
                               )

#--------------------------------------------------------------------------------
dashApp.layout.children.append(createHtmlButtonDiv)
#--------------------------------------------------------------------------------
@dashApp.callback(Output('downloadHtmlButtonDiv', 'style'),
                  Output('downloadHtmlButton', 'children'),
                  Output('globals', 'data', allow_duplicate=True),

                  Output('slexilModal',   'is_open',  allow_duplicate=True),
                  Output('modalTitle',    'children', allow_duplicate=True),
                  Output('modalBody', 'children', allow_duplicate=True),

                  [Input('createHtmlButton', 'n_clicks')],
                  State('downloadHtmlButtonDiv', 'style'),
                  State('globals', 'data'),
                  prevent_initial_call=True)
def createHtml(n_clicks, downloadHtmlButtonDivStyle, globals):

   print("--- runSlexil, n_clicks: %d" % n_clicks)
   title = globals['projectTitle']

      # expected return values
   errorBoxOpen = False
   errorBoxChildren = None
   errorBoxTitle = None

   downloadHtmlButtonDivStyle['display'] = 'inline-block'
   downloadHtmlButtonLabel = "Download %s.html" % globals['projectTitle']

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
      errorBoxTitle = "Slexil ERROR! in createHtml function"
      (traceBackString, errorString) = getExceptionTracebackString(e)
      errorStringHtml = html.P(errorString)
      htmlErrorMessage = createHtmlErrorReportWithEmailLink(globals,
                                                            errorString,
                                                            errorStringHtml,
                                                            traceBackString)
      errorBoxChildren = dbc.ModalBody(htmlErrorMessage)
      downloadHtmlButtonDivStyle['display'] = 'none'
      downloadHtmlButtonLabel = "" # ignored
      return (downloadHtmlButtonDivStyle, downloadHtmlButtonLabel,
              globals, errorBoxOpen,
              errorBoxTitle, errorBoxChildren)
      
   globals['htmlFileName'] = htmlFileName
   return (downloadHtmlButtonDivStyle, downloadHtmlButtonLabel,
           globals, errorBoxOpen,
           errorBoxTitle, errorBoxChildren)
           
        
#--------------------------------------------------------------------------------
#def createHtmlFromEAF(eafFile, title, projectName, projectDirectory):
#
#   yamlFileName = globals['yamlFileName']
#   htmlFileName = createHtmlFromYaml(yamlFileName, title, projectName, projectDirectory)
#   return htmlFilename
#
#--------------------------------------------------------------------------------
def createHtmlFromYaml(yamlFile, title, projectName, projectDirectory):

   mga = MorphemeGlossAbbreviations()

   print("--- makeHtml.py: createHtmlFromYaml")

   text = YamlToText(yamlFile,
                     grammaticalTerms=mga.getAll(),
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

#--------------------------------------------------------------------------------
