import sys
import os
sys.path.append("../../../slexil")
from text import *



audioFilename = "dummy.wav"
elanXmlFilename="7FlorenceRon230302AT.eaf"
targetDirectory = "audio"
projectDirectory="florence"
tierGuideFile="tierGuide.yaml"
grammaticalTermsFile="grammaticalTerms.txt"

text = Text(elanXmlFilename, audioFilename, grammaticalTermsFile, tierGuideFile,
            projectDirectory, quiet=True)
x = text.getTierSummary()
x = text.getMediaInfo()
   # make sure start and end times have been extracted into a pandas dataframe
times = text.determineStartAndEndTimes()
htmlText = indent(text.toHTML())

display = True;
if(display):
    filename = "florence.html"
    htmlFile = open(filename, "w")
    try:
        htmlFile.write(htmlText) #, "utf-8"))
        htmlFile.close()
    finally:
        print("opening %s in browser" % filename)
        os.system("open %s" % filename)

