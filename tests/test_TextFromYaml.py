import re
import sys, os

from slexil.textFromYaml import TextFromYaml

import pdb
import yaml
import yattag
import pandas as pd

pd.set_option('display.width', 1000)
pd.set_option('display.max_columns', None)
#--------------------------------------------------------------------------------
def test_infernoWithInterspersedHtmlLines():

   print("--- test_infernoWithInterspersedHtmlLines")

   f = "../testData/validYamlFiles/inferno.yaml"
   ftg = "../testData/validYamlFiles/infernoTierGuide.yaml"
   fgt = "../testData/validYamlFiles/infernoTerms.txt"
   text = TextFromYaml(f, fgt, ftg,
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
   htmlText_indented = yattag.indent(htmlText)

      # 3 lines of speech, one jquery pattern
   pattern = re.compile('speech-tier"')
   assert(len(pattern.findall(htmlText)) == 5)

      # should be no other tiers
   pattern = re.compile('-tier">')
   assert(len(pattern.findall(htmlText)) == 6)
   
   filename = "fromYaml.html"
   f = open(filename, "wb")
   f.write(bytes(htmlText_indented, "utf-8"))
   f.close()
   print("    wrote %s" % f.name)

#--------------------------------------------------------------------------------
def runTests():

  test_infernoWithInterspersedHtmlLines()
 
#--------------------------------------------------------------------------------
if __name__ == '__main__':
    runTests()
