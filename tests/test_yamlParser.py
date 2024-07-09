# -*- tab-width: 3 -*-
import yaml
import pdb
import os, sys
from slexil.yamlParser import YamlParser
from time import time
import pandas as pd
import numpy as np
pd.set_option('display.width', 1000)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
from pathlib import Path
path = Path(".")
#---------------------------------------------------------------------------------------------------
def test_ctor():

    print("--- test_ctor")

    f = "../testData/validYamlFiles/inferno.yaml"
    ftg = "../testData/validYamlFiles/infernoTierGuide.yaml"
    yp = YamlParser(f, ftg)

#----------------------------------------------------------------------------------------------------
def test_mediaGetters():

    print("--- test_mediaGetters")

    f = "../testData/validYamlFiles/inferno.yaml"
    ftg = "../testData/validYamlFiles/infernoTierGuide.yaml"
    yp = YamlParser(f, ftg)

    expected = "https://slexildata.artsrn.ualberta.ca/misc/inferno-threeLines.wav"
    assert(yp.getAudioURL() == expected)
    assert(yp.getVideoURL() == None)
    assert(yp.getMimeType() == "audio/x-wav")
    
           
#----------------------------------------------------------------------------------------------------
def test_mediaGetters():

    print("--- test_mediaGetters")

    f = "../testData/validYamlFiles/inferno.yaml"
    ftg = "../testData/validYamlFiles/infernoTierGuide.yaml"
    yp = YamlParser(f, ftg)

#----------------------------------------------------------------------------------------------------
def test_getTierInfo():

   print("--- test_getTierInfo")

   f = "../testData/validYamlFiles/inferno.yaml"
   ftg = "../testData/validYamlFiles/infernoTierGuide.yaml"
   yp = YamlParser(f, ftg)
   info = yp.getTierInfo()
   keys = list(info.keys())
   values = list(info.values())
   assert(keys == ['speech', 'morpheme', 'morphemeGloss', 'translation'])
   assert(values == ['italianSpeech', 'morphemes', 'morpheme-gloss', 'english'])
    
#----------------------------------------------------------------------------------------------------
def test_getIjalLine():

   print("--- test_getIjalLine")

   f = "../testData/validYamlFiles/inferno.yaml"
   ftg = "../testData/validYamlFiles/infernoTierGuide.yaml"
   yp = YamlParser(f, ftg)
   x = yp.getIjalLine(1)
   assert(x['lineNumber'] ==1)
   assert(x['startTime'] == 0)
   assert(x['endTime'] == 2828)
   assert(x['speech'] == 'Nel mezzo del cammin di nostra vita')
   assert(x['morphemes'] == ['en=il', 'mezz–o', 'de=il', 'cammin–Ø', 'di', 'nostr–a', 'vit–a'])
   assert(x['morphemeGlosses'] == ['in=DEF:MASC:SG', 'middle-MASC:SG', 'of=DEF:MASC:SG', 'journey–MASC:SG', 'of', 'our-FEM:SG', 'life-FEM'])
   assert(x['translation'] == 'Midway upon the journey of our life')

#----------------------------------------------------------------------------------------------------
def test_getHtmlLine():

   print("--- test_getHtmlLine")

   f = "../testData/validYamlFiles/inferno.yaml"
   ftg = "../testData/validYamlFiles/infernoTierGuide.yaml"
   yp = YamlParser(f, ftg)
   content = yp.getHtmlLine(0)
   assert(content == '<h3> Read by Roberto Begnini</h3> taken from youtube')
    
#----------------------------------------------------------------------------------------------------
def runTests():

  test_ctor()
  test_mediaGetters()
  test_getTierInfo()
  test_getIjalLine()
  test_getHtmlLine()  

#---------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    runTests()
