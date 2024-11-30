uploaderStyle = {'width': '400px',
                 'height': '70px',
                 'lineHeight': '60px',
                 'borderWidth': '1px',
                 'borderStyle': 'solid',
                 'borderRadius': '5px',
                 'textAlign': 'center',
                 'fontSize': '24px',
                 'margin': '10px',
                 'marginLeft': '50px',
                 'display': 'none',
                 'background-color': '#F5FAF3',
                 ':hover': {
                    'background-color': 'lightblue'
                     }
                 }

simpleTextDisplayStyle = {'fontSize': '32px',
                          'marginLeft': '200px'
                          }

mainTextLoaderDiv = html.Div(id="mainTextLoaderDiv",
                        children = [
                           dcc.Upload(
                              id='mainTextUploader',
                              accept=".eaf",
                              #className='textUploader',
                              children=html.Div(
                                  id='fileSelectorDiv',
                                  children = ['Drag and Drop or ',
                                              html.A('Select File')
                                              ]), #className="mainTextUploader"),
                              style=uploaderStyle,
                              multiple=False
                              )])

dashApp.layout.children.append(mainTextLoaderDiv)
#--------------------------------------------------------------------------------
@dashApp.callback(Output('createHtmlButtonDiv', 'style'),
                  Output('createHtmlButton', 'children'),
                  Output('globals', 'data', allow_duplicate=True),

                  Output('slexilModal',   'is_open',  allow_duplicate=True),
                  Output('modalTitle',    'children', allow_duplicate=True),
                  Output('modalContents', 'children', allow_duplicate=True),

                  Input('mainTextUploader', 'contents'),
                  State('mainTextUploader', 'filename'),
                  State('mainTextUploader', 'last_modified'),
                  State('createHtmlButtonDiv', 'style'),
                  State('globals', 'data'),
                  prevent_initial_call=True)

def handleMainTextUploadAndEafParse(contents, filename, date, buttonDivStyle, globals):

    globals['mainTextFilename'] = filename
    projectName = globals['projectName']
    projectTitle = globals['projectTitle']
    projectDirectory = os.path.join(PROJECTS_DIRECTORY, projectName)
    mainTextFilePath = os.path.join(projectDirectory, filename)
    buttonDivStyle['display'] = 'inline-block'
    globals['mainTextFilePath'] = mainTextFilePath

      # expected return values
    errorBoxOpen = False
    errorBoxChildren = None
    errorBoxTitle = None
    buttonDivStyle['display'] = 'inline-block' # assume success
    buttonLabel = "Create %s.html" % globals['projectTitle']

    try: 
        saveUploadedFile(contents, projectName, filename)
        fileType = globals['fileType']
        print("%s has format %s" % (filename, fileType))
        if fileType == "EAF":
            p = EafParser(mainTextFilePath, verbose=True,
                          fixOverlappingTimeSegments=False)

            p.run()
            title = globals['projectTitle'] = projectTitle
            yamlText = p.toYAML(projectTitle, projectName, projectName)
            yamlFileName = os.path.join(projectDirectory, "%s.yaml" % projectName)
            p.writeYAML(yamlText, yamlFileName)
            globals['yamlFileName'] = yamlFileName
            #pdb.set_trace()
            tbl = p.getTierTable()
            globals['tiers'] = list(tbl['TIER_ID'])
            globals['time aligned'] = list(tbl['TIME_ALIGNABLE'])
            globals['parent'] = list(tbl['PARENT_REF'])
            globals['lineCount'] = list(tbl['LINES'])
            print(p.getTierTable())
            if fileType == "YAML":
                globals['yamlFileName'] = mainTextFilePath

    except Exception as e:
       errorBoxOpen = True
       errorBoxTitle = "parse error"
       errorString = getExceptionTracebackString(e)
       errorBoxChildren = errorString
       #errorBoxChildren = dbc.ModalBody(e.__str__())
       buttonDivStyle['display'] = 'none'
       buttonLabel = "bug!"
       return (buttonDivStyle, buttonLabel, globals, errorBoxOpen,
               errorBoxTitle, errorBoxChildren)
       
    #pdb.set_trace()
    return (buttonDivStyle, buttonLabel, globals, errorBoxOpen,
           errorBoxTitle, errorBoxChildren)
    #return globals, errorBoxOpen, errorBoxChildren
   
#--------------------------------------------------------------------------------
def saveUploadedFile(contents, projectName, filename):

   data = contents.encode("utf8").split(b";base64,")[1]
   print("len(data) = %d" %len(data))

   targetDirectory = os.path.join(PROJECTS_DIRECTORY, projectName)
   if (not os.path.exists(targetDirectory)):
        os.mkdir(targetDirectory)
   newFile = os.path.join(targetDirectory, filename)

   with open(newFile, "wb") as fp:
      fp.write(base64.decodebytes(data))
   print("Filename: %s" % newFile)
   assert(os.path.isfile(newFile))

#--------------------------------------------------------------------------------
