#--------------------------------------------------------------------------------
createWebpageDiv = html.Div(id="createWebPageDiv",
          children=[
              html.Button("Create Web Page", id="createWebpageButton", n_clicks=0,
                          disabled=False, className="enabledButton"),
              html.Div(id="createWebpageHelp", children=[
                  DashIconify(icon="feather:info", color="blue",width=30),
               ], style={"display": "inline-block"}),
             #html.Iframe(id="htmlPreviewDiv",
             #         style={"width": "95%", "height": "400px",
             #                "border": "1px solid blue"})
          ],className="bodyStyle", hidden=True)
#----------------------------------------------------------------------
dashApp.layout.children.append(createWebpageDiv)
#----------------------------------------------------------------------
@callback(
    Output('slexilModal', 'is_open', allow_duplicate=True),
    Output('modalTitle', 'children', allow_duplicate=True),
    Output('modalContents', 'children', allow_duplicate=True),
    Input('createWebpageHelp', 'n_clicks'),
    prevent_initial_call=True
    )
def displayCreateWebpageHelp(n_clicks):
    contents = html.Ul(id="list",
       children=[html.Li("explanation for createWebpage coming soon")
                 ])
    
    return True, "Help for Create Webpage", contents

#----------------------------------------------------------------------
@callback(
   Output('memoryStore', 'data', allow_duplicate=True),
   Output('previewButton', 'hidden'),
   Output('previewButton', 'className'),
   Output('downloadHtmlButton', 'hidden'),
   Output('downloadHtmlButton', 'className'),
   Output('downloadZipFileButton', 'hidden'),
   Output('downloadZipFileButton', 'className'),
   Output('loadTrackerDiv', 'children', allow_duplicate=True),
   Output('slexilModal',      'is_open',  allow_duplicate=True),
   Output('modalContents',    'children', allow_duplicate=True),
   Input('createWebpageButton', 'n_clicks'),
   State('memoryStore', 'data'),
   prevent_initial_call=True)
def createWebpageCallback(n_clicks, data):
   if data is None:
      print("initializing None data in 23.makeHtml.py")
      data = {}
      data['webpage creation time'] = currentTime
   previewButtonHidden = False
   previewButtonClass = "enabledButton"
   downloadZipButtonHidden = True
   downloadZipButtonClass = "disabledButton"
   try:
      preferredMediaURL = None
      if "audioFileName" in data.keys():
          preferredMediaURL = data["audioFileName"]
      htmlFilePath = createWebPage(data["eafFullPath"],
                                   data["projectPath"],
                                   data["title"],
                                   preferredMediaURL)
      now = datetime.now()
      currentTime = now.strftime("%H:%M:%S")
      modalOpen = False
      modalContents = ""
      downloadHtmlButtonHidden = False
      downloadHtmlButtonClass = "enabledButton"
      if "audioFileName" in data.keys():
         downloadZipButtonHidden = False
         downloadZipButtonClass = "enabledButton"
   except BaseException as e:
      modalOpen = True
      #modalTitle = "create webpage error"
      modalContents = html.Pre(get_exception_traceback_str(e))
   results = [data, previewButtonHidden,
              previewButtonClass,
              downloadHtmlButtonHidden, downloadHtmlButtonClass,
              downloadZipButtonHidden, downloadZipButtonClass, "",
              modalOpen, modalContents]
   return results
#--------------------------------------------------------------------------------





