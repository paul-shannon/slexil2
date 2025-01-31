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

if not len(sys.argv) == 2:
    print("usage: python eaf2sfmt2html.py <eafFile> or <listOfEafFiles.txt>")
    sys.exit(1)

filename = sys.argv[1]
assert(os.path.exists(filename))
baseName = os.path.splitext(os.path.basename(filename))[0]
extension = os.path.splitext(os.path.basename(filename))[1]
if extension == '.txt':
   with open(filename) as f:
      eafFiles = f.read().splitlines()
      eafFiles = [f for f in eafFiles if not f.startswith("#")]
      #eafFiles = f.readlines()
else:
    eafFiles = [filename]

for eafFile in eafFiles:
   try:
      print("\n\n-----------------------------------------------------------")
      print("    %s" % eafFile)
      baseName = os.path.splitext(os.path.basename(eafFile))[0]
      tats = extractAllTimeAlignedTierIDs(eafFile)
      tatsString = ", ".join(map(str, tats))
      print("tats found: %s" % tatsString)
      if len(tats) != 1:
          continue
      p = EafParser(eafFile, verbose=False, fixOverlappingTimeSegments=False)
      p.run()
      print("-----------------------------------------------------------------")
      print(p.getRichTierTables()[0])
      print()
      print(p.getRichTierTables()[1])
      print("-----------------------------------------------------------------")
      tbl = p.getTierTable()
      text = p.toSFMT("title", "speaker", "transcriber")
      yamlOutFile = "testRuns/%s.yaml" % baseName
      p.writeSFMT(text, yamlOutFile)
      projectDirectory = "./"
      text = sfmtToWebPage(yamlOutFile,
                           grammaticalTerms=[],
                           projectDirectory=projectDirectory,
                           verbose = False,
                           fontSizeControls = True,
                           startLine = None,
                           endLine = None,
                           pageTitle = baseName,
                           helpFilename = None,
                           helpButtonLabel = None,
                           kbFilename = None,
                           linguisticsFilename = None,
                           fixOverlappingTimeSegments = False,
                           webpackLinksOnly=False,
                           useTooltips=False)
      htmlText = text.toHTML()
      htmlFileName = "testRuns/%s.html" % baseName
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

