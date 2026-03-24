import argparse
import os, sys
import unittest
from slexil.sfmtToWebPage import sfmtToWebPage
from slexil.tieredLine import TieredLine
from pathlib import Path
import pdb
import re
import yattag
from yattag import Doc
#--------------------------------------------------------------------------------
from slexil.morphemeGlossAbbreviations import MorphemeGlossAbbreviations
mga = MorphemeGlossAbbreviations()
#--------------------------------------------------------------------------------
def test_infernoOneLine():

   print("--- test_infernoOneLine")

   f = "../testData/validEafYamlFiles/inferno-1-line.yaml"

   page = sfmtToWebPage(f,
                        grammaticalTerms = mga.getAll(),
                        projectDirectory="inferno",
                        verbose = False,
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

   filename = "%s.html" % Path(f).stem

   f = open(filename, "wb")
   f.write(bytes(htmlText, "utf-8"))
   f.close()

   print("    wrote %s" % f.name)

#--------------------------------------------------------------------------------
def test_infernoSimple():

   print("--- test_infernoSimple")

   f = "../testData/validEafYamlFiles/inferno-mixedCaseMorphemes.yaml"

   page = sfmtToWebPage(f,
                        grammaticalTerms = mga.getAll(),
                        projectDirectory="inferno",
                        verbose = False,
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

   filename = "%s.html" % Path(f).stem

   f = open(filename, "wb")
   f.write(bytes(htmlText, "utf-8"))
   f.close()

   print("    wrote %s" % f.name)

#--------------------------------------------------------------------------------
def test_infernoWithHtml():

   print("--- test_infernoWithHtml")

   f = "../testData/validEafYamlFiles/inferno-withHtmlLines.yaml"

   page = sfmtToWebPage(f,
                        grammaticalTerms = mga.getAll(),
                        projectDirectory="inferno",
                        verbose = False,
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

   filename = "%s.html" % Path(f).stem
   f = open(filename, "wb")
   f.write(bytes(htmlText, "utf-8"))
   f.close()

   print("    wrote %s" % f.name)

#--------------------------------------------------------------------------------
# we prevent the yaml parser from interepreting special characters, commonly
# used by linguists, using this convention:
#   morphemes: |
#       [en=il,mezz–o,de=il,cammin–Ø,di,nostr–a,vit–a]
# rather than
#   morphemes: [en=il,mezz–o,de=il,cammin–Ø,di,nostr–a,vit–a]
# a complexity arises.  the [a,b] list is a string, 

def test_inferno_withEscapedYaml():

   print("--- test_inferno_withEscapedYaml")

   f = "../testData/validEafYamlFiles/inferno-threeLines-escapedYaml.yaml"

   page = sfmtToWebPage(f,
                        grammaticalTerms = mga.getAll(),
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


   # print(page.getTierSummary())
   htmlText = page.toHTML()
   #htmlText_indented = yattag.indent(htmlText)

   # 3 lines of speech, one jquery pattern

   filename = "inferno-escaped-yaml.html"
   f = open(filename, "wb")
   f.write(bytes(htmlText, "utf-8"))
   #f.write(bytes(htmlText_indented, "utf-8"))
   f.close()
   print("    wrote %s" % f.name)

#----------------------------------------------------------------------------------------------------
def test_harryMosesDaylight():

   print("--- test_harryMosesDaylight")

   f = "../testData/validEafYamlFiles/daylight-3lines.yaml"
   gtf = "../explore/lushootseed/harryMoses/daylight-prosody/grammaticalTerms.txt"

   #with open(gtf) as file:
   #   grammaticalTerms = file.read().split("\n")
   #   count = len(grammaticalTerms)
   #   if grammaticalTerms[count-1] == "":
   #      grammaticalTerms.pop()
   page = sfmtToWebPage(f,
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


   # print(page.getTierSummary())
   htmlText = page.toHTML()
   #htmlText_indented = yattag.indent(htmlText)

   # 3 lines of speech, one jquery pattern

   filename = "daylight.html"
   f = open(filename, "wb")
   f.write(bytes(htmlText, "utf-8"))
   #f.write(bytes(htmlText_indented, "utf-8"))
   f.close()
   print("    wrote %s" % f.name)

#--------------------------------------------------------------------------------
def test_harryMosesDaylight_bug():

   print("--- test_harryMosesDaylight_bug")

   f = "/Users/paul/github/slexil2/testData/validEafYamlFiles/daylight-bug.yaml"

   page = sfmtToWebPage(f,
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


   # print(page.getTierSummary())
   htmlText = page.toHTML()
   #htmlText_indented = yattag.indent(htmlText)

   # 3 lines of speech, one jquery pattern

   filename = "daylight-full.html"
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

   page = sfmtToWebPage(f,
                        grammaticalTerms = mga.getAll(),
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


   # print(page.getTierSummary())
   htmlText = page.toHTML()
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

   page = sfmtToWebPage(f,
                     grammaticalTerms=mga.getAll(),
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


   # print(page.getTierSummary())
   htmlText = page.toHTML()
   #htmlText_indented = yattag.indent(htmlText)

   # 3 lines of speech, one jquery pattern

   filename = "tlingit.html"
   f = open(filename, "wb")
   f.write(bytes(htmlText, "utf-8"))
   #f.write(bytes(htmlText_indented, "utf-8"))
   f.close()
   print("    wrote %s" % f.name)

#--------------------------------------------------------------------------------
def test_TrueForYesYamlParsing():

   print("--- test_TrueForYesYamlParsing")

   f = "../testData/validEafYamlFiles/jitz-tiny-with-yes.yaml"
   gtf = None

   page = sfmtToWebPage(f,
                        grammaticalTerms=mga.getAll(),
                     projectDirectory="tmp",
                     verbose = False,
                     fontSizeControls = True,
                     startLine = None,
                     endLine = None,
                     pageTitle = "jitz-tiny-with-yes",
                     helpFilename = None,
                     helpButtonLabel = None,
                     kbFilename = None,
                     linguisticsFilename = None,
                     fixOverlappingTimeSegments = False,
                     webpackLinksOnly=False,
                     useTooltips=False)


   htmlText = page.toHTML()

   assert(htmlPage.find("yes") > 0)
   filename = "jitz-tiney.html"
   f = open(filename, "wb")
   f.write(bytes(htmlText, "utf-8"))
   f.close()
   print("    wrote %s" % f.name)
   
#--------------------------------------------------------------------------------
def test_aliceFromEaf():

   print("--- test_aliceFromEaf")

   f = "dontWearRed.yaml"

   page = sfmtToWebPage(f,
                     grammaticalTerms=mga.getAll(),
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


   # print(page.getTierSummary())
   htmlText = page.toHTML()
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

   print("--- test_marthaLamontOwl")

   f = "../testData/validEafYamlFiles/owlLivesThere.yaml"


   page = sfmtToWebPage(f,
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


   htmlText = page.toHTML()

   filename = "owlLivesThere.html"
   f = open(filename, "wb")
   f.write(bytes(htmlText, "utf-8"))
   f.close()
   print("    wrote %s" % f.name)

#--------------------------------------------------------------------------------
def test_handleUnnumberedLines():

   print("--- test_handleUnnumberedLines")

   f = "../testData/validEafYamlFiles/inferno-withHTMLAndUnnumberedLines.yaml"

   page = sfmtToWebPage(f,
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


   htmlText = page.toHTML()
   filename = "inferno-unnumberedLines.html"
   f = open(filename, "wb")
   f.write(bytes(htmlText, "utf-8"))
   f.close()
   print("    wrote %s" % f.name)

#--------------------------------------------------------------------------------
# demonstration: shows how to find a line, a tag, which offends yattag.
# with a minor change to tieredLine.py, this demo no longer fails, but
# the method demonstrated here will likely be uselful in the future.
def test_findYattagOffendingLine():

   print("--- test_findYattagOffendingLine")
   f = "../testData/validEafYamlFiles/30-01-03cLlorona-MM.yaml"
   page = sfmtToWebPage(f,
                     grammaticalTerms = [],
                     projectDirectory="/tmp",
                     verbose = False,
                     fontSizeControls = True,
                     startLine = None,
                     endLine = None,
                     pageTitle = "30-01-03cLlorona-MM",
                     helpFilename = None,
                     helpButtonLabel = None,
                     kbFilename = None,
                     linguisticsFilename = None,
                     fixOverlappingTimeSegments = False,
                     webpackLinksOnly=False,
                     useTooltips=False)
   lines = page.lines

   htmlDoc = Doc()
   print(" lines from yaml: %d" % len(page.lines))
   
   for i in range(len(page.lines)):
      print(" toHTML on line %d" % i, flush=True)
      tieredLine = TieredLine(page.lines, i, i+1,
                              page.tierGuide,
                              grammaticalTerms=None,
                              useTooltips=False,
                              verbose=True)
      try:
         tieredLine.toHTML(htmlDoc)
         htmlDoc.getvalue()
      except TypeError as ex:
         print("--- exception raised")
         print(ex)
         pdb.set_trace()

   pdb.set_trace()
      

   
#--------------------------------------------------------------------------------
def runTests():

   
   test_infernoOneLine()
   test_infernoSimple()
   test_marthaLamontOwl()
   test_infernoWithHtml()
   test_lushootseedGrammar()
   test_harryMosesDaylight_bug()

   test_marthaLamontOwl()

   test_inferno_withEscapedYaml()
   test_harryMosesDaylight()
   test_tlingitVideoVanRescue()
   test_aliceFromEaf()

   test_handleUnnumberedLines()

#--------------------------------------------------------------------------------
if __name__ == '__main__':
    runTests()
