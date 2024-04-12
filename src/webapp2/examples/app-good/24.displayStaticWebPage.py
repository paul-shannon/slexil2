import flask
import os, io, traceback, time
from dash import html, Dash, callback, dcc, Input, Output, State, dash_table

styleSheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = flask.Flask(__name__)
dashApp = Dash(__name__, server=app, url_base_pathname='/',
                external_stylesheets=styleSheets)

dashApp.title = "iFrame test"


@app.route('/PROJECTS/<path:urlpath>')
def serveFile(urlpath):
    print("=== entering serveFile app.server.route: %s" % urlpath)
    fullPath = os.path.join("PROJECTS", urlpath)
    dirname = os.path.dirname(fullPath)
    filename = os.path.basename(fullPath)
    print("---- %s" % fullPath)

    if urlpath[-4:] == "html":
        print("=== populate textArea from %s" % urlpath)
        return flask.send_file(os.path.join(fullPath))
    #if urlpath[-3:] == 'zip':
    #    print("=== serve_static_file")
    #    print("urlpath:  %s" % urlpath)
    #    print("about to send %s, %s" % (dirname, filename))
    #    return flask.send_file(fullPath,
    #                           mimetype='application/zip',
    #                           as_attachment=True)
    return None

buttonStyle = {"margin": "20px",
              "fontSize": "20px",
              "border": "1px solid brown",
              "borderRadius": "10px"
              }

#--------------------------------------------------------------------------------
dashApp.layout = html.Div(id="mainDiv",
                children=[html.Button("Display", id="displayStaticHTMLButton",
                                      n_clicks=0, style=buttonStyle),
                          html.Button("Download Web Page", id="downloadWebPageButton",
                                      n_clicks=0, style=buttonStyle),
                          dcc.Download(id="downloader"),
                          html.Iframe(id="htmlPreviewDiv",
                                     style={"width": "95%", "height": "800px",
                                            "overflow": "auto"})
                         ])
#--------------------------------------------------------------------------------
@callback(
    Output('htmlPreviewDiv', 'src'),
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
