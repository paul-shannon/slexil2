#--------------------------------------------------------------------------------
def createProjectDirectory(projectName):

   path = os.path.join(PROJECTS_DIRECTORY, projectName)
   if not os.path.exists(path):
      os.mkdir(path)
   return path
      
#--------------------------------------------------------------------------------
setTitleDiv = html.Div(id="setTitleDiv",
          children=[
              html.H2('Enter Project Title: ',
                      style={'display':'inline-block', 'marginRight': "20px",
                             "fontSize": "24px"}),
              dcc.Input(id='projectNameInput',
                        type='text',
                        value='',
                        placeholder='',
                        debounce=True,
                        style={'display':'inline-block', 'fontSize': "24px",
                               'width': '400px'}),
              html.Button("Submit", id="setProjectNameButton", n_clicks=0,
                          style={'margin-left': '10px', 'margin-right': '10px'}),
              html.Div(id="projectTitleHelp", children=[
                  DashIconify(icon="feather:info", color="blue",width=30),
              ], style={"display": "inline-block"})
          ],className="bodyStyle")
#----------------------------------------------------------------------
dashApp.layout.children.append(setTitleDiv)
#----------------------------------------------------------------------
# @dashApp.callback(Output('globals', 'data', allow_duplicate=True),
#                   Output('fileTypeRadioButtons', 'options', allow_duplicate=True),
#                   Output('fileTypeRadioButtons', 'style', allow_duplicate=True),
#                   Output('inputFileTypePrompt', 'style', allow_duplicate=True),
#                   Input('projectNameInput', 'value'),
#                   State('globals', 'data'),
#                   prevent_initial_call=True)
# def saveProjectName_byCarriageReturn(projectTitle, globals):
#     characterCount = len(projectTitle)
#     if characterCount == 0:
#         projectTitle = "sp99"
#     projectName = projectTitle.replace(" ", "")
#     print("--- projectName: %s" % projectName)
#     globals['projectTitle'] = projectTitle
#     globals['projectName'] = projectName
#     enabledRadioButtonOptions=[
#         {'label': 'EAF', 'value': 'EAF', 'disabled': False},
#         {'label': 'YAML', 'value': 'YAML', 'disabled': False}
#         ]
#     radioButtonStyle = {'color': 'black', 'display': 'inline-block'}
#     inputFileTypePromptStyle = {'color': 'black'}
#     
#     return globals, enabledRadioButtonOptions, radioButtonStyle, inputFileTypePromptStyle
# 

@dashApp.callback(Output('globals', 'data', allow_duplicate=True),
                  Output('fileTypeChooserDiv', 'style'),
                  Input('setProjectNameButton', 'n_clicks'),
                  State('projectNameInput', 'value'),
                  State('globals', 'data'),
                  State('fileTypeChooserDiv', 'style'),
                  prevent_initial_call=True)
def saveProjectName_byButton(nClicks, projectTitle, globals, chooserStyle):
    characterCount = len(projectTitle)
    if characterCount == 0:
        projectTitle = "sp99"
    projectName = projectTitle.replace(" ", "")
    print("--- projectName: %s" % projectName)
    globals['projectTitle'] = projectTitle
    globals['projectName'] = projectName
    globals['projectPath'] = os.path.join(PROJECTS_DIR, projectName)
    chooserStyle['display'] = 'inline-block'
    #enabledRadioButtonOptions=[
    #    {'label': 'EAF', 'value': 'EAF', 'disabled': False},
    #    {'label': 'YAML', 'value': 'YAML', 'disabled': False}
    #    ]
    #radioButtonStyle = {'color': 'black', 'display': 'inline-block'}
    #inputFileTypePromptStyle = {'color': 'black'}
    #fileTypeChooserDivDisplay = "inline-block"
    
    return globals, chooserStyle

@callback(
    Output('slexilModal', 'is_open', allow_duplicate=True),
    Output('modalTitle', 'children', allow_duplicate=True),
    Output('modalBody', 'children', allow_duplicate=True),
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

# #----------------------------------------------------------------------
# @callback(
#     Output('globals', 'data'),
#     Output('fileTypeRadioButtons', 'options'),
#     Output('fileTypeRadioButtons', 'style'),
#     Output('inputFileTypePrompt', 'style'),
#     Input('setProjectNameButton', 'n_clicks'),
#     State('projectNameInput', 'value'),
#     State('globals', 'data'),
#     prevent_initial_call=True)
# def handleSetProjectNameButton(n_clicks, userEnteredString, data):
#     title = userEnteredString.strip()
#     newProjectName = title.replace(" ", "_")
#     projectPath = createProjectDirectory(newProjectName)
#     if data is None:
#        print("initializing None data")
#        data = {}
#     data['title'] = title
#     data['projectName'] = newProjectName
#     data['projectPath'] = projectPath
#     return(data, False)
#--------------------------------------------------------------------------------
