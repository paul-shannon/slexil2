from slexil.eafParser import EafParser
from slexil.text import Text
import os, yaml

def createWebPage(eafFullPath, projectPath, title):

   parser = EafParser(eafFullPath, verbose=False, fixOverlappingTimeSegments=False)
   x = parser.learnTierGuide()
   print(x)
   tierGuideYamlFile = os.path.join(projectPath, "tierGuide.yaml")
   with open(tierGuideYamlFile, 'w') as outfile:
      yaml.dump(x, outfile, default_flow_style=False)
   
   text = Text(xmlFilename=eafFullPath,
               grammaticalTermsFile=None,
               tierGuideFile=tierGuideYamlFile,
               projectDirectory=projectPath,
               verbose=True,
               fontSizeControls = False,
               startLine = None,
               endLine = None,
               pageTitle = title,
               helpFilename = None,
               helpButtonLabel = "",
               kbFilename = None,
               linguisticsFilename = None,
               webpackLinksOnly = False ,
               fixOverlappingTimeSegments = False,
               useTooltips=False)
	
   filename = title.replace(" ", "_")
   filename = "%s.html" % filename
   htmlText = text.toHTML()
   filePath = os.path.join(projectPath, filename)
   print ("writing html to '%s'" % filePath)
   f = open(filePath, "wb")
   f.write(bytes(htmlText, "utf-8"))
   f.close()
   return filePath

#--------------------------------------------------------------------------------
# createWebPage("PROJECTS/x33/inferno-threeLines-outOfTimeOrder.eaf", "PROJECTS/x33", "test")
   
