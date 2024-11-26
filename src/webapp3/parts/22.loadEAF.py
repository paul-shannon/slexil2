uploaderStyle = {'width': '60%',
                 'height': '60px',
                 'lineHeight': '60px',
                 'borderWidth': '1px',
                 'borderStyle': 'solid',
                 'borderRadius': '5px',
                 'textAlign': 'center',
                 'fontSize': '24px',
                 'margin': '10px',
                 'marginLeft': '100px',
                 'display': 'none'
                 }

simpleTextDisplayStyle = {'fontSize': '32px',
                          'marginLeft': '200px'
                          }

mainTextLoaderDiv = html.Div(id="mainTextLoaderDiv",
                        children = [
                           dcc.Upload(
                              id='mainTextUploader',
                              children=html.Div([
                                 'Drag and Drop or ',
                                 html.A('Select File')
                                 ]), #className="mainTextUploader"),
                              style=uploaderStyle,
                              multiple=False
                              )])

dashApp.layout.children.append(mainTextLoaderDiv)
#--------------------------------------------------------------------------------
@callback(
   Output('slexilModal',      'is_open',  allow_duplicate=True),
   Output('modalContents',    'children', allow_duplicate=True),
   Output('globals',          'data',     allow_duplicate=True),
   #Output('termsUploadYesNoDiv', 'hidden'),
   Input('mainTextUploader',  'contents'),
   State('mainTextUploader',  'filename'),
   State('globals',           'data'),
   prevent_initial_call=True)
def mainTextUploadHandler(fileContents, filename, globals):

   globals['eafFileName'] = filename

   try:
      fileData = fileContents.encode("utf8").split(b";base64,")[1]
      fullPath = os.path.join(globals['projectPath'], filename)
      with open(fullPath, "wb") as fp:
         fp.write(base64.decodebytes(fileData))
      assert(os.path.isfile(fullPath))
      fileSize = os.path.getsize(fullPath)
      globals['eafFullPath'] = fullPath
      globals['fileSize'] = fileSize
      parser = EafParser(fullPath, verbose=True, fixOverlappingTimeSegments=False)
      taTierCount = len(parser.getTimeAlignedTiers())
      if taTierCount > 1:
         msg = "Found %d time-aligned tiers.  slexil currently supports only one." % taTierCount
         raise ValueError(msg)
      globals['audioURL'] = parser.getAudioURL()
      globals['videoURL'] = parser.getVideoURL()
      if globals['videoURL'] is None:
         globals['mediaType'] = "audio"
      else:
         globals['mediaType'] = "video"
      parser.xmlValid()
      tbl_tiers = parser.getTierTable()
        # discard the DEFAULT_LOCALE column
      tbl_tiers = tbl_tiers[["TIER_ID", "LINGUISTIC_TYPE_REF", "PARENT_REF", "TIME_ALIGNABLE"]]
      dashTable_tiers = dash_table.DataTable(tbl_tiers.to_dict('records'),
                                             [{"name": i, "id": i} for i in tbl_tiers.columns],
                                             style_cell={'fontSize':20, 'font-family':'courier'})
      print("--- build tier table")
      tierTableDiv = html.Div(id="tierTable",
                              children=[dashTable_tiers],
                                  style = {"width": "95%", "margin": "20",
                                           "overflow": "auto",
                                           "padding": "6px",
                                           "border": "1px solid gray",
                                           "border-radius": "10px"})

      globals['tiers'] = tierTableDiv
      modalOpen = False
      modalContents = tierTableDiv
      modalTitle = "EAF Tiers"
      termsUploadYesNoDivHidden = False
      #hideCreateWebpageButton = False
   except BaseException as e:
      modalOpen = True
      modalTitle = "eaf error"
      modalContents = html.Pre(get_exception_traceback_str(e))
      termsUploadYesNoDivHidden = True
   return modalOpen, modalContents, globals
      

