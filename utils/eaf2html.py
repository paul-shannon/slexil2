import argparse
import os, sys
import unittest
from slexil.text import Text
import yattag  # only for indent method
import pdb
    
#----------------------------------------------------------------------------------------------------
parser = argparse.ArgumentParser(prog='eaf2html.py',
          description='creates interactive webpage from eaf xml')

#parser.add_argument('-f', '--eaf')
parser.add_argument('--eaf', type=str, required=True)
parser.add_argument('--tierGuide', type=str, required=True)
parser.add_argument('--terms', type=str, required=False)
parser.add_argument("--verbose", action="store_true")
parser.add_argument("--helpFile", help="optional info for about box")
parser.add_argument("--helpButtonLabel", help="optional button label")
parser.add_argument("--pageTitle", help="optional html title")
parser.add_argument('--start', type=int, required=False, default=None)
parser.add_argument('--end', type=int, required=False, default=None)
parser.add_argument('--webpackLinksOnly',  action="store_true")
parser.add_argument('--fontSizeControls',  action="store_true")
parser.add_argument('--kbFilename', required=False, default=None)
parser.add_argument('--linguisticsFilename', required=False, default=None)
parser.add_argument('--fixOverlappingTimeSegments', action="store_true")
parser.add_argument('--toolTips', action="store_true")


args = parser.parse_args()
print(args)
eaf = args.eaf
tierGuide = args.tierGuide
terms = args.terms
helpFile = args.helpFile
helpButtonLabel = args.helpButtonLabel
verbose = args.verbose
startLine = args.start
endLine = args.end
pageTitle = args.pageTitle
webpackLinksOnly = args.webpackLinksOnly
fontSizeControls = args.fontSizeControls
kbFilename = args.kbFilename
linguisticsFilename = args.linguisticsFilename
fixOverlappingTimeSegments = args.fixOverlappingTimeSegments
useTooltips = args.toolTips
#----------------------------------------------------------------------------------------------------
if(not os.path.isfile(eaf)):
    print("eaf2html.py error: eaf file '%s' not found" % eaf)
    sys.exit()

if(not os.path.isfile(tierGuide)):
    print("eaf2html.py error: tierGuidefile '%s' not found" % tierGuide)
    sys.exit()
    
if(terms and not os.path.isfile(terms)):
    print("eaf2html.py error: grammaticalTerms file '%s' not found" % terms)
    sys.exit()
    
if(linguisticsFilename and not os.path.isfile(linguisticsFilename)):
    print("eaf2html.py error:  file '%s' not found" % linguisticsFilename)
    sys.exit()
    
print("verbose? %s" % verbose)
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
            helpButtonLabel = helpButtonLabel,
            kbFilename = kbFilename,
            linguisticsFilename = linguisticsFilename,
            webpackLinksOnly = webpackLinksOnly,
            fixOverlappingTimeSegments = fixOverlappingTimeSegments,
            useTooltips=useTooltips)
	
htmlText = text.toHTML()
filename = "index.html"
f = open(filename, "wb")
f.write(bytes(htmlText, "utf-8"))
f.close()
print("wrote %s" % f.name)

