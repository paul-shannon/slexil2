import argparse
import pdb
import io, traceback, time
import os, sys
from slexil.eafParser import EafParser
from slexil.eafParser import extractAllTimeAlignedTierIDs
from slexil.sfmtToWebPage import sfmtToWebPage

import xmlschema
from xml.etree import ElementTree as etree
from time import time
import pandas as pd
import numpy as np
pd.set_option('display.width', 1000)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
from pathlib import Path
path = Path(".")
from xmlschema.validators.exceptions import XMLSchemaValidationError;
from slexil.yamlToText import YamlToText

parser = argparse.ArgumentParser(prog='yaml2html.py',
          description='creates interactive webpage from eaf xml')

parser.add_argument('--eaf', type=str, required=True)
parser.add_argument('--html', type=str, required=True)
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
eaf = args.eaf
htmlFileName = args.html
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

baseName = os.path.splitext(os.path.basename(eaf))[0]
try:
   print("\n\n-----------------------------------------------------------")
   print("    %s" % eaf)
   baseName = os.path.splitext(os.path.basename(eaf))[0]
   tats = extractAllTimeAlignedTierIDs(eaf)
   tatsString = ", ".join(map(str, tats))
   print("tats found: %s" % tatsString)
   if len(tats) != 1:
       sys.exit(1)
   p = EafParser(eaf, verbose=False, fixOverlappingTimeSegments=False)
   p.run()
   print("-----------------------------------------------------------------")
   print(p.getRichTierTables()[0])
   print()
   print(p.getRichTierTables()[1])
   print("-----------------------------------------------------------------")
   tbl = p.getTierTable()
   text = p.toSFMT("title", "speaker", "transcriber")
   yamlOutFile = "%s.yaml" % baseName
   if os.path.isdir("testResults"):
      yamlOutFile = "testResults/%s.yaml" % baseName
   p.writeSFMT(text, yamlOutFile)
   projectDirectory = "./"
   text = sfmtToWebPage(yamlOutFile,
                        grammaticalTerms=[],
                        projectDirectory=projectDirectory,
                        verbose = False,
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
   htmlText = text.toHTML()
   if os.path.isdir("testResults"):
      htmlFileName = "testResults/%s.html" % htmlFileName
   print("--- writing html file for at %s" % htmlFileName)
   with open(htmlFileName, "w") as file:
       file.write(htmlText)
except Exception as e:
   print("exception occurred")
   file = io.StringIO()
   exceptionString = traceback.format_exception_only(None, e)
   tracebackString = traceback.print_exception(e, file=file)
   print(file.getvalue().rstrip())
   print()
   print(exceptionString)

