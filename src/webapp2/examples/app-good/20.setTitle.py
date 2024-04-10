#--------------------------------------------------------------------------------
def createProjectDirectory(projectName):

   path = os.path.join(PROJECTS_DIRECTORY, projectName)
   if not os.path.exists(path):
      os.mkdir(path)
   return path
      
#--------------------------------------------------------------------------------
setTitleDiv = html.Div(id="setTitleDiv",
          children=[
              html.H2('Project Title: ',
                      style={'display':'inline-block', 'marginRight': "20px",
                             "fontSize": "24px"}),
              dcc.Input(id='projectNameInput',type='text',
                        placeholder='',
                        style={'display':'inline-block', 'fontSize': "24px",
                               'width': '400px'}),
              html.Button("Submit", id="setProjectNameButton", n_clicks=0,
                          disabled=True, className="disabledButton"),
              html.Div(id="projectTitleHelp", children=[
                  DashIconify(icon="feather:info", color="blue",width=30),
              ], style={"display": "inline-block"})
          ],className="bodyStyle")
#----------------------------------------------------------------------
dashApp.layout.children.append(setTitleDiv)
#----------------------------------------------------------------------
@callback(
    Output('setProjectNameButton', 'className'),
    Output('setProjectNameButton', 'disabled'),
    Input('projectNameInput', 'value'),
    prevent_initial_call=True)
def handleProjectNameInputChars(userEnteredString):
    characterCount = len(userEnteredString)
    print("string size: %d" % characterCount)
    minCharacterCount = 3
    if(characterCount >= minCharacterCount):
        return "enabledButton", False
    else:
        return "disabledButton", True

@callback(
    Output('slexilModal', 'is_open', allow_duplicate=True),
    Output('modalTitle', 'children', allow_duplicate=True),
    Output('modalContents', 'children', allow_duplicate=True),
    Input('projectTitleHelp', 'n_clicks'),
    prevent_initial_call=True
    )
def displayProjectTitleHelp(n_clicks):
    contents = html.Ul(id="list",
       children=[html.Li("Your title will be displayed prominently at the top of the web page we create from your text."),
                 html.Li("We recommend a concise and descriptive name, 3-40 characters long."),
                 html.Li("It can include spaces and upper and lower case characters."),
                 html.Li("For instance: How Daylight Was Stolen - Harry Moses.")
                 ])
    
    return True, "Help for Project Title Input", contents

#----------------------------------------------------------------------
@callback(
    Output('memoryStore', 'data'),
    Output('eafLoaderDiv', 'hidden'),
    Input('setProjectNameButton', 'n_clicks'),
    State('projectNameInput', 'value'),
    State('memoryStore', 'data'),
    prevent_initial_call=True)
def handleSetProjectNameButton(n_clicks, userEnteredString, data):
    print("--- handleSetProjectNameButton: %d, %s" % (n_clicks, userEnteredString))
    title = userEnteredString.strip()
    newProjectName = title.replace(" ", "_")
    projectPath = createProjectDirectory(newProjectName)
    if data is None:
       print("initializing None data")
       data = {}
    data['title'] = title
    data['projectName'] = newProjectName
    data['projectPath'] = projectPath
    return(data, False)
#--------------------------------------------------------------------------------
