#--------------------------------------------------------------------------------
audioLoaderDiv = html.Div(id="audioLoaderDiv",
                          children=[
                              dcc.Upload(
                                  id='audioUploader',
                                  accept=".wav",
                                  children=html.Div([
                                      'Drag and Drop or ',
                                      html.A('Select Audio file')
                                  ], className="fubar"),
                                  className="eafUploader",
                                  multiple=False
                              )], hidden=False)

dashApp.layout.children.append(audioLoaderDiv)
#--------------------------------------------------------------------------------
@callback(
   Output('slexilModal',      'is_open',  allow_duplicate=True),
   Output('modalContents',    'children', allow_duplicate=True),
   Output('memoryStore',      'data',     allow_duplicate=True),
   #Output('createWebpageDiv', 'hidden'),
   Input('audioUploader',    'contents'),
   State('audioUploader',    'filename'),
   State('memoryStore',      'data'),
   prevent_initial_call=True)
def audioUploadHandler(fileContents, filename, data):

   print("=== soundUploadHandler")

   if filename is None:
       return("","",1)

   if data is None:
      data = {}

   data['audioFileName'] = filename;
   modalOpen = False
   modalContents = ""
   
   try:
      fileData = fileContents.encode("utf8").split(b";base64,")[1]
      fullPath = os.path.join(data['projectPath'], filename)
      with open(fullPath, "wb") as fp:
         fp.write(base64.decodebytes(fileData))

      assert(os.path.isfile(fullPath))
      fileSize = os.path.getsize(fullPath)
      data['audioFullPath'] = fullPath
      data['audioFileSize'] = fileSize
      #rate, mtx = wavfile.read(fullPath)
      #data["audioSamplingRate"] = rate
      #print(mtx)

   except BaseException as e:
      modalOpen = True
      modalTitle = "audio upload error"
      modalContents = html.Pre(get_exception_traceback_str(e))

   return modalOpen, modalContents, data





 # data = contents.encode("utf8").split(b";base64,")[1]
    # filename = os.path.join(projectDirectory, name)
    # if not filename[-4:] == ".wav" and not filename[-4:] == ".WAV":
    # 	sound_validationMessage = "Please select a WAVE (.wav) file."
    # 	return sound_validationMessage, "", 1
    # with open(filename, "wb") as fp:
    #    fp.write(base64.decodebytes(data))
    #    fileSize = os.path.getsize(filename)
    #    errorMessage = ""
    #    validSound = True
    #    try:
    #       rate, mtx = wavfile.read(filename)
    #    except ValueError as e:
    #       print("exeption in wavfile: %s" % e)
    #       rate = -1
    #       validSound = False
    #       errorMessage = str(e)
    #    print("sound file size: %d, rate: %d" % (fileSize, rate))
    #    if validSound:
    #    	  sound_validationMessage = "Sound file: %s (%d bytes)" % (name, fileSize)
    #    	  newButtonState = 0
    #    	  return sound_validationMessage, filename, newButtonState
    #    else:
    #    	  if "Unsupported bit depth: the wav file has 24-bit data" in errorMessage:
    #            sound_validationMessage = "File %s (%d byes) has 24-bit data, must be minimum 32-bit."  % (name, fileSize)
    #    	  else:
    #            sound_validationMessage = "ERROR: %s [File: %s (%d bytes)]" % (errorMessage, name, fileSize)
    #    	  newButtonState = 1
    
