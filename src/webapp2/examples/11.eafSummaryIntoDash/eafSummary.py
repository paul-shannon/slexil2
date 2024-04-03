from dash import html, Dash, callback, dcc, Input, Output, State, dash_table
from slexil.eafParser import EafParser
app = Dash(external_stylesheets=[])
buttonStyle={"margin": "10px", "padding": "20px"}

app.layout = html.Div(id="mainDiv",
                      children=[html.H1('SLEXIL EAF Parsing Demo'), 
                       html.Button("Summarize EAF", id="summarizeEafButton", n_clicks=0, style=buttonStyle),
                       html.Div(id="summaryDiv", children=[])
                       ],
    style={"margin": "50px"})
#----------------------------------------------------------------------
@callback(
    Output('summaryDiv', 'children', allow_duplicate=True),
    Input('summarizeEafButton', 'n_clicks'),
    prevent_initial_call=True
    )
def summarizeEaf(n_clicks):
    f = "inferno-threeLines.eaf"
    parser = EafParser(f, verbose=True, fixOverlappingTimeSegments=False)
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
                            style = {"width": "95t", "margin": "20",
                                     "margin-top": "40px",
                                     "padding": "6px",
                                     "overflow": "auto",
                                     "border": "1px solid gray",
                                     "border-radius": "10px"})
                            
    return [tierTableDiv, lineTableDiv]
    
#----------------------------------------------------------------------
if __name__ == '__main__':
    port = 9014
    app.run(host='0.0.0.0', debug=True, port=port)

    
