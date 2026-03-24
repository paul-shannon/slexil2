# -*- tab-width: 3 -*-
import re
import sys, os

from slexil.ijalLineFromDict import IjalLineFromDict
from slexil.yamlParser import YamlParser

import pdb
import yaml
import yattag
import pandas as pd

pd.set_option('display.width', 1000)
pd.set_option('display.max_columns', None)
#----------------------------------------------------------------------------------------------------
def test_basic():

   print("--- test_basic")
   f = "../testData/validEafYamlFiles/inferno-threeLines.yaml"
   ftg = "../testData/validEafYamlFiles/infernoTierGuide.yaml"
   tierGuide = yaml.load(open(ftg), Loader=yaml.FullLoader)

   yp = YamlParser(f, ftg)
   yp.parseAndSortAllLines()
     # the inferno demo now has some html lines
     # first line of the classic inferno is the third, #2
   lineDict = yp.getAllLines()[0]
   assert(isinstance(lineDict, dict))
    
   ijalLine = IjalLineFromDict(lineDict, 0, tierGuide)
   assert(ijalLine.getTierCount() == 4)

   assert(ijalLine.getStartTime() == 0)
   assert(ijalLine.getEndTime() == 2828)
   assert(ijalLine.getSpokenText() == "Nel mezzo del cammin di nostra vita")
   assert(ijalLine.getTranslation() == "Midway upon the journey of our life")
   expected = ['en=il', 'mezz–o', 'de=il', 'cammin–Ø', 'di', 'nostr–a', 'vit–a']
   assert(ijalLine.getMorphemes() == expected)
   expected = ['in=DEF:MASC:SG', 'middle-MASC:SG', 'of=DEF:MASC:SG', 'journey–MASC:SG', 'of', 'our-FEM:SG', 'life-FEM']
   assert(ijalLine.getMorphemeGlosses() == expected)


#----------------------------------------------------------------------------------------------------
def runTests():

   test_basic()

        
#----------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    runTests()
