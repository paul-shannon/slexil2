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
   f = "../testData/validYamlFiles/inferno.yaml"
   ftg = "../testData/validYamlFiles/infernoTierGuide.yaml"
   tierGuide = yaml.load(open(ftg), Loader=yaml.FullLoader)

   yp = YamlParser(f, ftg)
   yp.parseAndSortAllLines()
   lineDict = yp.getAllLines()[1]
   assert(isinstance(lineDict, dict))
    
   ijalLine = IjalLineFromDict(lineDict, 1, tierGuide, grammaticalTerms=[],
                             useTooltips=False, verbose=True)
   
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
