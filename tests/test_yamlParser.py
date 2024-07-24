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
   lineNumber = 2
   x = yp.getIjalLine(lineNumber)
   assert(x['lineNumber'] == lineNumber)
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
def test_getTimeTable():

   print("--- test_getTimeTable")

   f = "../testData/validYamlFiles/inferno.yaml"
   ftg = "../testData/validYamlFiles/infernoTierGuide.yaml"
   yp = YamlParser(f, ftg)

   tbl = yp.getTimeTable()
   assert(tbl.shape == (3, 2))
   assert(tbl['start'].tolist() == [0,3095,5624])
   assert(tbl['end'].tolist() == [2828, 5500, 8033])

#----------------------------------------------------------------------------------------------------
def test_lineDictToTable():

   print("--- test_lineDictToTable")
   f = "../testData/validYamlFiles/inferno.yaml"
   ftg = "../testData/validYamlFiles/infernoTierGuide.yaml"
   yp = YamlParser(f, ftg)
   yp.parseAndSortAllLines()
   lineDict = yp.getAllLines()[1]
   assert(isinstance(lineDict, dict))
   tbl = yp.lineDictToTable(lineDict, 1)
   
#----------------------------------------------------------------------------------------------------
def test_getAllLines():

   print("--- test_getAllLines")

   f = "../testData/validYamlFiles/inferno.yaml"
   ftg = "../testData/validYamlFiles/infernoTierGuide.yaml"
   yp = YamlParser(f, ftg)
   yp.parseAndSortAllLines()
   pl = yp.getAllLines()

   assert(len(pl) == 9)

     # lines (0-based)
     #  html: 0,1, 4-7
     #  ijal: 2,3,8
     # [type(line) for line in pl]

   assert(isinstance(pl[0], str))
   assert(isinstance(pl[1], str))
   assert(isinstance(pl[2], dict))
   assert(isinstance(pl[3], dict))
   assert(isinstance(pl[4], str))
   assert(isinstance(pl[5], str))
   assert(isinstance(pl[6], str))
   assert(isinstance(pl[7], str))
   assert(isinstance(pl[8], dict))
   

   assert(pl[0] == '<h3> Read by Roberto Begnini</h3> taken from youtube')

   assert(pl[2]['speech'] == 'Nel mezzo del cammin di nostra vita')
   assert(pl[3]['speech'] ==  'mi ritrovai per una selva oscura')
   assert(pl[8]['speech'] == 'ché la diritta via era smarrita.')

#----------------------------------------------------------------------------------------------------
def test_run():

   print("--- test_run")

   f = "../testData/validYamlFiles/inferno.yaml"
   ftg = "../testData/validYamlFiles/infernoTierGuide.yaml"
   yp = YamlParser(f, ftg)
   yp.run()
    
#----------------------------------------------------------------------------------------------------
def runTests():

  test_ctor()
  test_mediaGetters()
  test_getTierInfo()
  test_getIjalLine()
  test_getHtmlLine()  
  # test_lineDictToTable()
  test_getTimeTable()
  test_getAllLines()
  test_run()

#---------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    runTests()
