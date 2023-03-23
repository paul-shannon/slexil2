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
if(len(sys.argv) != 3):
    print("usage:  eaf2html.py <elanXmlFilename> <projectName>")
    sys.exit(1)
          
elanXmlFilename = sys.argv[1] # "01RuthNora230209AT.eaf"
projectName = sys.argv[2]     # "01",  "07", etc
projectDirectory = "./"
tierGuideFile= "tierGuide.yaml"
grammaticalTermsFile="grammaticalTerms.txt"

text = Text(elanXmlFilename, audioFilename, grammaticalTermsFile, tierGuideFile,
            projectDirectory, lineNumberForDebugging=None, quiet=True)
print(text.getTierSummary())
# pdb.set_trace()
htmlText = indent(text.toHTML())
# jsText = text.getJavascript()

# tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".html", dir=".")
filename = "%s-1.html" % projectName
f = open(filename, "wb")
f.write(bytes(htmlText, "utf-8"))
f.close()
print("wrote %s" % f.name)
