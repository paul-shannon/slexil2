import argparse
import os, sys
import unittest
from slexil.yamlToText import YamlToText
import yattag  # only for indent method
import pdb
import re
import yaml
import yattag
#--------------------------------------------------------------------------------
def test_infernoSimple():

   print("--- test_infernoSimple")

   f = "../testData/validYamlFiles/inferno-noAnalysisTiers.yaml"
   #f = "../testData/validYamlFiles/inferno-1-line.yaml"
   #f = "../testData/validYamlFiles/inferno-2-lines.yaml"
   ftg = None
   fgt = "../testData/validYamlFiles/infernoTerms.txt"
   text = YamlToText(f, fgt, ftg,
                     projectDirectory="inferno",
                     verbose = True,
                     fontSizeControls = True,
                     startLine = None,
                     endLine = None,
                     pageTitle = "inferno with markup",
                     helpFilename = None,
                     helpButtonLabel = None,
                     kbFilename = None,
                     linguisticsFilename = None,
                     fixOverlappingTimeSegments = False,
                     webpackLinksOnly=False,
                     useTooltips=False)


   # print(text.getTierSummary())
   htmlText = text.toHTML()
   #htmlText_indented = yattag.indent(htmlText)

   # 3 lines of speech, one jquery pattern

   filename = "index.html"
   f = open(filename, "wb")
   f.write(bytes(htmlText, "utf-8"))
   #f.write(bytes(htmlText_indented, "utf-8"))
   f.close()
   print("    wrote %s" % f.name)

#--------------------------------------------------------------------------------
def runTests():

    test_infernoSimple()
#--------------------------------------------------------------------------------
if __name__ == '__main__':
    runTests()
