import re
import sys
import slexil
from text import *
import pdb
pd.set_option('display.width', 1000)
import yattag
#----------------------------------------------------------------------------------------------------
packageRoot = os.path.dirname(os.path.dirname(os.path.abspath("explore_text-inferno.py")))
dataDir = os.path.join(packageRoot, "testData", "inferno")
projectDir = os.path.join(packageRoot, "tests", "tmp")
#----------------------------------------------------------------------------------------------------

elanXmlFilename =      os.path.join(dataDir, "inferno-threeLines.eaf")
projectDirectory =     projectDir
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

print(text.getTierSummary())
htmlText = text.toHTML()
htmlText_indented = yattag.indent(htmlText)

filename = "index.html"
f = open(filename, "wb")
f.write(bytes(htmlText_indented, "utf-8"))
f.close()
print("wrote %s" % f.name)



