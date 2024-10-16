import base64
from slexil.eafParser import EafParser

#--------------------------------------------------------------------------------
# the webapp requires a PROJECTS_DIRECTORY in the current working directory
# each individual project, one for each text, is created as a subdirectory here
PROJECTS_DIRECTORY = "PROJECTS"
try:
    assert(os.path.exists(PROJECTS_DIRECTORY))
except AssertionError:
    os.mkdir(PROJECTS_DIRECTORY)
#--------------------------------------------------------------------------------
eafDir = "eafs"
files = os.listdir(eafDir)
eafFiles = [f for f in files if f.endswith("eaf")]
eafFiles.sort()
print("eaf count: %d" % len(eafFiles))
#--------------------------------------------------------------------------------
def createProjectDirectory(projectName):

   path = os.path.join(PROJECTS_DIRECTORY, projectName)
   if not os.path.exists(path):
      os.mkdir(path)
   return path
      
#--------------------------------------------------------------------------------
eafModalDiv = html.Div(
    [dbc.Modal([
         dbc.ModalHeader(dbc.ModalTitle("EAF Structure",
                                        className="bodyStyle",
                                        id="eafModalTitle"),
                         close_button=True),
         dbc.ModalBody("", id='eafModalContents', className="bodyStyle")],
         id="eafModalDiv",
         centered=True,
         is_open=False,
         size="xl",    # sm, lg, xl
         fullscreen=False,
         scrollable=True
         )], className="bodyStyle")

#-------------------------------------------------------
loadWatcher = dcc.Loading(id="eafLoadWatcher", type="default",
                          children=eafModalDiv)

eafLoaderDiv = html.Div(id="eafLoaderDiv",
                        children = [dcc.Upload(
                            id='eafUploader',
                            accept=".eaf",
                            children=html.Div([
                                'Drag and Drop or ',
                                html.A('Select EAF File')
                                ], className="fubar"),
                            className="eafUploader",
                            multiple=False
                            )], style={"display": "none"})
#--------------------------------------------------------------------------------
# @callback(
#    Output('memoryStore',   'data',     allow_duplicate=True),
#    Output('eafModalDiv',   'is_open',  allow_duplicate=True),
#    Output('eafModalContents', 'children', allow_duplicate=True),
#    Input('eafUploader',    'contents'),
#    State('eafUploader',    'filename'),
#    State('memoryStore',    'data'),
#    prevent_initial_call=True)
# def eafUploadHandler(fileContents, filename, data):
#    if data is None:
#       data = {}
# 
#      # these will already have been created and assigned
#      # in the full app, by the setTitle module
# 
#    data['projectName'] = "fubar"
#    data['projectPath'] = "PROJECTS/fubar"
# 
#    data['eafFileName'] = filename
#    try:
#       fileData = fileContents.encode("utf8").split(b";base64,")[1]
#       fullPath = os.path.join(data['projectPath'], filename)
#       with open(fullPath, "wb") as fp:
#          fp.write(base64.decodebytes(fileData))
#       assert(os.path.isfile(fullPath))
#       fileSize = os.path.getsize(fullPath)
#       data['eafFullPath'] = fullPath
#       data['fileSize'] = fileSize
#       tbl_tiers = parser.getTierTable()
#         # discard the DEFAULT_LOCALE column
#       tbl_tiers = tbl_tiers[["TIER_ID", "LINGUISTIC_TYPE_REF", "PARENT_REF", "TIME_ALIGNABLE"]]
#       dashTable_tiers = dash_table.DataTable(tbl_tiers.to_dict('records'),
#                                              [{"name": i, "id": i} for i in tbl_tiers.columns],
#                                              style_cell={'fontSize':20, 'font-family':'courier'})
#       print("--- build tier table")
#       tierTableDiv = html.Div(id="tierTable",
#                                children=[dashTable_tiers],
#                                   style = {"width": "95%", "margin": "20",
#                                            "overflow": "auto",
#                                            "padding": "6px",
#                                            "border": "1px solid gray",
#                                            "border-radius": "10px"})
# 
#       modalOpen = True
#       modalContents = tierTableDiv
#       modalTitle = "EAF Tiers"
#    except BaseException as e:
#       modalOpen = True
#       modalTitle = "eaf error"
#       modalContents = html.Pre(get_exception_traceback_str(e))
#    return data, modalOpen, modalContents
#    #return data, modalOpen, modalTitle, modalContents
#       

#--------------------------------------------------------------------------------
dashApp.layout.children.append(loadWatcher)
dashApp.layout.children.append(eafLoaderDiv)
#----------------------------------------------------------------------
