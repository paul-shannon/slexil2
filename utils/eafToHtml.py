# eafToHtml.py
#--------------------------------------------------------------------------------
import yaml
import pdb
import io, traceback, time
import os, sys
from slexil.eafParser import EafParser
from slexil.eafParser import extractAllTimeAlignedTierIDs
import xmlschema
from xml.etree import ElementTree as etree
from time import time
import pandas as pd
import numpy as np
pd.set_option('display.width', 1000)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
from pathlib import Path
#--------------------------------------------------------------------------------
path = Path(".")
from xmlschema.validators.exceptions import XMLSchemaValidationError;
# from slexil.yamlToText import YamlToText

if not len(sys.argv) == 2:
    print("usage: python eafToYamlToHtml.py <eafFile> or <listOfEafFiles.txt>")
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

projectDirectory = "./"

for eafFile in eafFiles:
   try:
     text = Text(xmlFilename=eaf,
                 grammaticalTermsFile=None,
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
            useTooltips=useTooltips,
            practiceFile=practiceFile)
	
htmlText = text.toHTML()
filename = "index.html"
f = open(filename, "wb")
f.write(bytes(htmlText, "utf-8"))
f.close()


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
      yaml = p.toYAML("title", "speaker", "transcriber")
      yamlFile = "%s.yaml" % baseName
      p.writeYAML(yaml, yamlFile)
      projectDirectory = "./"
      text = YamlToText(yamlFile,
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
      htmlFileName = "%s.html" % baseName
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

