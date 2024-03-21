import base64
import os
import xmlschema
import pdb

class XmlFileUtils:
    xmlFileFullPath = None
    xmlFilename = None
    projectDirectory = None
    base64bytes = None
    schema = xmlschema.XMLSchema('http://www.mpi.nl/tools/elan/EAFv3.0.xsd')
    verbose = None
    localFilename = None  # the original is uploaded, then saved locally

    def __init__(self, filePath, projectDirectory, base64bytes, verbose=False):
       self.xmlFileFullPath = filePath
       self.xmlFilename = os.path.basename(filePath)
       self.projectDirectory = projectDirectory
       self.base64bytes = base64bytes
       self.verbose = verbose

    def saveBytesToFile(self):
       self.localFilename = os.path.join(self.projectDirectory, self.xmlFilename)
       data = self.base64bytes.encode("utf8").split(b";base64,")[1]
       with open(self.localFilename, "wb") as fp:
          fp.write(base64.decodebytes(data))
       return(self.localFilename)

    def getLocalFilename(self):
       return(self.localFilename)
   
    def validElanXML(self):
       result = {"valid": True, "details": None}
       try: 
          schemaFit = xmlschema.validate(self.localFilename, self.schema)
       except(Exception) as err:
          #print("--- exception when attempting to validate %s" % self.localFilename)
          #pdb.set_trace()
          #print(str(class(err)))
          #print(err)
          #print(str(err))
          details = "invalid xml file %s : %s" % (os.path.basename(self.localFilename), err)
          result["valid"] = False
          result["details"] = details
       return(result)
       

