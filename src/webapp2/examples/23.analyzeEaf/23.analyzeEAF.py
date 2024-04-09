from slexil.eafParser import EafParser
eafFiles = os.listdir("eafs/")
eafFiles.sort()

analyzeEafDiv = html.Div(id="analyzeEafDiv",
     children=[dcc.Dropdown(eafFiles, id='eafFileSelector',
              style={"fontSize": "24px", "width": "500px"})])
     
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
   summary = parser.getSummary()
   el = html.Ul(id="eafAttributes", children=[]);
   keys = list(summary)
   keys.sort()
   if data is None:
      data = {}

   for key in keys:
      value = summary[key]
      valueType = type(value)
      if str(valueType) == "<class 'pandas.core.frame.DataFrame'>":
         value = "table"
      data[key] = value
      #pdb.set_trace()
      el.children.append(html.Li("%s: %s" % (key, value)))
   return data, True, "Analysis of %s" % filename, el
   



