import re
import sys
sys.path.append("/Users/paul/github/slexil2/slexil")
from text import *
import importlib
import os
import pdb
import tempfile
import argparse
#----------------------------------------------------------------------------------------------------
pd.set_option('display.width', 1000)
#----------------------------------------------------------------------------------------------------
argParser = argparse.ArgumentParser()
argParser.add_argument("--eaf", help="the ELAN XML file")
argParser.add_argument("--terms", help="grammatical categories to capitalize")
argParser.add_argument("--tierGuide", help="e.g, speech, translation, morpheme, morphemeGloss, ...")
argParser.add_argument("--projectDirectory", help="where to write html file")
argParser.add_argument("--quiet", help="verbose stdout reporting", action="store_true")
argParser.add_argument("--startLine", help="optional start line")
argParser.add_argument("--endLine", help="optional end line")
argParser.add_argument("--addFontSizeControls", help="text font size +/-", action="store_true")

args = argParser.parse_args()

elanXmlFilename = vars(args)["eaf"]
grammaticalTermsFile = vars(args)["terms"]
tierGuideFile = vars(args)["tierGuide"]
projectDirectory = vars(args)["projectDirectory"]
quiet = vars(args)["quiet"]
startLine = int(vars(args)["startLine"])
endLine = int(vars(args)["endLine"])
fontSizeControls = vars(args)["addFontSizeControls"]

text = Text(elanXmlFilename, grammaticalTermsFile, tierGuideFile,
            projectDirectory, quiet, fontSizeControls, startLine, endLine)
print(text.getTierSummary())
htmlText = text.toHTML()
htmlText_indented = indent(htmlText)

filename = "index.html"
f = open(filename, "wb")
f.write(bytes(htmlText_indented, "utf-8"))
f.close()
print("wrote %s" % f.name)
