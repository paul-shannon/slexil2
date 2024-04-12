#--------------------------------------------------------------------------------
downloadAndDisplayDiv = html.Div(id="downloadAndDisplayDiv",
          children=[html.Button("Display", id="displayStaticHTMLButton",
                                n_clicks=0),
                    html.Button("Download Web Page", id="downloadWebPageButton",
                                n_clicks=0),
                    dcc.Download(id="downloader"),
                    html.Iframe(id="displayIFrame",
                                style={"width": "95%", "height": "800px",
                                       "overflow": "auto"})
                    ])
dashApp.layout.children.append(downloadAndDisplayDiv)
#--------------------------------------------------------------------------------
@callback(
    Output('displayIFrame', 'src'),
    Input('displayStaticHTMLButton', 'n_clicks'),
    prevent_initial_call=True
    )
def displayPage(n_clicks):
    return "http://127.0.0.1:9020/PROJECTS/example/index.html"

@callback(
    Output('downloader', 'data'),
    Input('downloadWebPageButton', 'n_clicks'),
    prevent_initial_call=True
    )
def downloadWebPage(n_clicks):
    return dcc.send_file("PROJECTS/example/index.html")

#--------------------------------------------------------------------------------
if __name__ == '__main__':
    port = 9020
    dashApp.run(host='0.0.0.0', debug=True, port=port)
