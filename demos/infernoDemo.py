from slexil.text import Text
from yattag import indent

elanXmlFilename = "inferno-threeLines.eaf"
tierGuideFile = "tierGuide.yaml"
grammaticalTermsFile = "grammaticalTerms.txt"
projectDirectory = "./"
fontSizeControls = False
startLine = None
endLine = None
kbFilename = None
linguisticsFilename = None

text = Text(elanXmlFilename,
			grammaticalTermsFile=grammaticalTermsFile,
			tierGuideFile=tierGuideFile,
			projectDirectory=projectDirectory,
			verbose=False,
			fontSizeControls = fontSizeControls,
			startLine = startLine,
			endLine = endLine,
			kbFilename = kbFilename,
			linguisticsFilename = linguisticsFilename)

htmlText = text.toHTML() 
filename = "inferno.html"
f = open(filename, "w")
f.write(indent(htmlText))
print("wrote %s" % filename)

