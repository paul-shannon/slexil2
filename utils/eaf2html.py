import re
import sys
import slexil
from text import *
import importlib
import os
import pdb
import tempfile
import argparse
#-------------------------------------------------------------------------------
pd.set_option('display.width', 1000)
#-------------------------------------------------------------------------------
parser = argparse.ArgumentParser()
parser.add_argument("--eaf", help="the ELAN XML file")
parser.add_argument("--terms", help="grammatical categories to capitalize")
helpText = "e.g, speech, translation, morpheme,morphemeGloss, ..."
parser.add_argument("--tierGuide", help=helpText)
parser.add_argument("--projectDirectory", help="where to write html file")
parser.add_argument("--verbose", help="verbose stdout reporting", action="store_true")
parser.add_argument("--startLine", help="optional start line")
parser.add_argument("--endLine", help="optional end line")
parser.add_argument("--addFontSizeControls", help="text font size +/-",
					   action="store_true")
parser.add_argument("--helpFile", help="optional info for about box")
parser.add_argument("--helpButtonLabel")
parser.add_argument("--kb", help="a knowledge base file")
parser.add_argument("--linguistics", help="a linguistics knowledge base file")
parser.add_argument("--pageTitle", help="optional html title")
 
args = parser.parse_args()
elanXmlFilename = vars(args)["eaf"]
grammaticalTermsFile = vars(args)["terms"]
tierGuideFile = vars(args)["tierGuide"]
projectDirectory = vars(args)["projectDirectory"]
verbose = vars(args)["verbose"]
startLine = vars(args)["startLine"]
helpFilename = vars(args)["helpFile"]
helpButtonLabel = vars(args)["helpButtonLabel"]
pageTitle = vars(args)["pageTitle"]
endLine = vars(args)["endLine"]
kbFilename = vars(args)["kb"]
linguisticsFilename = vars(args)["linguistics"]

if(startLine != None):
	startLine = int(startLine)
if(endLine != None):
	endLine = int(endLine)
fontSizeControls = vars(args)["addFontSizeControls"]

text = Text(elanXmlFilename,
            grammaticalTermsFile,
            tierGuideFile,
            projectDirectory,
            verbose,
            fontSizeControls,
            startLine,
            endLine,
            pageTitle,
            helpFilename,
            helpButtonLabel,
            kbFilename,
            linguisticsFilename)

print(text.getTierSummary())
htmlText = text.toHTML()
htmlText_indented = indent(htmlText)

filename = "index.html"
f = open(filename, "wb")
f.write(bytes(htmlText_indented, "utf-8"))
f.close()
print("wrote %s" % f.name)
