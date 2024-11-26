from slexil.eafParser import EafParser
# eafFiles = os.listdir("eafs/")
# eafFiles.sort()

analyzeEafDiv = html.Div(id="analyzeEafDiv",
     children=[dcc.Dropdown(eafFiles, id='eafFileSelector',
              style={"fontSize": "24px", "width": "500px"})])
     

@callback(
    Output('memoryStore', 'data', allow_duplicate=True),
    Output('slexilModal', 'is_open', allow_duplicate=True),
    Output('modalTitle', 'children', allow_duplicate=True),
    Output('modalContents', 'children', allow_duplicate=True),
    Input('eafUploader',    'contents'),
    State('eafUploader',    'filename'),
    State('memoryStore', 'data'),
    prevent_initial_call=True)
def analyzeEAF(fileContents, filename, data):
   print("entering analyzeEAF callback")
   if data is None:
      data = {}
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
      el = html.Ul(id="eafAttributes", children=[]);
      el.children.append(html.Li("lineCount: %s" % parser.getLineCount()))
      el.children.append(html.Li("audioURL: %s" % parser.getAudioURL()))
      el.children.append(html.Li("videoURL: %s" % parser.getVideoURL()))
      timeAlignedTiers = parser.getTimeAlignedTiers()
      el.children.append(html.Li("time-aligned tiers: %s" % timeAlignedTiers))
      i = 1
      for tal in timeAlignedTiers:
         tierFamily = parser.getTimeAlignedTierFamily(tal)
         el.children.append(html.Li("  tier group %d: %s" % (i, tierFamily)))
         i += 1
       modalOpen = True
       modalContents = el
       modalTitle = "%s info" % data['projectName']
   except BaseException as e:
      modalOpen = True
      modalTitle = "eaf error"
      modalContents = html.Pre(get_exception_traceback_str(e))

   return data, modalOpen, modalTitle, modalContents
   
#--------------------------------------------------------------------------------
dashApp.layout.children.append(analyzeEafDiv)


