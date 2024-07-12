import argparse
import os, sys
import unittest
from slexil.textFromYaml import TextFromYaml
import yattag  # only for indent method
import pdb
    
#----------------------------------------------------------------------------------------------------
parser = argparse.ArgumentParser(prog='yaml2html.py',
          description='creates interactive webpage from eaf xml')

parser.add_argument('--yaml', type=str, required=True)
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
yaml = args.yaml
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
if(not os.path.isfile(yaml)):
    print("yaml2html.py error: yaml file '%s' not found" % yaml)
    sys.exit()

if(not os.path.isfile(tierGuide)):
    print("yaml2html.py error: tierGuidefile '%s' not found" % tierGuide)
    sys.exit()
    
if(terms and not os.path.isfile(terms)):
    print("yaml2html.py error: grammaticalTerms file '%s' not found" % terms)
    sys.exit()
    
if(linguisticsFilename and not os.path.isfile(linguisticsFilename)):
    print("yaml2html.py error:  file '%s' not found" % linguisticsFilename)
    sys.exit()
    
print("verbose? %s" % verbose)
projectDirectory = "./"


text = TextFromYaml(yaml, terms, tierGuide,
                  projectDirectory="inferno",
                  verbose = True,
                  fontSizeControls = True,
                  startLine = None,
                  endLine = None,
                  pageTitle = "inferno with markup",
                  helpFilename = None,
                  helpButtonLabel = None,
                  kbFilename = kbFilename,
                  linguisticsFilename = None,
                  fixOverlappingTimeSegments = False,
                  webpackLinksOnly=False,
                  useTooltips=False)


# print(text.getTierSummary())
htmlText = text.toHTML()
htmlText_indented = yattag.indent(htmlText)

   # 3 lines of speech, one jquery pattern

filename = "fromYaml.html"
f = open(filename, "wb")
f.write(bytes(htmlText_indented, "utf-8"))
f.close()
print("    wrote %s" % f.name)
