from slexil.eafParser import EafParser
eafFiles = os.listdir("eafs/")
eafFiles.sort()

analyzeEafDiv = html.Div(id="analyzeEafDiv",
     children=[dcc.Dropdown(eafFiles, id='eafFileSelector',
              style={"fontSize": "24px", "width": "500px"})])
     
dashApp.layout.children.append(analyzeEafDiv)

@callback(
    Output('slexilModal', 'is_open', allow_duplicate=True),
    Output('modalTitle', 'children', allow_duplicate=True),
    Output('modalContents', 'children', allow_duplicate=True),
    Input('eafFileSelector', 'value'),
    prevent_initial_call=True)
def analyzeEAF(filename):
   print("entering analyzeEAF callback")
   filename = os.path.join("eafs", filename)
   parser = EafParser(filename, verbose=False, fixOverlappingTimeSegments=False)
   el = html.Ul(id="eafAttributes",
      children=[html.Li("line count: %d" % parser.getLineCount())
      ])
   return True, "Analysis of %s" % filename, el
   



