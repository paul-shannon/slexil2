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
argParser = argparse.ArgumentParser()
argParser.add_argument("--eaf", help="the ELAN XML file")
argParser.add_argument("--terms", help="grammatical categories to capitalize")
helpText = "e.g, speech, translation, morpheme,morphemeGloss, ..."
argParser.add_argument("--tierGuide",help=helpText)
argParser.add_argument("--projectDirectory", help="where to write html file")
argParser.add_argument("--verbose", help="verbose stdout reporting",
					   action="store_true")
argParser.add_argument("--startLine", help="optional start line")
argParser.add_argument("--endLine", help="optional end line")
argParser.add_argument("--addFontSizeControls", help="text font size +/-",
					   action="store_true")
argParser.add_argument("--kb", help="a knowledge base file")
argParser.add_argument("--linguistics",
					   help="a linguistics knowledge base file")
 
args = argParser.parse_args()

elanXmlFilename = vars(args)["eaf"]
grammaticalTermsFile = vars(args)["terms"]
tierGuideFile = vars(args)["tierGuide"]
projectDirectory = vars(args)["projectDirectory"]
verbose = vars(args)["verbose"]
startLine = vars(args)["startLine"]
endLine = vars(args)["endLine"]
kbFilename = vars(args)["kb"]
linguisticsFilename = vars(args)["linguistics"]

if(startLine != None):
	startLine = int(startLine)
if(endLine != None):
	endLine = int(endLine)
fontSizeControls = vars(args)["addFontSizeControls"]

text = Text(elanXmlFilename, grammaticalTermsFile, tierGuideFile,
			projectDirectory, verbose, fontSizeControls, startLine, endLine,
			kbFilename, linguisticsFilename)

print(text.getTierSummary())
htmlText = text.toHTML()
htmlText_indented = indent(htmlText)

filename = "index.html"
f = open(filename, "wb")
f.write(bytes(htmlText_indented, "utf-8"))
f.close()
print("wrote %s" % f.name)
