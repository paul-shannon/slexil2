# good example here:
#  https://community.plotly.com/t/show-and-tell-dash-uploader-upload-large-files/38451/51?page=3
#  https://stackoverflow.com/questions/75194431/dash-dcc-upload-component-for-large-file

import dash_uploader as du
import shutil

audioFileUploadYesNoDiv = html.Div(id="audioUploadYesNoDiv",
              style={"margin-left": "20px", #"display": "inline-block",
                     "padding-bottom": "0px"},
              children=[
                 html.Div(html.Label("Upload an audio file?",
                            style={"font-size": "24px",
                                   "font-family": "New York Times-Roman"}),
                          style={"display": "inline-block"}),
                 html.Div(
                     dcc.RadioItems(id="audioUploadYesNoButton",
                                    options=[' Yes', ' No'],
                                    className="radioButtonsClass",
                                    labelStyle = {'display': 'inline',
                                                  'cursor': 'pointer',
                                                  'margin-left':'20px',
                                                  "font-size": "24px",
                                                  "font-family": "New York Times-Roman"}),
                          style={"display": "inline-block"}),
                 ], hidden=True)
dashApp.layout.children.append(audioFileUploadYesNoDiv)
#---------------------------------------------------------------------
du.configure_upload(dashApp, "/tmp")

audioLoaderDiv = html.Div(id="audioUploadDiv",
                          children=[du.Upload(
                              id='audioUploader',
                              filetypes=["wav", "WAV"],
                              text='Drag and Drop or Select Audio File',
                              text_completed='Uploaded: ',
                              default_style={"height": "80px", "border": "0px"},
                              chunk_size=10,
                              cancel_button=True
                              )
                              ],hidden=True)
dashApp.layout.children.append(audioLoaderDiv)
#--------------------------------------------------------------------------------
@callback(
   Output('audioUploadDiv',    'hidden', allow_duplicate=True),
   Output('createWebPageDiv', 'hidden', allow_duplicate=True),
   Input('audioUploadYesNoButton', "value"),
   prevent_initial_call=True)
def audioUploadHandler(uploadYesNo):
    print("uploadYesNo: %s" % uploadYesNo)
    if uploadYesNo == ' Yes':
       createWebPageDivHidden = True
       audioUploaderDivHidden = False
    else:
       createWebPageDivHidden = False
       audioUploaderDivHidden = True
    return audioUploaderDivHidden, createWebPageDivHidden

#--------------------------------------------------------------------------------
@callback(
   Output('slexilModal',      'is_open',  allow_duplicate=True),
   Output('modalContents',    'children', allow_duplicate=True),
   Output('memoryStore',      'data',     allow_duplicate=True),
   Output('createWebPageDiv', 'hidden',   allow_duplicate=True),
   Input('audioUploader',     'isCompleted'),
   State('audioUploader',     'fileNames'),
   State('audioUploader',     'upload_id'),
   State('memoryStore',       'data'),
   prevent_initial_call=True)
def audioUploadHandler(isCompleted, fileNames, upload_id, data):

   print("=== soundUploadHandler")
   filename = fileNames[0]
   if filename is None:
       return("","",1)

   if data is None:
      data = {}

   try:
      data['audioFileName'] = filename;
      temporaryPath = "/tmp/%s/%s" % (upload_id, filename)
      projectPath = data['projectPath']
      shutil.copy2(temporaryPath, projectPath)
      modalOpen = False
      modalContents = ""
      createWebPageDivHidden = False
   
   except BaseException as e:
      modalOpen = True
      modalTitle = "audio upload error"
      modalContents = html.Pre(get_exception_traceback_str(e))
      createWebPageDivHidden = True

   return modalOpen, modalContents, data, createWebPageDivHidden

   #try:
   #   fileData = fileContents.encode("utf8").split(b";base64,")[1]
   #   fullPath = os.path.join(data['projectPath'], filename)
   #   with open(fullPath, "wb") as fp:
   #      fp.write(base64.decodebytes(fileData))
#
#      assert(os.path.isfile(fullPath))
#      fileSize = os.path.getsize(fullPath)
#      data['audioFullPath'] = fullPath
#      data['audioFileSize'] = fileSize
#      createWebPageDivHidden = False
#      #rate, mtx = wavfile.read(fullPath)
#      #data["audioSamplingRate"] = rate
#      #print(mtx)
#





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
    
