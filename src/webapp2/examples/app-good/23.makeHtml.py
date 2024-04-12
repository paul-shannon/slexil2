#--------------------------------------------------------------------------------
createWebpageDiv = html.Div(id="createWebpageDiv",
          children=[
              html.Button("Create Webpage", id="createWebpageButton", n_clicks=0,
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
    #Output('htmlPreviewDiv', 'src'),
    Input('createWebpageButton', 'n_clicks'),
    State('memoryStore', 'data'),
    prevent_initial_call=True)
def createWebpageCallback(n_clicks, data):
    if data is None:
       print("initializing None data in 23.makeHtml.py")
       data = {}
    htmlFilePath = createWebPage(data["eafFullPath"], data["projectPath"], data["title"])
    now = datetime.now()
    currentTime = now.strftime("%H:%M:%S")
    data['webpage creation time'] = currentTime
    print("htmlFilePath: %s" % htmlFilePath)
    
    return data
#--------------------------------------------------------------------------------
