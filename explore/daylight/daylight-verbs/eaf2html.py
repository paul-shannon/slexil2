import re
import sys
sys.path.append("../../../slexil")
from text import *
import importlib
import os
import pdb
import tempfile
#----------------------------------------------------------------------------------------------------
pd.set_option('display.width', 1000)
#----------------------------------------------------------------------------------------------------
audioFilename = "../daylight.wav"
elanXmlFilename ="gettingLight.eaf"
targetDirectory = "audio"
projectDirectory = "./"
tierGuideFile= "tierGuide.yaml"
grammaticalTermsFile="grammaticalTerms.txt"

text = Text(elanXmlFilename, audioFilename, grammaticalTermsFile, tierGuideFile,
            projectDirectory, lineNumberForDebugging=None, quiet=True)
print(text.getTierSummary())

htmlText = indent(text.toHTML())
# jsText = text.getJavascript()

# tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".html", dir=".")
f = open("daylight-verbs-0.html", "wb")
f.write(bytes(htmlText, "utf-8"))
f.close()
print("wrote %s" % f.name)
