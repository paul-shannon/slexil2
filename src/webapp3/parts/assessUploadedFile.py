from slexil.newYamlParser import NewYamlParser
from slexil.eafParser import extractAllTimeAlignedTierIDs
#--------------------------------------------------------------------------------
analyzeButtonStyle = {"margin": "15px",
                      "margin-left": "30px",
                      "fontSize": "20px",
                      "border": "1px solid gray",
                      "borderRadius": "10px"
                      }


#--------------------------------------------------------------------------------
analyzeButtonDiv = html.Div(id="analyzeButtonDiv",
                            style={'display': 'none'},
                            children=[html.Button('Assess',
                                                  id='analyzeButton',
                                                  style=analyzeButtonStyle)]
                            )
dashApp.layout.children.append(analyzeButtonDiv)
#--------------------------------------------------------------------------------
@dashApp.callback(Output('globals',       'data',     allow_duplicate=True),
                  Output('slexilModal',   'is_open',  allow_duplicate=True),
                  Output('modalTitle',    'children', allow_duplicate=True),
                  Output('modalBody',     'children', allow_duplicate=True),
                  Output('createHtmlButtonDiv', 'style'),
                  Output('analyzeButtonDiv', 'style', allow_duplicate=True),

                  [Input('analyzeButton', 'n_clicks')],
                  State('globals', 'data'),
                  State('createHtmlButtonDiv', 'style'),
                  State('analyzeButtonDiv', 'style'),
                  prevent_initial_call=True)
def analyze(n_clicks,  globals, createHtmlDivStyle, analyzeButtonDivStyle):

   #print("--- analyze %s" % globals['mainTextFilename'])

   errorBoxOpen = False
   errorBoxChildren = None
   errorBoxTitle = None
   createHtmlDivStyle['display'] = 'none' # pessimistic: assume failure here

   fileType = globals['fileType']
   mainTextFilePath = globals['mainTextFilePath']
   #print("%s has format %s" % (mainTextFilePath, fileType))
   mediaURL = "unknown"
   timeAlignedTierCount = 1 # only possibilit with current YAML format
   try:
      if fileType == "EAF":
         p = EafParser(mainTextFilePath, verbose=True,
                       fixOverlappingTimeSegments=False)
         p.run()
         tbl = p.getTierTable()
         mediaURL = p.getMediaURL()
         timeAlignedTiers = extractAllTimeAlignedTierIDs(mainTextFilePath)
         if len(timeAlignedTiers) > 1:
            tierNamesString = " ".join(timeAlignedTiers)
            #errorMessage = html.Div(children=[
            #   html.P("%d time-aligned tiers found: %s" % (len(timeAlignedTiers), tierNamesString)),
            #   html.P("""Slexil currently supports only one time-aligned tier. 
            #             Email a bug report (see below) if you wish to request 
            #             such support in a future release.""")])
            msg = "%d time-aligned tiers found: %s,  " %\
                    (len(timeAlignedTiers), tierNamesString)
            msg += " but Slexil currently supports only one time-aligned tier.  "
            msg += "Email a bug report (see below) if you wish to request "
            msg += "such support in a future release."
            raise Exception(msg)
         yaml = p.toYAML("a", "b", "c")
         yamlFile = os.path.join(globals['projectPath'],
                                 "%s.yaml" % globals['projectName'])
         p.writeYAML(yaml, yamlFile)
         globals['yamlFileName'] = yamlFile
      elif fileType == "YAML":
         p = NewYamlParser(mainTextFilePath)
         tbl = p.getTierTable()
         mediaURL = p.getMediaURL()
      formattedTable = dbc.Table.from_dataframe(tbl)
      errorBoxOpen = True
      errorBoxChildren = html.Div(children=[html.P("media url: %s" % mediaURL),
                                            html.P("time-aligned tier count: %d" %
                                                   timeAlignedTierCount),
                                            html.P(formattedTable)])
      errorBoxTitle = "Valid Structure"
      createHtmlDivStyle['display'] = 'inline-block'
      analyzeButtonDivStyle['display'] = 'inline-block'
      return (globals, errorBoxOpen, errorBoxTitle, errorBoxChildren,
              createHtmlDivStyle, analyzeButtonDivStyle)

   except Exception as e:
      errorBoxOpen = True
      errorBoxTitle = "%s PARSING ERROR" % globals['fileType']
      (traceBackString, errorString) = getExceptionTracebackString(e)
      #print("  traceBackString: %s" % traceBackString)
      #print("  errorString: %s" % errorString)
      if type(errorString) is list:
         errorString = errorString[0]
         errorStrings = errorString.split('\n')
         errorStringHtml = html.Ul(children=[])
         for element in errorStrings:
            if(len(element) > 0):
               errorStringHtml.children.append(html.Li(element))
      else:
         errorStringHtml = html.P(errorString)
      htmlErrorMessage = createHtmlErrorReportWithEmailLink(globals,
                                                            errorString,
                                                            errorStringHtml,
                                                            traceBackString)
      #htmlErrorMessage = createHtmlErrorReportWithEmailLink(globals, errorString, traceBackString)
      errorBoxChildren = dbc.ModalBody(htmlErrorMessage)
      #errorBoxChildren = errorString
      #pdb.set_trace()
      #errorBoxChildren = dbc.ModalBody(e.__str__())
      #buttonDivStyle['display'] = 'none'
      #buttonLabel = "bug!"
      analyzeButtonDivStyle['display'] = 'none'
      return (globals, errorBoxOpen, errorBoxTitle, errorBoxChildren,
              createHtmlDivStyle, analyzeButtonDivStyle)

#--------------------------------------------------------------------------------
