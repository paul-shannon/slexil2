eafLoaderDiv = html.Div(id="eafLoaderDiv",
                        children = [dcc.Upload(
                            id='eafUploader',
                            #accept=".eaf",
                            children=html.Div([
                                'Drag and Drop or ',
                                html.A('Select EAF File')
                                ], className="fubar"),
                            className="eafUploader",
                            multiple=False
                            )], hidden=True)

dashApp.layout.children.append(eafLoaderDiv)
#--------------------------------------------------------------------------------
@callback(
   Output('slexilModal',      'is_open',  allow_duplicate=True),
   Output('modalContents',    'children', allow_duplicate=True),
   Output('memoryStore',      'data',     allow_duplicate=True),
   Output('audioUploadYesNoDiv', 'hidden'),
   Output('createWebPageDiv', 'hidden'),
   Input('eafUploader',       'contents'),
   State('eafUploader',       'filename'),
   State('memoryStore',       'data'),
   prevent_initial_call=True)
def eafUploadHandler(fileContents, filename, data):

   if data is None:
      data = {}

   if not filename[-4:] == '.eaf':
      modalOpen = True
      modalTitle = "Incorrect file type"
      unorderedList = html.Ul(id="list", children=[
         html.Li("Expected a file with an .eaf extension"),
         html.Li("Instead got %s" % filename)
         ])
      modalContents = unorderedList
      hideAudioUploadYesNo = True
      hideCreateWebPageDiv = True
      return modalOpen, modalContents, data, hideAudioUploadYesNo, hideCreateWebPageDiv

   data['eafFileName'] = filename

   try:
      fileData = fileContents.encode("utf8").split(b";base64,")[1]
      fullPath = os.path.join(data['projectPath'], filename)
      with open(fullPath, "wb") as fp:
         fp.write(base64.decodebytes(fileData))
      assert(os.path.isfile(fullPath))
      fileSize = os.path.getsize(fullPath)
      data['eafFullPath'] = fullPath
      data['fileSize'] = fileSize
      parser = EafParser(fullPath, verbose=True, fixOverlappingTimeSegments=False)
      taTierCount = len(parser.getTimeAlignedTiers())
      if taTierCount > 1:
         msg = "Found %d time-aligned tiers.  slexil currently supports only one." % taTierCount
         raise ValueError(msg)
      data['audioURL'] = parser.getAudioURL()
      data['videoURL'] = parser.getVideoURL()
      hideCreateWebPageDiv = True
      hideAudioUploadYesNo = True
      if data['videoURL']:
         data['mediaType'] = "video"
         hideCreateWebPageDiv = False
         hideAudioUploadYesNo = True
      else:
         data['mediaType'] = "audio"
         hideCreateWebPageDiv = True
         hideAudioUploadYesNo = False
         #audioUploadDivHidden = False
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

      data['tiers'] = tierTableDiv
      modalOpen = False
      modalContents = tierTableDiv
      modalTitle = "EAF Tiers"
      #hideCreateWebpageButton = False
   except BaseException as e:
      modalOpen = True
      modalTitle = "eaf error"
      modalContents = html.Pre(get_exception_traceback_str(e))
      hideAudioUploadYesNo = True
      hideCreateWebPageDiv = True
   return modalOpen, modalContents, data, hideAudioUploadYesNo, hideCreateWebPageDiv
      

