# -*- tab-width: 3 -*-
import yaml
import pdb
import os, sys
from slexil.eafParser import EafParser
import xmlschema
from xml.etree import ElementTree as etree
from time import time
import pandas as pd
import numpy as np
pd.set_option('display.width', 1000)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
from pathlib import Path
path = Path(".")
from xmlschema.validators.exceptions import XMLSchemaValidationError;

eafFiles = open("../testData/eafFileList.txt").read().split('\n')
if(eafFiles[-1] == ""):
    del eafFiles[-1]
print("eaf file count: %d" % len(eafFiles))

#---------------------------------------------------------------------------------------------------
def runTests():

   test_parsingSpeed()
   test_invalidXmlRaisesException_misnamedParentRef()
   test_invalidXmlRaisesException_misnamedTierType()
   test_invalidXmlRaisesException_misspelledTag()
   test_ctor()
   test_tierTable_0()
   test_timeTable()
   test_checkAgainstTierGuide()
   test_depthFirstTierTraversal()
   test_getLineTable()
   test_parseAllLines()
   test_sortLinesByTime_inferno()
   test_sortLinesByTime_natalia()
   test_tedsBlueJay()
   test_fixOverlappingTimes()  # very slow
   test_variousGetters()
   test_getSummary()

#---------------------------------------------------------------------------------------------------
def test_ctor():

    print("--- test_ctor")
    f = eafFiles[0]
    parser = EafParser(f, verbose=False, fixOverlappingTimeSegments=False)
    parser.run()
    assert(parser.getFilename() == f)
    assert(parser.xmlValid())

#---------------------------------------------------------------------------------------------------
def test_parsingSpeed(slowVersion=False):

   print("--- test_parsingSpeed")

   f = "../explore/aliceTaff/01/01RuthNora230503Slexil.eaf"
   print("    01RuthNora230503Slexil.eaf")
   t0 = time() * 1000
   parser = EafParser(f, verbose=False, fixOverlappingTimeSegments=False)
   t1 = time() * 1000
   parser.run()
   t2 = time() * 1000
   parser.xmlValid()
   t3 = time() * 1000

   lineCount = parser.getLineCount()

   print("lines: %d" % lineCount)
   print(" ctor: %d" % round(t1 - t0))
   print("  run: %d" % round(t2 - t1))
   print("valid: %d" % round(t3 - t2))

   if not slowVersion:
       return
   
   f = "../explore/aliceTaff/04/4EthelAnita230503Slexil.eaf"
   print("    4EthelAnita230503Slexil")
   t0 = time() * 1000
   parser = EafParser(f, verbose=False, fixOverlappingTimeSegments=False)
   t1 = time() * 1000
   parser.run()
   t2 = time() * 1000
   parser.xmlValid()
   t3 = time() * 1000

   lineCount = parser.getLineCount()

   print("lines: %d" % lineCount)
   print(" ctor: %d" % round(t1 - t0))
   print("  run: %d" % round(t2 - t1))
   print("valid: %d" % round(t3 - t2))

   
#---------------------------------------------------------------------------------------------------
def test_mediaUrlExtraction():

   print("--- test_mediaUrlExtraction")

   f = "../explore/aliceTaff/01/01RuthNora230503Slexil.eaf"
   parser = EafParser(f, verbose=False, fixOverlappingTimeSegments=False)
   a = parser.getAudioInfo()
   v = parser.getVideoInfo()

#---------------------------------------------------------------------------------------------------
def test_invalidXmlRaisesException_misnamedParentRef():

    print("--- test_invalidXmlRaisesException_misnamedParentRef")
    f = "../testData/invalidEafFiles/inferno-misnamedParentRef.eaf"
    
    try:
       parser = EafParser(f, verbose=False, fixOverlappingTimeSegments=False)
       parser.xmlValid()
       success = True
    except XMLSchemaValidationError as e:
       assert(e.message.find("failed validating") >= 0)
       assert(len(e.args) == 5)
       assert(e.args[2] == "value ('italianSpEEch',) not found for XsdKey(name='tierNameKey')")
       success = False

    assert(not success)
    
#---------------------------------------------------------------------------------------------------
def test_invalidXmlRaisesException_misnamedTierType():

    print("--- test_invalidXmlRaisesException_misnamedTierType")
    f = "../testData/invalidEafFiles/inferno-misnamedTierType.eaf"
    
    try:
       parser = EafParser(f, verbose=False, fixOverlappingTimeSegments=False)
       parser.xmlValid()
       success = True
    except XMLSchemaValidationError as e:
       assert(e.message.find("failed validating") >= 0)
       assert(len(e.args) == 5)
       assert(e.args[2] == "value ('translation',) not found for XsdKey(name='linTypeNameKey')")
       success = False

    assert(not success)

#---------------------------------------------------------------------------------------------------
def test_invalidXmlRaisesException_misspelledTag():

    print("--- test_invalidXmlRaisesException_misspelledTag")
    f = "../testData/invalidEafFiles/inferno-misspelledTag.eaf"
    
    try:
       parser = EafParser(f, verbose=False, fixOverlappingTimeSegments=False)
       parser.xmlValid()
       success = True
    except XMLSchemaValidationError as e:
       errorString = str(e)
       assert(errorString.find("failed validating") >= 0)
       assert(errorString.find("Unexpected child with tag") >= 0)
       assert(errorString.find("TIME_ORDERxxx") >= 0)
       success = False

    assert(not success)

#---------------------------------------------------------------------------------------------------
def test_tierTable_0():

    print("--- test_tierTable_0")

    f0 = "../testData/inferno/inferno-threeLines.eaf"
    f1 = "../explore/aliceTaff/v1/01RuthNora230209AT-orig.eaf"
    f2 = "../explore/daylight/beckAndHess/beckAndHess.eaf"
    f3 = "../explore/nataliaCaceres/incoming/084_TheWomanOfTheWater-DonkeyTiger.eaf"
    f4 = "../explore/daylight/beckAndHess/beckAndHess.eaf"
    
    parser = EafParser(f0, verbose=False, fixOverlappingTimeSegments=False)
    parser.run()

    tbl = parser.getTierTable()
    assert(tbl.shape == (4,7))
       # check column names
    expected = ['TIER_ID', 'LINGUISTIC_TYPE_REF', 'PARENT_REF', 'DEFAULT_LOCALE',
                'CONSTRAINTS', 'GRAPHIC_REFERENCES', 'TIME_ALIGNABLE']
    assert(tbl.columns.values.tolist() == expected)
       # check 1st column 
    assert(tbl["TIER_ID"].tolist() ==
                     ['italianSpeech', 'morphemes', 'morpheme-gloss', 'english'])
    assert(tbl["TIME_ALIGNABLE"].tolist() ==
                      ['true', 'false', 'false', 'false'])

      # parent_ref column values: [nan, 'utterance', 'utterance', 'utterance'])
      # must use 2 steps to handle nan
    assert(np.isnan(tbl.loc[0, "PARENT_REF"]))
      # the morpehmeGloss tier is the child of morphemes
      # it could also, and perhaps more commonly, be a child of the time-aligned
      # tier, lushootseed
    assert(tbl.loc[1:3, "PARENT_REF"].tolist() ==
                     ['italianSpeech', 'italianSpeech', 'italianSpeech'])

#--------------------------------------------------------------------------------
def test_tierTable():

    print("--- test_tierTable")

    f0 = "../testData/inferno/inferno-threeLines.eaf"
    f1 = "../explore/aliceTaff/v1/01RuthNora230209AT-orig.eaf"
    f2 = "../explore/daylight/beckAndHess/beckAndHess.eaf"
    f3 = "../explore/nataliaCaceres/incoming/084_TheWomanOfTheWater-DonkeyTiger.eaf"
    f4 = "../explore/daylight/beckAndHess/beckAndHess.eaf"
    
    parser = EafParser(f, verbose=False, fixOverlappingTimeSegments=False)
    parser.run()
    tbl = parser.getTierTable()
    assert(tbl.shape == (4,5))
       # check column names
    expected = ['TIER_ID', 'LINGUISTIC_TYPE_REF', 'PARENT_REF', 'DEFAULT_LOCALE', 'TIME_ALIGNABLE']
    assert(tbl.columns.values.tolist() == expected)
       # check 1st column 
    assert(tbl["TIER_ID"].tolist() ==
                     ['lushootseed', 'morphemes', 'morphemeGloss', 'english'])
    assert(tbl["TIME_ALIGNABLE"].tolist() ==
                      ['true', 'false', 'false', 'false'])

      # parent_ref column values: [nan, 'utterance', 'utterance', 'utterance'])
      # must use 2 steps to handle nan
    assert(np.isnan(tbl.loc[0, "PARENT_REF"]))
      # the morpehmeGloss tier is the child of morphemes
      # it could also, and perhaps more commonly, be a child of the time-aligned
      # tier, lushootseed
    assert(tbl.loc[1:3, "PARENT_REF"].tolist() ==
                     ['lushootseed', 'morphemes', 'lushootseed'])

#---------------------------------------------------------------------------------------------------
def test_tierTable_1():

    print("--- test_tierTable")

    f0 = "../testData/inferno/inferno-threeLines.eaf"
    f1 = "../explore/aliceTaff/v1/01RuthNora230209AT-orig.eaf"
    f2 = "../explore/daylight/beckAndHess/beckAndHess.eaf"
    f3 = "../explore/nataliaCaceres/incoming/084_TheWomanOfTheWater-DonkeyTiger.eaf"
    f4 = "../explore/daylight/beckAndHess/beckAndHess.eaf"
    
    parser = EafParser(f, verbose=False, fixOverlappingTimeSegments=False)
    parser.run()
    tbl = parser.getTierTable()
    assert(tbl.shape == (4,5))
       # check column names
    expected = ['TIER_ID', 'LINGUISTIC_TYPE_REF', 'PARENT_REF', 'DEFAULT_LOCALE', 'TIME_ALIGNABLE']
    assert(tbl.columns.values.tolist() == expected)
       # check 1st column 
    assert(tbl["TIER_ID"].tolist() ==
                     ['lushootseed', 'morphemes', 'morphemeGloss', 'english'])
    assert(tbl["TIME_ALIGNABLE"].tolist() ==
                      ['true', 'false', 'false', 'false'])

      # parent_ref column values: [nan, 'utterance', 'utterance', 'utterance'])
      # must use 2 steps to handle nan
    assert(np.isnan(tbl.loc[0, "PARENT_REF"]))
      # the morpehmeGloss tier is the child of morphemes
      # it could also, and perhaps more commonly, be a child of the time-aligned
      # tier, lushootseed
    assert(tbl.loc[1:3, "PARENT_REF"].tolist() ==
                     ['lushootseed', 'morphemes', 'lushootseed'])

#---------------------------------------------------------------------------------------------------
def test_tierTable_2():

    print("--- test_tierTable_2")

    f0 = "../testData/inferno/inferno-threeLines.eaf"
    f1 = "../explore/aliceTaff/v1/01RuthNora230209AT-orig.eaf"
    f2 = "../explore/daylight/beckAndHess/beckAndHess.eaf"
    f3 = "../explore/nataliaCaceres/incoming/084_TheWomanOfTheWater-DonkeyTiger.eaf"
    f4 = "../explore/daylight/beckAndHess/beckAndHess.eaf"
    
    parser = EafParser(f, verbose=False, fixOverlappingTimeSegments=False)
    parser.run()
    tbl = parser.getTierTable()
    assert(tbl.shape == (4,5))
       # check column names
    expected = ['TIER_ID', 'LINGUISTIC_TYPE_REF', 'PARENT_REF', 'DEFAULT_LOCALE', 'TIME_ALIGNABLE']
    assert(tbl.columns.values.tolist() == expected)
       # check 1st column 
    assert(tbl["TIER_ID"].tolist() ==
                     ['lushootseed', 'morphemes', 'morphemeGloss', 'english'])
    assert(tbl["TIME_ALIGNABLE"].tolist() ==
                      ['true', 'false', 'false', 'false'])

      # parent_ref column values: [nan, 'utterance', 'utterance', 'utterance'])
      # must use 2 steps to handle nan
    assert(np.isnan(tbl.loc[0, "PARENT_REF"]))
      # the morpehmeGloss tier is the child of morphemes
      # it could also, and perhaps more commonly, be a child of the time-aligned
      # tier, lushootseed
    assert(tbl.loc[1:3, "PARENT_REF"].tolist() ==
                     ['lushootseed', 'morphemes', 'lushootseed'])

#---------------------------------------------------------------------------------------------------
def test_tierTable_3():

    print("--- test_tierTable_3")

    f0 = "../testData/inferno/inferno-threeLines.eaf"
    f1 = "../explore/aliceTaff/v1/01RuthNora230209AT-orig.eaf"
    f2 = "../explore/daylight/beckAndHess/beckAndHess.eaf"
    f3 = "../explore/nataliaCaceres/incoming/084_TheWomanOfTheWater-DonkeyTiger.eaf"
    f4 = "../explore/daylight/beckAndHess/beckAndHess.eaf"
    
    parser = EafParser(f, verbose=False, fixOverlappingTimeSegments=False)
    parser.run()
    tbl = parser.getTierTable()
    assert(tbl.shape == (4,5))
       # check column names
    expected = ['TIER_ID', 'LINGUISTIC_TYPE_REF', 'PARENT_REF', 'DEFAULT_LOCALE', 'TIME_ALIGNABLE']
    assert(tbl.columns.values.tolist() == expected)
       # check 1st column 
    assert(tbl["TIER_ID"].tolist() ==
                     ['lushootseed', 'morphemes', 'morphemeGloss', 'english'])
    assert(tbl["TIME_ALIGNABLE"].tolist() ==
                      ['true', 'false', 'false', 'false'])

      # parent_ref column values: [nan, 'utterance', 'utterance', 'utterance'])
      # must use 2 steps to handle nan
    assert(np.isnan(tbl.loc[0, "PARENT_REF"]))
      # the morpehmeGloss tier is the child of morphemes
      # it could also, and perhaps more commonly, be a child of the time-aligned
      # tier, lushootseed
    assert(tbl.loc[1:3, "PARENT_REF"].tolist() ==
                     ['lushootseed', 'morphemes', 'lushootseed'])

#---------------------------------------------------------------------------------------------------
def test_timeTable():

    print("--- test_timeTable")
    f = eafFiles[3]
      # dependent tier are direct 
    f0 = "../testData/inferno/inferno-threeLines.eaf"
    f1 = "../explore/aliceTaff/v1/01RuthNora230209AT-orig.eaf"
    f2 = "../explore/daylight/beckAndHess/beckAndHess.eaf"
    f3 = "../explore/nataliaCaceres/incoming/084_TheWomanOfTheWater-DonkeyTiger.eaf"

    assert(f == '../testData/validEafFiles/inferno-threeLines.eaf')
    parser = EafParser(f, verbose=False, fixOverlappingTimeSegments=False)
    parser.run()
    tbl = parser.getTimeTable()
    assert(tbl.shape == (3,5))
       # looks like this:
       # tbl.loc[1:3]
       #   lineID  start   end   t1   t2
       # 1  a1358   1400  2475  ts3  ts4
       # 2  a1376   2665  5090  ts5  ts6
       # 3  a1377   5090  7530  ts7  ts8

    assert(tbl.columns.values.tolist() ==
                     ['lineID', 'start', 'end', 't1', 't2'])
    startTimes = tbl["start"].tolist()
    endTimes = tbl["end"].tolist()
    assert(startTimes == [0, 3095, 5624])
    assert(endTimes == [2828, 5500, 8033])
    
#---------------------------------------------------------------------------------------------------
# tierGuide.yaml 
def test_checkAgainstTierGuide():

   print("--- test_againstTierGuide")
   eaf = "../testData/inferno/inferno-threeLines.eaf"
   goodTierGuide = "../testData/inferno/tierGuide.yaml"
   badTierGuide = "../testData/inferno/tierGuide-broken.yaml"

   parser = EafParser(eaf, verbose=False, fixOverlappingTimeSegments=False)
   result = parser.checkAgainstTierGuide(goodTierGuide)
   assert(result == {'valid': True, 'failures': []})

   result = parser.checkAgainstTierGuide(badTierGuide)
   assert(not result["valid"])
   assert("EyetalianSpeech" in result["failures"])
   assert("scottish" in result["failures"])

#---------------------------------------------------------------------------------------------------
# lines from typically all tiers are grouped with a time-aligned spoken tier
# we need to recover all of those lines, some of which may be nested > 1 level
# below the spoken tier line.  this recursive capability is tested here.
#---------------------------------------------------------------------------------------------------
def test_depthFirstTierTraversal():

    print("--- test_depthFirstTierTraversal")
    f = eafFiles[0]
    f = "../testData/inferno/inferno-threeLines.eaf"
    parser = EafParser(f, verbose=False, fixOverlappingTimeSegments=False)
    parser.run()

    nestedAnnotationIDs = parser.depthFirstTierTraversal("a2")
    assert(nestedAnnotationIDs == ['a6', 'a10', 'a14'])

      # a10 is a child of a6 (morpheme -> morphemeGloss)
    nestedAnnotationIDs = parser.depthFirstTierTraversal("a6")
    assert(nestedAnnotationIDs == ['a10'])

      # a10 is a leaf node: no children
    nestedAnnotationIDs = parser.depthFirstTierTraversal("a10")
    assert(nestedAnnotationIDs == [])

      # a1 is aligned.  it too should have 2 direct &
      # 1 indirect children
    nestedAnnotationIDs = parser.depthFirstTierTraversal("a1")
    assert(nestedAnnotationIDs == ['a5', 'a9', 'a13'])

      # now a tlingit eaf

    f =  "../explore/aliceTaff/incoming/eafs/12HelenFloBaby230503Slexil.eaf"
    parser = EafParser(f, verbose=False, fixOverlappingTimeSegments=False)
    parser.run()
    nestedAnnotationIDs = parser.depthFirstTierTraversal("a1")
    assert(nestedAnnotationIDs == ['a365'])


#---------------------------------------------------------------------------------------------------
# a "line" is the parent time-aligned tier, and all of its associated child tiers
def test_getLineTable():

    print("--- test_getLineTable")

    f = eafFiles[0]
    parser = EafParser(f, verbose=False, fixOverlappingTimeSegments=False)
    assert(parser.getLineCount() == 3)

    tbl = parser.getTierTable()
    assert(tbl.shape == (4, 7))

    tbl = parser.getTimeTable()
    assert(tbl.shape == (3, 5))

    tbl = parser.getLineTable(1)
    assert(tbl.shape == (4, 7))
    expected = ['id','parent','startTime','endTime','tierID','tierType','text']
    assert(tbl.columns.tolist() == expected)
    assert(tbl["id"].tolist() == ['a1', 'a5', 'a9', 'a13'])
    assert(tbl["parent"].tolist() == ['', 'a1', 'a5', 'a1'])
    expected = ['italianSpeech', 'morphemes', 'morpheme-gloss', 'english']
    assert(tbl["tierID"].tolist() == expected)
    assert(tbl.loc[0, "startTime"] == 0.0)
    assert(tbl.loc[0, "endTime"] == 3093.0)

#---------------------------------------------------------------------------------------------------
# a "line" is the parent time-aligned tier, and all of its associated child tiers
def test_parseAllLines():

    print("--- test_parseAllLines")
    f = eafFiles[0]
    parser = EafParser(f, verbose=False, fixOverlappingTimeSegments=False)
    parser.run()
    assert(parser.getLineCount() == 3)
    x = parser.getAllLinesTable()  # a list of time-ordered line tables
    startTimes = [tbl.loc[0, "startTime"] for tbl in x]
    assert(startTimes == [0.0, 3093.0, 5624.0])

#---------------------------------------------------------------------------------------------------
# eaf lines may come out of order.  this is especially likely when multiple
# speakers are annotated, since the linguist is likely to put them in separate tiers
# we, howerver, need one time-aligned sort list of lines
def test_sortLinesByTime_inferno():

   print("--- test_sortLinesByTime_inferno")
   f = "../testData/validEafFiles/inferno-threeLines-outOfTimeOrder.eaf"
   parser = EafParser(f, verbose=False, fixOverlappingTimeSegments=False)
   parser.run()

   tiers = parser.getTierTable()
   lines = parser.getAllLinesTable()
   times = parser.getTimeTable()
      # ensure that, in addition to times table rows being sorted
      # by the start column, that the indices (row numbers) are
      # also sorted.  this is essential.  in the browser, lines
      # are identified by these indices, scrolled to and highlighted
      # and if these do not follow time order, crazy bad scrolling occurs
   assert(times.index.tolist() == [0,1,2])

   startTimesFromTimes = times["start"].tolist()

       # make sure the times are sorted
       # test for actual sort order by calling the sort function
       # I don't know the evaluation order within "assert" so
       # I make a copy of the original to check against a list
       # we explicitly sort here.  

   startTimesFromTimes_copy = startTimesFromTimes
   startTimesFromTimes.sort()
   assert(startTimesFromTimes_copy == startTimesFromTimes)

   startTimesFromLines = [line["startTime"].tolist()[0] for line in lines]
   startTimesFromLines_copy = startTimesFromLines
   startTimesFromLines.sort()
   assert(startTimesFromLines_copy == startTimesFromLines)

   assert(startTimesFromTimes == startTimesFromLines)

#--------------------------------------------------------------------------------
# natalia presents eaf files with multiple speakers, two in the case
# examined here.  
def test_sortLinesByTime_natalia():

   print("--- test_sortLinesByTime_natalia")
   f = "../testData/validEafFiles/084_TheWomanOfTheWater-DonkeyTiger.eaf"
   parser = EafParser(f, verbose=False, fixOverlappingTimeSegments=False)
   parser.run()
   tiers = parser.getTierTable()
   lines = parser.getAllLinesTable()
   times = parser.getTimeTable()

     # ensure that not only times, but row numbers (indices)
     # are sorted
   assert(times.index.tolist() == list(range(0, times.shape[0])))


   startTimesFromTimes = times["start"].tolist()
   startTimesFromLines = [line["startTime"].tolist()[0] for line in lines]
   assert(startTimesFromTimes == startTimesFromLines)


#---------------------------------------------------------------------------------------------------
def test_fixOverlappingTimes():

    print("--- test_fixOverlappingTimes")
    f = "../testData/overlappingTimes.eaf"
    parser = EafParser(f, verbose=False, fixOverlappingTimeSegments=False)
    parser.run()

    rowCount = parser.getLineCount()
    assert(rowCount == 1132)
    tbl = parser.getTimeTable()
    overlaps = [tbl.iloc[i,2] >= tbl.iloc[i+1,1] for i in range(0,rowCount-1)]
       # 1131 check, not 1132, since the first line has no previous 
       # line with which it can overlap
    assert(pd.DataFrame(overlaps).groupby(0).size()[True]  == 1024)
    assert(pd.DataFrame(overlaps).groupby(0).size()[False] == 107)

       # now decrement the end of each of those overlapping lines by 1 msec
    parser = EafParser(f, verbose=False, fixOverlappingTimeSegments=True)
    parser.run()

    tbl = parser.getTimeTable()
    overlaps = [tbl.iloc[i,2] >= tbl.iloc[i+1,1] for i in range(0,rowCount-1)]
    assert(pd.DataFrame(overlaps).groupby(0).size()[False] == 1131)
    print("    leaving test_fixOverlappingTimes")

#---------------------------------------------------------------------------------------------------
# we usually want disjoint times, so that only one is selected at a time
# in manual playback.  test that optional capability here
def test_tedsBlueJay():

    print("--- test_tedsBlueJay")
    f = "../testData/Metcalf7ab_BLUEJAY_ch1.eaf"
    parser = EafParser(f, verbose=False, fixOverlappingTimeSegments=False)
    parser.run()
    
    rowCount = parser.getLineCount()
    tbl = parser.getTimeTable()
    x = parser.getAllLinesTable()  # a list of time-ordered line tables
    startTimes = [tbl.loc[0, "startTime"] for tbl in x]
    assert(len(startTimes) == 120)
    assert(startTimes[:5] == [0, 0, 2507, 2507, 6651])
    

#---------------------------------------------------------------------------------------------------
def test_variousGetters():

   print("--- test_variousGetters")
     #---------------------------------------------------------------
     # use an eaf with just one time-aligned tier, just one child
     #---------------------------------------------------------------

   f = "../explore/aliceTaff/01/01RuthNora230503Slexil.eaf"
   p = EafParser(f, verbose=False, fixOverlappingTimeSegments=False)
   p.run()
   assert(p.getFilename() == '../explore/aliceTaff/01/01RuthNora230503Slexil.eaf')
   assert(p.getLineCount() == 170)
   assert(p.getTierTable().shape == (2,7))
   assert(p.getAudioURL() ==
          'file:///Users/ataff/Documents/266286-19NEH/1RuthNora/1RuthNora2Wide.wav')
   assert(p.getAudioMimeType() == 'audio/x-wav')
   assert(p.getVideoURL() ==
          'https://slexildata.artsrn.ualberta.ca/tlingit/1RuthNora2Wide.m4v')
   assert(p.getVideoMimeType() == "unknown")
      # p.getMetadata()  # todo.  currently does nothing
   assert(p.getTimeTable().shape == (170,5))
   assert(len(p.getAllLinesTable()) == 170)
    
#---------------------------------------------------------------------------------------------------
def test_getSummary():

   print("--- test_getSummary")

     #---------------------------------------------------------------
     # first, an eaf with just one time-aligned tier, just one child
     #---------------------------------------------------------------

   f = "../explore/aliceTaff/01/01RuthNora230503Slexil.eaf"
   parser = EafParser(f, verbose=False, fixOverlappingTimeSegments=False)
   parser.run()
   x =  parser.getSummary()
   keys = list(x)
   keys.sort()
   assert(keys == ['audioMimeType', 'audioURL', 
                   'lineCount', 'tierTable',
                   'timeAlignedTierFamily.1',
                   'timeAlignedTiers',
                   'videoMimeType', 'videoURL'])
   assert(x["lineCount"] == 170)
   assert(x["tierTable"].shape == (2, 7))
   assert(x["audioMimeType"] == 'audio/x-wav')
   assert(x["audioURL"] == 
          "file:///Users/ataff/Documents/266286-19NEH/1RuthNora/1RuthNora2Wide.wav")
   assert(x["videoMimeType"] == 'unknown')
   assert(x["videoURL"] == 
          'https://slexildata.artsrn.ualberta.ca/tlingit/1RuthNora2Wide.m4v')
   assert(x["timeAlignedTierFamily.1"] == ['translation'])
          
     #---------------------------------------------------------------
     # second, the standard IJAL 4-tier line, one time-aligned
     #---------------------------------------------------------------

   f = "../explore/misc/inferno/inferno-threeLines.eaf"
   parser = EafParser(f, verbose=False, fixOverlappingTimeSegments=False)
   x =  parser.getSummary()
   keys = list(x)
   keys.sort()
   assert(keys == ['audioMimeType', 'audioURL', 
                   'lineCount', 'tierTable',
                   'timeAlignedTierFamily.1',
                   'timeAlignedTiers',
                   'videoMimeType', 'videoURL'])
   assert(x["lineCount"] == 3)
   assert(x["tierTable"].shape == (4, 5))
   assert(x["audioMimeType"] == 'audio/x-wav')
   assert(x["audioURL"] == 
          "https://slexildata.artsrn.ualberta.ca/misc/inferno-threeLines.wav")
   assert(x["videoMimeType"] is None)
   assert(x["videoURL"] is None)

   assert(x["timeAlignedTierFamily.1"] == ['morphemes', 'morpheme-gloss', 'english'])



#---------------------------------------------------------------------------------------------------
def test_lineToYAML():

    print("--- test_lineToYAML")
    f = "../testData/validEafFiles/inferno-threeLines.eaf"
    parser = EafParser(f, verbose=False, fixOverlappingTimeSegments=False)
    line = parser.getAllLinesTable()[0]
    x = parser.lineToYAML(line, 1)
    assert(x[0] == '  - lineNumber: 1')
    assert(x[1] == '    startTime: 0')
    assert(x[2] == '    endTime: 2828')
    assert(x[3] == '    italianSpeech: Nel mezzo del cammin di nostra vita')
    assert(x[4] == '    morphemes: [en=il,mezz–o,de=il,cammin–Ø,di,nostr–a,vit–a]')
    assert(x[5] == '    morpheme-gloss: [in=DEF:MASC:SG,middle-MASC:SG,of=DEF:MASC:SG,journey–MASC:SG,of,our-FEM:SG,life-FEM]')
    assert(x[6] == '    english: Midway upon the journey of our life')
    
#---------------------------------------------------------------------------------------------------
def test_toYAML():

    print("--- test_toYAML")
    f = "../testData/validEafFiles/inferno-threeLines.eaf"
    parser = EafParser(f, verbose=False, fixOverlappingTimeSegments=False)
    yaml = parser.toYAML("Dante's Inferno", "Roberto Benigni", "Paul Shannon",
                         "inferno.yaml")
    
#---------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    runTests()
