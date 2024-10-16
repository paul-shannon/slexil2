
myDiv = html.Div(id="myDiv",
                 children=[dcc.Dropdown(eafFiles,
                                      # 'inferno-threeLines.eaf',
                                      id='eafChooser',
                                      style={"width": "400px", "font-size": "18px"}),
                           ])

dashApp.layout.children.append(myDiv)

@callback(
    Output('slexilModal', 'is_open', allow_duplicate=True),
    Output('modalContents', 'children', allow_duplicate=True),
    Output('memoryStore', 'data', allow_duplicate=True),
    Input('eafChooser', 'value'),
    State('memoryStore', 'data'),
    prevent_initial_call=True
    )
def summarizeEaf(eafFilename, data):
    if data is None:
        data = {}
    print("--- %s" % eafFilename)
    eafFilePath = "%s/%s" % (eafDir, eafFilename)
    data['eafDir'] = eafDir
    data['eafFilename'] = eafFilename
    data['eafPath'] = eafFilePath
    try:
       parser = EafParser(eafFilePath, verbose=True, fixOverlappingTimeSegments=False)
       tbl_tiers = parser.getTierTable()
       dashTable_tiers = dash_table.DataTable(tbl_tiers.to_dict('records'),
                                              [{"name": i, "id": i} for i in tbl_tiers.columns],
                                              style_cell={'fontSize':20, 'font-family':'courier'})
       tierTableDiv = html.Div(id="tierTable",
                               children=[dashTable_tiers],
                               style = {"width": "95%", "margin": "20",
                                        "overflow": "auto",
                                        "padding": "6px",
                                        "border": "1px solid gray",
                                        "border-radius": "10px"})
       tbl_line0 = parser.getAllLinesTable()[0]
       dashTable_lines = dash_table.DataTable(tbl_line0.to_dict('records'),
                                              [{"name": i, "id": i} for i in tbl_line0.columns],
                                              style_cell={'fontSize':18, 'font-family':'courier'})
       lineTableDiv = html.Div(id="lineTable",
                               children=[dashTable_lines],
                               style = {"width": "95%", "margin": "20",
                                        "margin-top": "40px",
                                        "padding": "6px",
                                        "overflow": "auto",
                                        "border": "1px solid gray",
                                        "border-radius": "10px"})
       return True, [tierTableDiv], data
    except BaseException as e:
       success = False
       modalContents = get_exception_traceback_str(e)
       return True, html.Pre(modalContents), data


    
#----------------------------------------------------------------------
