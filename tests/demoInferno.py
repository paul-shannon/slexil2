import os
import unittest
from slexil.text import Text
import yattag

#----------------------------------------------------------------------------------------------------
dataDir = "../testData/inferno"
elanXmlFilename =      os.path.join(dataDir, "inferno-threeLines.eaf")
projectDirectory = "./"
tierGuideFile =        os.path.join(dataDir, "tierGuide.yaml")
grammaticalTermsFile = os.path.join(dataDir, "grammaticalTerms.txt")
fontSizeControls = False
startLine = None
endLine = None
kbFilename = None
linguisticsFilename = None

text = Text(elanXmlFilename,
			grammaticalTermsFile=grammaticalTermsFile,
			tierGuideFile=tierGuideFile,
			projectDirectory=projectDirectory,
			verbose=True,
			fontSizeControls = fontSizeControls,
			startLine = startLine,
			endLine = endLine,
			kbFilename = kbFilename,
			linguisticsFilename = linguisticsFilename)
	
htmlText = text.toHTML()
htmlText_indented = yattag.indent(htmlText)

filename = "inferno.html"
f = open(filename, "wb")
f.write(bytes(htmlText_indented, "utf-8"))
f.close()
print("wrote %s" % f.name)

