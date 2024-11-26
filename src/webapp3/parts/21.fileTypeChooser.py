#--------------------------------------------------------------------------------
fileTypeChooserDiv = html.Div(id="fileTypeChooserDiv",
             style={'margin': '5px', 'marginLeft': '10px', 'fontSize': '24px',
                    'display': 'none', 'marginRight': '10px'},
             children=[html.Span("Input File Type? ",
                                 id="inputFileTypePrompt",
                                 style={'fontFamily': 'New York Times-Roman',
                                        'fontSize': '24px'}
                                 ),
                       dcc.RadioItems(id="fileTypeRadioButtons",
                                      options=[
                                          {'label': '   EAF  ', 'value': 'EAF', 'disabled': False},
                                          {'label': '   YAML  ', 'value': 'YAML', 'disabled': False}
                                         ],
                                      labelStyle={'display': 'inline-block', 'margin': '20px', 'margin-top': '0px'},
                                      inline=True,
                                      style={'display': 'inline-block',
                                             'fontFamily': 'New York Times-Roman',
                                             'font-size': '24px'})
                       ])
#----------------------------------------------------------------------
dashApp.layout.children.append(fileTypeChooserDiv)
#----------------------------------------------------------------------
@dashApp.callback(Output('globals', 'data', allow_duplicate=True),
                  Output('mainTextUploader', 'style'),
                  Input('fileTypeRadioButtons', 'value'),
                  State('globals', 'data'),
                  State('mainTextUploader', 'style'),
                  prevent_initial_call=True)
def handleFileTypeSelection(fileType,  globals, uploaderStyle):
    print("handleFileTypeSelection: %s" % fileType)
    newText = dcc.Markdown("- input file type: %s" % fileType)
    globals['fileType'] = fileType
    uploaderStyle['display'] =  'inline-block'
    return globals, uploaderStyle

