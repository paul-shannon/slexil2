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

   #f = "../testData/validYamlFiles/inferno-heterogeneousTiers.yaml"
   #f = "../testData/validYamlFiles/inferno-noAnalysisTiers.yaml"
   #f = "../testData/validYamlFiles/inferno-1-line.yaml"
   f = "../testData/validYamlFiles/inferno-2-lines.yaml"
   gtf = "../testData/validYamlFiles/infernoTerms.txt"
   with open(gtf) as file:
      grammaticalTerms = file.read().split("\n")
      count = len(grammaticalTerms)
      if grammaticalTerms[count-1] == "":
         grammaticalTerms.pop()
   text = YamlToText(f, grammaticalTerms,
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

   filename = "inferno.html"
   f = open(filename, "wb")
   f.write(bytes(htmlText, "utf-8"))
   #f.write(bytes(htmlText_indented, "utf-8"))
   f.close()
   print("    wrote %s" % f.name)

#--------------------------------------------------------------------------------
def test_harryMosesDaylight():

   print("--- test_harryMosesDaylight")

   f = "../testData/validYamlFiles/daylight-3lines.yaml"
   gtf = "../explore/lushootseed/harryMoses/daylight-prosody/grammaticalTerms.txt"

   with open(gtf) as file:
      grammaticalTerms = file.read().split("\n")
      count = len(grammaticalTerms)
      if grammaticalTerms[count-1] == "":
         grammaticalTerms.pop()
   text = YamlToText(f, grammaticalTerms,
                     projectDirectory="tmp",
                     verbose = True,
                     fontSizeControls = True,
                     startLine = None,
                     endLine = None,
                     pageTitle = "Harry Moses - How Daylight Was Stolen",
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

   filename = "daylight.html"
   f = open(filename, "wb")
   f.write(bytes(htmlText, "utf-8"))
   #f.write(bytes(htmlText_indented, "utf-8"))
   f.close()
   print("    wrote %s" % f.name)

#--------------------------------------------------------------------------------
def test_tlingitVideoVanRescue():

   print("--- test_tlingitVideoVanRescue")

   f = "../testData/validYamlFiles/tlingitVan-2lines.yaml"

   gtf = None
   grammaticalTerms = []

   if(not gtf is None):
      with open(gtf) as file:
         grammaticalTerms = file.read().split("\n")
         count = len(grammaticalTerms)
         if grammaticalTerms[count-1] == "":
            grammaticalTerms.pop()

   text = YamlToText(f, grammaticalTerms,
                     projectDirectory="tmp",
                     verbose = True,
                     fontSizeControls = True,
                     startLine = None,
                     endLine = None,
                     pageTitle = "Tlingit - Van Rescue",
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

   filename = "tlingit.html"
   f = open(filename, "wb")
   f.write(bytes(htmlText, "utf-8"))
   #f.write(bytes(htmlText_indented, "utf-8"))
   f.close()
   print("    wrote %s" % f.name)

#--------------------------------------------------------------------------------
def runTests():

   test_infernoSimple()
   test_harryMosesDaylight()
   test_tlingitVideoVanRescue()

#--------------------------------------------------------------------------------
if __name__ == '__main__':
    runTests()
