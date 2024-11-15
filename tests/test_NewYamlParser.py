# -*- tab-width: 3 -*-
import yaml
import pdb
import os, sys
from slexil.newYamlParser import NewYamlParser
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
    yp = NewYamlParser(f)

#----------------------------------------------------------------------------------------------------
def test_mediaGetters():

    print("--- test_mediaGetters: inferno audio")

    f = "../testData/validYamlFiles/inferno.yaml"
    yp = NewYamlParser(f)

    expected = "https://slexildata.artsrn.ualberta.ca/misc/inferno-threeLines.wav"
    assert(yp.getAudioURL() == expected)
    assert(yp.getVideoURL() == None)
    assert(yp.getMimeType() == "audio/x-wav")
    
    print("--- test_mediaGetters: tlingit video")

    f = "../testData/validYamlFiles/tlingitVan-2lines.yaml"
    yp = NewYamlParser(f)

    expected = "https://slexildata.artsrn.ualberta.ca/tlingit/83VanRescue.m4v"
    assert(yp.getAudioURL() == None)
    assert(yp.getVideoURL() == expected)
    assert(yp.getMimeType() == "video/m4v")

    
#----------------------------------------------------------------------------------------------------
def test_getTierGuide():

   print("--- test_getTierGuide")

   f = "../testData/validYamlFiles/inferno.yaml"
   ftg = "../testData/validYamlFiles/infernoTierGuide.yaml"
   yp = NewYamlParser(f, ftg)
   info = yp.getTierGuide()
   keys = list(info.keys())
   values = list(info.values())
   assert(keys == ['speech', 'analysis_1', 'analysis_2', 'tier_1'])
   assert(values == ['italianSpeech', 'morphemes', 'morpheme-gloss', 'english'])
    
#----------------------------------------------------------------------------------------------------
def test_getTieredLineObject():

   print("--- test_getTieredLineObject")

   f = "../testData/validYamlFiles/inferno.yaml"
   yp = NewYamlParser(f)
   lineNumber = 2
   tierNumber = 2
   tl = yp.getTieredLineObject(lineNumber, tierNumber)

   map = tl.getTierMap()  # same as tl.getTierGuide()

   assert(map['speech'] == 'italianSpeech')
   assert(map['analysis_1'] == 'morphemes')
   assert(map['analysis_2'] == 'morpheme-gloss')
   assert(map['tier_1'] == 'english')

#----------------------------------------------------------------------------------------------------
def test_getHtmlLine():
 
  print("--- test_getHtmlLine")

  f = "../testData/validYamlFiles/inferno.yaml"
  yp = NewYamlParser(f)
  content = yp.getHtmlLine(0)
  assert(content == '<h3> Read by Roberto Begnini</h3> taken from youtube')
    
#----------------------------------------------------------------------------------------------------
def test_getTimeTable():

   print("--- test_getTimeTable")

   f = "../testData/validYamlFiles/inferno.yaml"
   yp = NewYamlParser(f)

   tbl = yp.getTimeTable()
   assert(tbl.shape == (3, 2))
   assert(tbl['start'].tolist() == [0,3095,5624])
   assert(tbl['end'].tolist() == [2828, 5500, 8033])

#----------------------------------------------------------------------------------------------------
def test_lineDictToTable():

   print("--- test_lineDictToTable")
   f = "../testData/validYamlFiles/inferno.yaml"
   yp = NewYamlParser(f)
   yp.parseAndSortAllLines()
   assert(len(yp.getAllLines()) == 9)
   assert(len(yp.getHtmlLines()) == 6)
   assert(len(yp.getTieredLines()) == 3)
   line = yp.getAllLines()[1]
   assert(isinstance(line, dict))
   
#----------------------------------------------------------------------------------------------------
def test_getAllLines():

   print("--- test_getAllLines")

   f = "../testData/validYamlFiles/inferno.yaml"
   ftg = "../testData/validYamlFiles/infernoTierGuide.yaml"
   yp = NewYamlParser(f, ftg)
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
   yp = NewYamlParser(f, ftg)
   yp.run()
    
#----------------------------------------------------------------------------------------------------
def runTests():

  test_ctor()
  test_mediaGetters()
  test_getTierGuide()
  test_getTieredLineObject()
  #test_getHtmlLine()  
  test_getTimeTable()
  test_lineDictToTable()
  #test_getAllLines()
  #test_run()

#---------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    runTests()
