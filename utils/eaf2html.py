import argparse
import os, sys
import unittest
from slexil.text import Text
import yattag  # only for indent method
import pdb
    
#----------------------------------------------------------------------------------------------------
parser = argparse.ArgumentParser(prog='toHTML.py',
          description='creates interactive webpage from eaf xml')

#parser.add_argument('-f', '--eaf')
parser.add_argument('--eaf', type=str, required=True)
parser.add_argument('--tierGuide', type=str, required=True)
parser.add_argument('--terms', type=str, required=False)
parser.add_argument('--verbose', type=str, required=False, default=False)
parser.add_argument("--helpFile", help="optional info for about box")
parser.add_argument("--helpButtonLabel", help="optional button label")
parser.add_argument("--pageTitle", help="optional html title")
parser.add_argument('--start', type=int, required=False, default=None)
parser.add_argument('--end', type=int, required=False, default=None)
parser.add_argument('--webpackLinksOnly',  action="store_true")
parser.add_argument('--fontSizeControls',  action="store_true")
parser.add_argument('--kbFilename', required=False, default=None)
parser.add_argument('--linguisticsFilename', required=False, default=None)

linguisticsFilename = None

args = parser.parse_args()
print(args)
eaf = args.eaf
tierGuide = args.tierGuide
terms = args.terms
helpFile = args.helpFile
helpButtonName = args.helpButtonLabel
verbose = args.verbose
startLine = args.start
endLine = args.end
pageTitle = args.pageTitle
webpackLinksOnly = args.webpackLinksOnly
fontSizeControls = args.fontSizeControls
kbFilename = args.kbFilename
linguisticsFilemane = args.linguisticsFilename
#----------------------------------------------------------------------------------------------------
if(not os.path.isfile(eaf)):
    print("toHTML.py error: eaf file '%s' not found" % eaf)
    sys.exit()

if(not os.path.isfile(tierGuide)):
    print("toHTML.py error: tierGuidefile '%s' not found" % tierGuide)
    sys.exit()
    
if(terms and os.path.isfile(terms)):
    print("toHTML.py error: grammaticalTerms file '%s' not found" % terms)
    sys.exit()
    
projectDirectory = "./"
text = Text(xmlFilename=eaf,
            grammaticalTermsFile=terms,
            tierGuideFile=tierGuide,
            projectDirectory=projectDirectory,
            verbose=verbose,
            fontSizeControls = fontSizeControls,
            startLine = startLine,
            endLine = endLine,
            pageTitle = pageTitle,
            helpFilename = helpFile,
            helpButtonLabel = "About",
            kbFilename = kbFilename,
            linguisticsFilename = linguisticsFilename,
            webpackLinksOnly = webpackLinksOnly,
            fixOverlappingTimeSegments = False)
	
htmlText = text.toHTML()
filename = "index.html"
f = open(filename, "wb")
f.write(bytes(htmlText, "utf-8"))
f.close()
print("wrote %s" % f.name)

