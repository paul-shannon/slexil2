#--------------------------------------------------------------------------------
downloadAndDisplayDiv = html.Div(id="downloadAndDisplayDiv",
          children=[html.Button("Preview", id="previewButton",
                                n_clicks=0, hidden=True, className="disabledButton"),
                    html.Button("Download Web Page", id="downloadHtmlButton",
                                n_clicks=0, hidden=True, className="disabledButton"),
                    html.Button("Download Web Page with Audio",
                                id="downloadZipFileButton",
                                n_clicks=0, hidden=True, className="disabledButton"),
                    dcc.Download(id="htmlDownloader"),
                    dcc.Download(id="zipDownloader"),
                    html.Iframe(id="displayIFrame",
                                style={"width": "95%", "height": "800px",
                                       "overflow": "auto"})
                    ])
dashApp.layout.children.append(downloadAndDisplayDiv)
#--------------------------------------------------------------------------------
def createZipFile(projectDir, projectTitle, audioFile):
    print("=== entering createZipFile")
    currentDirectoryOnEntry = os.getcwd()
    print("    currentDirectoryOnEntry: %s" % currentDirectoryOnEntry)
    print("    projectDir: %s" % projectDir)
    os.chdir(projectDir)
    print(projectDir)
    filesToSave = []
    filesToSave.insert(0, "%s.html" % projectTitle)
    filesToSave.append(audioFile)

    # zipfile is named for project
    zipFilename = "%s.zip" % projectTitle
    zipFilenameFullPath = os.path.join(currentDirectoryOnEntry, projectDir, zipFilename)
    zipHandle = zipfile.ZipFile(zipFilename, 'w')
    for file in filesToSave:
        print("   adding %s" % file)
        zipHandle.write(file)

    zipHandle.close()
    os.chdir(currentDirectoryOnEntry)
    print("=== leaving createZipFile")

    return zipFilenameFullPath

#--------------------------------------------------------------------------------
@callback(
    Output('displayIFrame', 'src'),
    Input('previewButton', 'n_clicks'),
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
    Output('htmlDownloader', 'data'),
    Input('downloadHtmlButton', 'n_clicks'),
    State('memoryStore', 'data'),
    prevent_initial_call=True
    )
def downloadWebPage(n_clicks, data):
    projectName = data["projectName"]
    htmlFileName = "%s.html" % projectName
    htmlFileFullPath = "PROJECTS/%s/%s" % (projectName, htmlFileName)
    return dcc.send_file(htmlFileFullPath)

@callback(
    Output('zipDownloader', 'data'),
    Input('downloadZipFileButton', 'n_clicks'),
    State('memoryStore', 'data'),
    prevent_initial_call=True
    )
def downloadZip(n_clicks, data):
    projectName = data["projectName"]
    projectDir =  "PROJECTS/%s" % projectName
    audioFile = data["audioFileName"]
    zipFilePath = createZipFile(projectDir, projectName, audioFile)
    print("=== calling dcc.send_file: %s" % zipFilePath)
    return dcc.send_file(zipFilePath)

#--------------------------------------------------------------------------------
