from slexil.eafParser import EafParser
eafFiles = os.listdir("eafs/")
eafFiles.sort()

analyzeEafDiv = html.Div(id="analyzeEafDiv",
     children=[dcc.Dropdown(eafFiles, id='eafFileSelector',
              style={"fontSize": "24px", "width": "500px", "marginLeft": "30px"})])
     
dashApp.layout.children.append(analyzeEafDiv)

@callback(
    Output('memoryStore', 'data', allow_duplicate=True),
    Output('slexilModal', 'is_open', allow_duplicate=True),
    Output('modalTitle', 'children', allow_duplicate=True),
    Output('modalContents', 'children', allow_duplicate=True),
    Input('eafFileSelector', 'value'),
    State('memoryStore', 'data'),
    prevent_initial_call=True)
def analyzeEAF(filename, data):
   print("entering analyzeEAF callback")
   filename = os.path.join("eafs", filename)
   parser = EafParser(filename, verbose=False, fixOverlappingTimeSegments=False)
   el = html.Ul(id="eafAttributes", children=[]);
   if data is None:
      data = {}

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

   return data, True, "Analysis of %s" % filename, el
   



