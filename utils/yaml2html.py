import argparse
import os, sys
import unittest
from pathlib import Path
#from slexil.textFromYaml import TextFromYaml

from slexil.yamlToText import YamlToText
from slexil.morphemeGlossAbbreviations import MorphemeGlossAbbreviations

import yattag  # only for indent method
import pdb
    
#----------------------------------------------------------------------------------------------------
parser = argparse.ArgumentParser(prog='yaml2html.py',
          description='creates interactive webpage from eaf xml')

parser.add_argument('--yaml', type=str, required=True)
parser.add_argument('--tierGuide', type=str, required=False)
# parser.add_argument('--terms', type=str, required=False)
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
yaml = args.yaml
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
if(not os.path.isfile(yaml)):
    print("yaml2html.py error: yaml file '%s' not found" % yaml)
    sys.exit()

if(tierGuide and not os.path.isfile(tierGuide)):
    print("yaml2html.py error: tierGuidefile '%s' not found" % tierGuide)
    sys.exit()
    
#if(grammaticalTerms and not os.path.isfile(grammaticalTerms)):
#    print("yaml2html.py error: grammaticalTerms file '%s' not found" % grammaticalTerms)
#    sys.exit()
    
if(linguisticsFilename and not os.path.isfile(linguisticsFilename)):
    print("yaml2html.py error:  file '%s' not found" % linguisticsFilename)
    sys.exit()
    
print("verbose? %s" % verbose)
# pdb.set_trace()
projectDirectory = "./"
mga = MorphemeGlossAbbreviations()

text = YamlToText(yaml,
                  grammaticalTerms=mga.getAll(),
                  projectDirectory=projectDirectory,
                  verbose = verbose,
                  fontSizeControls = True,
                  startLine = None,
                  endLine = None,
                  pageTitle = pageTitle,
                  helpFilename = helpFile,
                  helpButtonLabel = helpButtonLabel,
                  kbFilename = kbFilename,
                  linguisticsFilename = linguisticsFilename,
                  fixOverlappingTimeSegments = False,
                  webpackLinksOnly=False,
                  useTooltips=False)



# text = TextFromYaml(yaml, terms, tierGuide,
#                   projectDirectory=projectDirectory,
#                   verbose = verbose,
#                   fontSizeControls = fontSizeControls,
#                   startLine = startLine,
#                   endLine = endLine,
#                   pageTitle = pageTitle,
#                   helpFilename = helpFile,
#                   helpButtonLabel = helpButtonLabel,
#                   kbFilename = kbFilename,
#                   linguisticsFilename = linguisticsFilename,
#                   fixOverlappingTimeSegments = fixOverlappingTimeSegments,
#                   webpackLinksOnly=webpackLinksOnly,
#                   useTooltips=useTooltips)


# print(text.getTierSummary())
htmlText = text.toHTML()
#htmlText_indented = yattag.indent(htmlText)

   # 3 lines of speech, one jquery pattern

#filename = "index.html"
filename = "%s/%s.html" % (outputDir, Path(yaml).stem)
f = open(filename, "wb")
f.write(bytes(htmlText, "utf-8"))
#f.write(bytes(htmlText_indented, "utf-8"))
f.close()
print("    wrote %s" % f.name)
