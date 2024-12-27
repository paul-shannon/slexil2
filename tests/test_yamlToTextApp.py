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
from slexil.morphemeGlossAbbreviations import MorphemeGlossAbbreviations
mga = MorphemeGlossAbbreviations()
#--------------------------------------------------------------------------------
def test_infernoSimple():

   print("--- test_infernoSimple")

   #f = "../testData/validYamlFiles/inferno-heterogeneousTiers.yaml"
   #f = "../testData/validYamlFiles/inferno-noAnalysisTiers.yaml"
   #f = "../testData/validYamlFiles/inferno-1-line.yaml"
   #f = "../testData/validYamlFiles/inferno-2-lines.yaml"
   #f = "../testData/validEafYamlFiles/inferno-mixedDemo.yaml"
   f = "../testData/validEafYamlFiles/inferno-withHtmlLines.yaml"
   f = "../testData/validEafYamlFiles/inferno-mixedCaseMorphemes.yaml"

   #gtf = "../testData/validEafYamlFiles/infernoTerms.txt"
   #with open(gtf) as file:
   #   grammaticalTerms = file.read().split("\n")
   #   count = len(grammaticalTerms)
   #   if grammaticalTerms[count-1] == "":
   #      grammaticalTerms.pop()


   text = YamlToText(f, grammaticalTerms = mga.getAll(),
                     projectDirectory="inferno",
                     verbose = False,
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

   f = "../testData/validEafYamlFiles/daylight-3lines.yaml"
   gtf = "../explore/lushootseed/harryMoses/daylight-prosody/grammaticalTerms.txt"

   #with open(gtf) as file:
   #   grammaticalTerms = file.read().split("\n")
   #   count = len(grammaticalTerms)
   #   if grammaticalTerms[count-1] == "":
   #      grammaticalTerms.pop()
   text = YamlToText(f,
                     grammaticalTerms = mga.getAll(),
                     projectDirectory="tmp",
                     verbose = False,
                     fontSizeControls = True,
                     startLine = None,
                     endLine = None,
                     pageTitle = "Harry Moses - How Daylight Was Stolen",
                     helpFilename = None,
                     helpButtonLabel = None,
                     kbFilename = "/Users/paul/github/slexil2/explore/lushootseed/harryMoses/daylight-prosody/kb.js",
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
def test_lushootseedGrammar():

   print("--- test_lushootseedGrammar")

   f = "../explore/lushootseed/grammars/test.yaml"
   grammaticalTerms = []   

   text = YamlToText(f,
                     grammaticalTerms=[],
                     projectDirectory="tmp",
                     verbose = False,
                     fontSizeControls = True,
                     startLine = None,
                     endLine = None,
                     pageTitle = "Lushootseed Grammar I",
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

   filename = "grammar.html"
   f = open(filename, "wb")
   f.write(bytes(htmlText, "utf-8"))
   #f.write(bytes(htmlText_indented, "utf-8"))
   f.close()
   print("    wrote %s" % f.name)

#--------------------------------------------------------------------------------
def test_tlingitVideoVanRescue():

   print("--- test_tlingitVideoVanRescue")

   f = "../testData/validEafYamlFiles/tlingitVan-2lines.yaml"

   gtf = None

   text = YamlToText(f, grammaticalTerms=[],
                     projectDirectory="tmp",
                     verbose = False,
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
def test_aliceFromEaf():

   print("--- test_aliceFromEaf")

   f = "dontWearRed.yaml"

   text = YamlToText(f, grammaticalTerms=[],
                     projectDirectory="tmp",
                     verbose = False,
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

   filename = "dontWearRead.html"
   f = open(filename, "wb")
   f.write(bytes(htmlText, "utf-8"))
   #f.write(bytes(htmlText_indented, "utf-8"))
   f.close()
   print("    wrote %s" % f.name)

#--------------------------------------------------------------------------------
def test_marthaLamontOwl():

   print("--- test_marthaLamontOwn")

   f = "../testData/validEafYamlFiles/owlLivesThere.yaml"


   text = YamlToText(f,
                     grammaticalTerms=mga.getAll(),
                     projectDirectory="tmp",
                     verbose = False,
                     fontSizeControls = True,
                     startLine = None,
                     endLine = None,
                     pageTitle = "Martha Lamont - Owl Lives There",
                     helpFilename = None,
                     helpButtonLabel = None,
                     kbFilename = None,
                     linguisticsFilename = None,
                     fixOverlappingTimeSegments = False,
                     webpackLinksOnly=False,
                     useTooltips=False)


   htmlText = text.toHTML()

   filename = "owlLivesThere.html"
   f = open(filename, "wb")
   f.write(bytes(htmlText, "utf-8"))
   f.close()
   print("    wrote %s" % f.name)

#--------------------------------------------------------------------------------
def runTests():

   test_marthaLamontOwl()

   test_infernoSimple()
   test_harryMosesDaylight()
   test_tlingitVideoVanRescue()
   test_lushootseedGrammar()
   test_aliceFromEaf()

#--------------------------------------------------------------------------------
if __name__ == '__main__':
    runTests()
