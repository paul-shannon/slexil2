import re
import sys
sys.path.append("/Users/paul/github/slexil2/slexil")
from text import *
import importlib
import os
import pdb
import tempfile
#----------------------------------------------------------------------------------------------------
pd.set_option('display.width', 1000)
#----------------------------------------------------------------------------------------------------
audioFilename = "audio/daylight.wav"
elanXmlFilename ="beckAndHess.eaf"
projectDirectory = "dist"
tierGuideFile= "tierGuide.yaml"
grammaticalTermsFile="grammaticalTerms.txt"

text = Text(elanXmlFilename, audioFilename, grammaticalTermsFile, tierGuideFile,
            projectDirectory, quiet=True)
text.getTierSummary()

htmlText = indent(text.toHTML())
# jsText = text.getJavascript()

f = open("beckAndHess0.html", "wb")
f.write(bytes(htmlText, "utf-8"))
f.close()
print("wrote %s" % f.name)
