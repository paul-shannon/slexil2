#--------------------------------------------------------------------------------
downloadAndDisplayDiv = html.Div(id="downloadAndDisplayDiv",
          children=[html.Button("Display", id="displayStaticHTMLButton",
                                n_clicks=0, hidden=True, className="disabledButton"),
                    html.Button("Download Web Page", id="downloadWebPageButton",
                                n_clicks=0, hidden=True, className="disabledButton"),
                    dcc.Download(id="downloader"),
                    html.Iframe(id="displayIFrame",
                                style={"width": "95%", "height": "800px",
                                       "overflow": "auto"})
                    ])
dashApp.layout.children.append(downloadAndDisplayDiv)
#--------------------------------------------------------------------------------
@callback(
    Output('displayIFrame', 'src'),
    Input('displayStaticHTMLButton', 'n_clicks'),
    State('memoryStore', 'data'),
    prevent_initial_call=True
    )
def displayPage(n_clicks, data):
    projectName = data["projectName"]
    htmlFileName = "%s.html" % projectName
    htmlFileFullPath = "PROJECTS/%s/%s" % (projectName, htmlFileName)
    url = "%s" % htmlFileFullPath
    return url

@callback(
    Output('downloader', 'data'),
    Input('downloadWebPageButton', 'n_clicks'),
    State('memoryStore', 'data'),
    prevent_initial_call=True
    )
def downloadWebPage(n_clicks, data):
    projectName = data["projectName"]
    htmlFileName = "%s.html" % projectName
    htmlFileFullPath = "PROJECTS/%s/%s" % (projectName, htmlFileName)
    return dcc.send_file(htmlFileFullPath)

#--------------------------------------------------------------------------------
