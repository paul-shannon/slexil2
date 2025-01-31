import argparse
import os, sys
import unittest
from pathlib import Path

from slexil.sfmtToWebPage import sfmtToWebPage
from slexil.morphemeGlossAbbreviations import MorphemeGlossAbbreviations

import yattag  # only for indent method
import pdb
    
#----------------------------------------------------------------------------------------------------
parser = argparse.ArgumentParser(prog='yaml2html.py',
          description='creates interactive webpage from eaf xml')

parser.add_argument('--sfmt', type=str, required=True)
parser.add_argument('--tierGuide', type=str, required=False)
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
parser.add_argument('--outputDir', default="./")


args = parser.parse_args()
print(args)
sfmt = args.sfmt
tierGuide = args.tierGuide
#grammaticalTerms = args.terms
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
outputDir = args.outputDir
#----------------------------------------------------------------------------------------------------
if(not os.path.isfile(sfmt)):
    print("sfmt2html.py error: sfmt file '%s' not found" % sfmt)
    sys.exit()

if(tierGuide and not os.path.isfile(tierGuide)):
    print("sfmt2html.py error: tierGuidefile '%s' not found" % tierGuide)
    sys.exit()
    
#if(grammaticalTerms and not os.path.isfile(grammaticalTerms)):
#    print("sfmt2html.py error: grammaticalTerms file '%s' not found" % grammaticalTerms)
#    sys.exit()
    
if(linguisticsFilename and not os.path.isfile(linguisticsFilename)):
    print("sfmt2html.py error:  file '%s' not found" % linguisticsFilename)
    sys.exit()
    
print("verbose? %s" % verbose)
# pdb.set_trace()
projectDirectory = "./"
mga = MorphemeGlossAbbreviations()

page = sfmtToWebPage(sfmt, grammaticalTerms = mga.getAll(),
                     projectDirectory="inferno",
                     verbose = True,
                     fontSizeControls = True,
                     startLine = None,
                     endLine = None,
                     pageTitle = "inferno from test_sfmtToWebPage.py",
                     helpFilename = None,
                     helpButtonLabel = None,
                     kbFilename = None,
                     linguisticsFilename = None,
                     fixOverlappingTimeSegments = False,
                     webpackLinksOnly=False,
                     useTooltips=False)


htmlText = page.toHTML()

html_filename = "%s.html" % Path(sfmt).stem
f = open(html_filename, "wb")
f.write(bytes(htmlText, "utf-8"))
f.close()
print("wrote %s" % html_filename)
