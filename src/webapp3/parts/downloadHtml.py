downloadHtmlButtonDiv = html.Div(id="downloadHtmlButtonDiv",
                               style={'display': 'none'},
                               children=[html.Button('Download HTML',
                                                     id='downloadHtmlButton',
                                                     style=buttonStyle),
                                    dcc.Download(id="download-html")])

dashApp.layout.children.append(downloadHtmlButtonDiv)

#--------------------------------------------------------------------------------
@dashApp.callback(
    Output("download-html", "data"),
    Input("downloadHtmlButton", "n_clicks"),
    State("globals", "data"),
    prevent_initial_call=True,
    )
def downloadHtml(n_clicks, globals):
    print("--- 23a downloadHtml")
    
    filename = os.path.join(PROJECTS_DIRECTORY,
                            globals['projectName'],
                            "%s.html" % globals['projectName'])
    return dcc.send_file(filename)

