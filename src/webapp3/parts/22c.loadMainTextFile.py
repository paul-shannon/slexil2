uploaderStyle = {'width': '400px',
                 'height': '70px',
                 'lineHeight': '60px',
                 'borderWidth': '1px',
                 'borderStyle': 'solid',
                 'borderRadius': '5px',
                 'textAlign': 'center',
                 'fontSize': '24px',
                 'margin': '10px',
                 'marginLeft': '30px',
                 'display': 'none',
                 'background-color': '#F5FAF3',
                 ':hover': {
                    'background-color': 'lightblue'
                     }
                 }

simpleTextDisplayStyle = {'fontSize': '32px',
                          'marginLeft': '200px'
                          }

  # accept string (.eaf or .yaml) set in callback
  # function handleFileTypeSelection

mainTextLoaderDiv = html.Div(id="mainTextLoaderDiv",
                        children = [
                           dcc.Upload(
                              id='mainTextUploader',
                              children=html.Div(
                                  id='fileSelectorDiv',
                                  children = ['Drag and Drop or ',
                                              html.A('Select File')
                                              ]),
                              style=uploaderStyle,
                              multiple=False
                              )])

dashApp.layout.children.append(mainTextLoaderDiv)
#--------------------------------------------------------------------------------
@dashApp.callback(#Output('createHtmlButtonDiv', 'style'),
                  #Output('createHtmlButton', 'children'),
                  Output('analyzeButtonDiv', 'style'),
                  Output('analyzeButton', 'children'),    
                  Output('globals', 'data', allow_duplicate=True),

                  Output('slexilModal',   'is_open',  allow_duplicate=True),
                  Output('modalTitle',    'children', allow_duplicate=True),
                  Output('modalBody', 'children', allow_duplicate=True),

                  Input('mainTextUploader', 'contents'),
                  State('mainTextUploader', 'filename'),
                  State('mainTextUploader', 'last_modified'),
                  State('analyzeButtonDiv', 'style'),
                  State('globals', 'data'),
                  prevent_initial_call=True)

def handleMainTextUpload(contents, filename, date, analyzeButtonDivStyle, globals):

    globals['mainTextFilename'] = filename
    projectName = globals['projectName']
    projectTitle = globals['projectTitle']
    projectDirectory = os.path.join(PROJECTS_DIRECTORY, projectName)
    mainTextFilePath = os.path.join(projectDirectory, filename)
    analyzeButtonDivStyle['display'] = 'inline-block'
    globals['mainTextFilePath'] = mainTextFilePath

      # expected return values
    errorBoxOpen = False
    errorBoxChildren = None
    errorBoxTitle = None
    analyzeButtonDivStyle['display'] = 'inline-block' # assume success
    buttonLabel = "Assess %s file" % globals['fileType']

    try: 
        saveUploadedFile(contents, projectName, filename)
    except Exception as e:
       errorBoxOpen = True
       errorBoxTitle = "parse error"
       errorString = getExceptionTracebackString(e)
       errorBoxChildren = errorString
       analyzeButtonDivStyle['display'] = 'none'
       buttonLabel = "bug!"
       return (analyzeButtonDivStyle, buttonLabel, globals, errorBoxOpen,
               errorBoxTitle, errorBoxChildren)
       
    return (analyzeButtonDivStyle, buttonLabel, globals, errorBoxOpen,
            errorBoxTitle, errorBoxChildren)
   
#--------------------------------------------------------------------------------
def saveUploadedFile(contents, projectName, filename):

   print("saveUploadedFile: %s, %s" % (projectName, filename))
   print("content length: %d" % len(contents))
   
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
