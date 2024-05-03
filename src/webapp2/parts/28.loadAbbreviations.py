# good example here:
#  https://community.plotly.com/t/show-and-tell-dash-uploader-upload-large-files/38451/51?page=3
#  https://stackoverflow.com/questions/75194431/dash-dcc-upload-component-for-large-file

import dash_uploader as du
import shutil

termsFileUploadYesNoDiv = html.Div(id="termsUploadYesNoDiv",
              style={"margin-left": "20px", "display": "inline-block",
                     "padding-bottom": "0px"},
              children=[
                 html.Div(html.Label("Upload grammatical abbreviations file?",
                            style={"font-size": "24px",
                                   "font-family": "New York Times-Roman"}),
                          style={"display": "inline-block"}),
                 html.Div(
                     dcc.RadioItems(id="termsUploadYesNoButton",
                                    options=[' Yes', ' No'],
                                    #value=' No',
                                    className="radioButtonsClass",
                                    labelStyle = {'display': 'inline',
                                                  'cursor': 'pointer',
                                                  'margin-left':'20px',
                                                  "font-size": "24px",
                                                  "font-family": "New York Times-Roman"}),
                          style={"display": "inline-block"}),
                 ], hidden=True)
dashApp.layout.children.append(termsFileUploadYesNoDiv)
#---------------------------------------------------------------------
termsLoaderDiv = html.Div(id="termsUploadDiv",
                          children=[dcc.Upload(
                              id='termsUploader',
                              #filetypes=["wav", "WAV"],
                            children=html.Div([
                                'Drag and Drop or ',
                                html.A('Select Abbreviations File')
                                ], className="fubar"),
                            className="eafUploader",
                            multiple=False
                            )],hidden=True)

dashApp.layout.children.append(termsLoaderDiv)
#--------------------------------------------------------------------------------
@callback(
   Output('termsUploadDiv',        'hidden', allow_duplicate=True),
   Output('createWebPageDiv',      'hidden', allow_duplicate=True),
   Output('audioUploadYesNoDiv',   'hidden', allow_duplicate=True),
   Input('termsUploadYesNoButton', 'value'),
   State('memoryStore',            'data'),
   prevent_initial_call=True)
def termsYesNoHandler(uploadYesNo, data):
    print("uploadYesNo: %s" % uploadYesNo)
    if uploadYesNo == ' Yes':
       createWebPageDivHidden = True
       termsUploaderDivHidden = False
       createWebPageDivHidden = True
       audioUploadYesNoHidden = True
    else:
       termsUploaderDivHidden = True
       if data['mediaType'] == "audio":
          createWebPageDivHidden = True
          audioUploadYesNoHidden = False
       else:
          audioUploadYesNoHidden = True
          createWebPageDivHidden = False
    return termsUploaderDivHidden, createWebPageDivHidden, audioUploadYesNoHidden

#--------------------------------------------------------------------------------
@callback(
   Output('slexilModal',         'is_open',  allow_duplicate=True),
   Output('modalContents',       'children', allow_duplicate=True),
   Output('memoryStore',         'data',     allow_duplicate=True),
   Output('audioUploadYesNoDiv', 'hidden',   allow_duplicate=True),
   Output('createWebPageDiv',    'hidden',   allow_duplicate=True),
   Input('termsUploader',        'contents'),
   State('termsUploader',        'filename'),
   State('memoryStore',          'data'),
   prevent_initial_call=True)
def termsUploadHandler(fileContents, filename, data):

   print("=== soundUploadHandler")
   if filename is None:
       return("","",1)

   if data is None:
      data = {}

   try:
      data['termsFileName'] = filename;
      fileData = fileContents.encode("utf8").split(b";base64,")[1]
      fullPath = os.path.join(data['projectPath'], filename)
      with open(fullPath, "wb") as fp:
         fp.write(base64.decodebytes(fileData))
      assert(os.path.isfile(fullPath))
      fileSize = os.path.getsize(fullPath)
      data['termsFullPath'] = fullPath
      data['termsFileSize'] = fileSize

      modalOpen = False
      modalContents = ""
      createWebPageDivHidden = False
      audioUploadYesNoHidden = True
      if data['mediaType'] == "audio":
         print("audio, hiding cwp, showing auyn")
         createWebPageDivHidden = True
         audioUploadYesNoHidden = False
   
   except BaseException as e:
      modalOpen = True
      modalTitle = "terms upload error"
      modalContents = html.Pre(get_exception_traceback_str(e))
      createWebPageDivHidden = True

   return modalOpen, modalContents, data, audioUploadYesNoHidden, createWebPageDivHidden

