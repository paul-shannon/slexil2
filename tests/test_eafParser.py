# -*- tab-width: 3 -*-
import yaml
import pprint
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
from slexil.exceptions import *

eafFiles = open("../testData/eafFileList.txt").read().split('\n')
if(eafFiles[-1] == ""):
    del eafFiles[-1]
print("eaf file count: %d" % len(eafFiles))

#---------------------------------------------------------------------------------------------------
def test_xmlValidity_notMemberFunction():

    from slexil.eafParser import xmlValid
    import traceback

    print("--- test_xmlValidity_notMemberFunction")
    f = "../testData/invalidEafFiles/inferno-misspelledTag.eaf"
    try:
       xmlValid(f)
    except Exception as ex:
        message = str(ex)
        tb = traceback.format_exception_only(None, ex)[0]
        assert("Unexpected child with tag 'TIME_ORDERxxx'" in tb)
    
#---------------------------------------------------------------------------------------------------
def test_ctor():

    print("--- test_ctor")
    f = eafFiles[0]
    parser = EafParser(f, verbose=False, fixOverlappingTimeSegments=False)
    parser.run()
    assert(parser.getFilename() == f)
    assert(parser.xmlValid())
    assert(parser.getRootTimeAlignedTiers() == ['italianSpeech'])

#---------------------------------------------------------------------------------------------------
def test_extractAllRootTimeAlignedTiers():

    from slexil.eafParser import extractAllTimeAlignedTierIDs

    print("--- test_extractAllRootTimeAlignedTiers()")

    fs = ["../testData/inferno/inferno-threeLines.eaf",
          "../testData/validEafYamlFiles/natalia-yekwana.eaf",
          "../explore/aliceTaff/v1/01RuthNora230209AT-orig.eaf",
          "../explore/daylight/beckAndHess/beckAndHess.eaf",
          "../explore/nataliaCaceres/incoming/084_TheWomanOfTheWater-DonkeyTiger.eaf",
          "../explore/daylight/beckAndHess/beckAndHess.eaf"]

    expected = [['italianSpeech'],
                ['ref@FcM', 'ref@Anl'],
                ['utterance'],
                ['lushootseed'],
                ['ref@VG', 'ref@AM'],
                ['lushootseed']]

    i = 0
    for f in fs:
       assert(extractAllTimeAlignedTierIDs(fs[i]))
       #print(expected[i])
       i += 1       

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

   #print("lines: %d" % lineCount)
   #print(" ctor: %d" % round(t1 - t0))
   #print("  run: %d" % round(t2 - t1))
   #print("valid: %d" % round(t3 - t2))

   if not slowVersion:
       return
   
   f = "../explore/aliceTaff/04/4EthelAnita230503Slexil.eaf"
   #print("    4EthelAnita230503Slexil")
   t0 = time() * 1000
   parser = EafParser(f, verbose=False, fixOverlappingTimeSegments=False)
   t1 = time() * 1000
   parser.run()
   t2 = time() * 1000
   parser.xmlValid()
   t3 = time() * 1000

   lineCount = parser.getLineCount()

   #print("lines: %d" % lineCount)
   #print(" ctor: %d" % round(t1 - t0))
   #print("  run: %d" % round(t2 - t1))
   #print("valid: %d" % round(t3 - t2))

   
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

    f0 = "../testData/validEafYamlFiles/inferno-threeLines.eaf"
    f1 = "../explore/aliceTaff/v1/01RuthNora230209AT-orig.eaf"
    f2 = "../explore/daylight/beckAndHess/beckAndHess.eaf"
    f3 = "../explore/nataliaCaceres/incoming/084_TheWomanOfTheWater-DonkeyTiger.eaf"
    f4 = "../explore/daylight/beckAndHess/beckAndHess.eaf"
    
    parser = EafParser(f0, verbose=False, fixOverlappingTimeSegments=False)
    parser.run()

    tbl = parser.getTierTable()
    assert(tbl.shape == (4,5))
       # check column names
    expected = ['TIER_ID', 'PARENT_REF', 'LINES', 'LINGUISTIC_TYPE_REF', 'TIME_ALIGNABLE']
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
    # pdb.set_trace()
    assert(tbl.loc[1:3, "PARENT_REF"].tolist() ==
                     ['italianSpeech', 'morphemes', 'italianSpeech'])

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
    f = eafFiles[0]
      # dependent tier are direct 
    f0 = "../testData/inferno/inferno-threeLines.eaf"
    f1 = "../explore/aliceTaff/v1/01RuthNora230209AT-orig.eaf"
    f2 = "../explore/daylight/beckAndHess/beckAndHess.eaf"
    f3 = "../explore/nataliaCaceres/incoming/084_TheWomanOfTheWater-DonkeyTiger.eaf"

    assert(f == '../testData/inferno/inferno-threeLines.eaf')
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
    assert(startTimes == [0, 3093, 5624])
    assert(endTimes == [3093, 5624, 8033])
    
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
    assert(tbl.shape == (4, 5))

    tbl = parser.getTimeTable()
    assert(tbl.shape == (3, 5))

    tbl = parser.getLineTable(1)
    assert(tbl.shape == (4, 8))
    expected = ['id','parent','startTime','endTime','tierID','tierType','text','tabCount']
    assert(tbl.columns.tolist() == expected)
    assert(tbl["id"].tolist() == ['a1', 'a5', 'a9', 'a13'])
    assert(tbl["parent"].tolist() == ['', 'a1', 'a5', 'a1'])
    expected = ['italianSpeech', 'morphemes', 'morpheme-gloss', 'english']
    assert(tbl["tierID"].tolist() == expected)
    assert(tbl.loc[0, "startTime"] == 0.0)
    assert(tbl.loc[0, "endTime"] == 3093.0)
    
#---------------------------------------------------------------------------------------------------
# a "line" is the parent time-aligned tier, and all of its associated child tiers
# there are two time aligned "root" tiers here.
# at present (december 2024) we only extract the first encountered
# root tier.
# bug encountered, trying to find out why
#  this eaf time-aligned element makes it into the ref@FcM child elements
#     <TIER LINGUISTIC_TYPE_REF="ref" PARTICIPANT="Anl" TIER_ID="ref@Anl">
#        <ANNOTATION>
#            <ALIGNABLE_ANNOTATION ANNOTATION_ID="a84"
#                TIME_SLOT_REF1="ts19" TIME_SLOT_REF2="ts20">
#                <ANNOTATION_VALUE>CtoAbjPic.010</ANNOTATION_VALUE>
#            </ALIGNABLE_ANNOTATION>
#        </ANNOTATION>
#
#  - lineNumber: 10
#    startTime: 68588
#    endTime: 69277
#    ref@Anl: |
#         CtoAbjPic.010
#
#    and like this in eafParser's line list:
#
#  {'lineNumber': 10, 'startTime': 68588, 'endTime': 69277,
#   'ref@Anl': 'CtoAbjPic.010\n'}
#
# and 'ref@An1' is not in the inferred tier guide.

def test_getLineTable_nataliaYekwana():

    print("--- test_getLineTable_nataliaYekwana")

    f = "../testData/validEafYamlFiles/natalia-yekwana.eaf"
    parser = EafParser(f, verbose=False, fixOverlappingTimeSegments=False)
    assert(parser.getLineCount() == 40)

    tbl = parser.getTierTable()
    assert(tbl.shape == (4, 5))

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
   f = "../testData/validEafYamlFiles/inferno-threeLines-outOfTimeOrder.eaf"
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
   f = "../testData/validEafYamlFiles/084_TheWomanOfTheWater-DonkeyTiger.eaf"
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
   assert(p.getTierTable().shape == (2,5))
   assert(p.getAudioURL() is None)
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
   assert(x["tierTable"].shape == (2, 5))
   #assert(x["audioMimeType"] == 'audio/x-wav')
   #assert(x["audioURL"] == 
   #       "file:///Users/ataff/Documents/266286-19NEH/1RuthNora/1RuthNora2Wide.wav")
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
    f = "../testData/validEafYamlFiles/inferno-threeLines.eaf"
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
def test_lineToYAML_multipleTabsSeparatingTokens():

    print("--- test_lineToYAML_multipleTabsSeparatingTokens")
    f = "../testData/validEafYamlFiles/from-dbeckServer/bugs/Crane_COM_TS_RP.eaf"
    parser = EafParser(f, verbose=False, fixOverlappingTimeSegments=False)
    parser.run()
    lineTbls = parser.getAllLinesTable()
    lineTable = lineTbls[8]
    x = parser.lineToYAML(lineTable, 8)
     # morphemes tiers in row 1 (note 0 indexing)
    text = lineTable.iloc[1]['text']

       # the offending line, before fix
       # x[4]
       #'    morphemes: [tuq=namut’ukw’its’uyu,’ew’kw=tqa’,,stulta’luw’qa’.]'
       # figured out that 
   
    x = parser.lineToYAML(lineTable, 8)
    assert("    morphemes: |\n         [tuq=namut’ukw’its’uyu," in x[4])
    assert("    morphemeGloss: |\n         [find.out=LC.REFLOBLDMHSDYN,finish" in x[5])

#---------------------------------------------------------------------------------------------------
def test_lineToYAML_yesBecomesTrue():

    print("--- test_lineToYAML_yesBecomesTrue")
    f = "../testData/invalidEafFiles/JITZ.eaf"
    parser = EafParser(f, verbose=False, fixOverlappingTimeSegments=False)
    parser.run()
    tbl = parser.getAllLinesTable()

        # first, look at what lineToYAML gets us

    line = tbl[44]
    x = parser.lineToYAML(line, 44)
    expected = "    intr-cp: |\n         [SUBORD,3S–appreciate–PASS–DEP2,"
    assert(expected in x[6])

        # now looi at what toYAML gets us

    y = parser.toYAML("title", "narrator", "textEntry")
    assert(len(y) == 620)
    assert(expected in y[401])
   
      # minimal checks
    assert(len(x) == 8)
    assert("lineNumber" in x[0])
    assert ("yes" in x[6])
    
#---------------------------------------------------------------------------------------------------
# alice taff, in her eafs, somtimes
#   - uses curly brackets for false start speech
#   - embeds double quotes
#   - embeds colons
# when transformed to yaml, the yaml format breaks.  using the yaml pipe "|" character
# promised to work around them, making the yaml loadable, for conversion to html
def test_toYAML_tlingitFunnyCharacters():
    
    print("--- test_toYAML_tlingitFunnyCharacters")
    f = "../testData/validEafYamlFiles/4EthelAnita230503Slexil.eaf"
    parser = EafParser(f, verbose=False, fixOverlappingTimeSegments=False)
    parser.run()
    yamlText = parser.toYAML("Ethel & Anita", "Ethel, Anita, Roberta", "Alice Taff")
    fOut = "/tmp/4EthelAnita230503Slexil.yaml"
    parser.writeYAML(yamlText, fOut)
    x = yaml.load(open(fOut), Loader=yaml.CLoader)

       # these all fail:
       #
       #  84: translation: Ask her: "What is this?"
       # 234: translation: {Their} their artwork that is right here.
       # 253: translation: "tʼukanéiyi" is a
       # 271: utterance: "But I learned, I donʼt know where I learned "kay," you know, instead of "okay." I used to say, "kay." And they used to get so mad at me."
       # 311: translation: [name],
       # 415: translation: [name] Yes.

#---------------------------------------------------------------------------------------------------
def test_toYAML_inferno3():

    print("--- test_toYAML_inferno3")

    f = "../testData/validEafYamlFiles/inferno-threeLines.eaf"
    parser = EafParser(f, verbose=False, fixOverlappingTimeSegments=False)
    parser.run()
    yaml = parser.toYAML("Dante's Inferno", "Roberto Benigni", "Paul Shannon")

    expected = ["title: Dante's Inferno",
     'narrator: Roberto Benigni',
     'textEntry: Paul Shannon',
     'mediaFile: https://slexildata.artsrn.ualberta.ca/misc/inferno-threeLines.wav',
     'mimeType: audio/x-wav',
     '',
     'lines:',
     '  - lineNumber: 1',
     '    startTime: 0',
     '    endTime: 2828',
     '    italianSpeech: |\n         Nel mezzo del cammin di nostra vita',
     '    morphemes: |\n         [en=il,mezz–o,de=il,cammin–Ø,di,nostr–a,vit–a]',
     '    morpheme-gloss: |\n         [in=DEF:MASC:SG,middle-MASC:SG,of=DEF:MASC:SG,journey–MASC:SG,of,our-FEM:SG,life-FEM]',
     '    english: |\n         Midway upon the journey of our life',
     '',
     '  - lineNumber: 2',
     '    startTime: 3095',
     '    endTime: 5500',
     '    italianSpeech: |\n         mi ritrovai per una selva oscura',
     '    morphemes: |\n         [mi,ritrov–ai,per,una,selv–a,oscur–a]',
     '    morpheme-gloss: |\n         [I:DAT,found–1SG:INDEF:REM:PAST,for,INDEF:FEM:SG,forest-FEM,dark–FEM:SG]',
     '    english: |\n         I found myself within a forest dark',
     '',
     '  - lineNumber: 3',
     '    startTime: 5624',
     '    endTime: 8033',
     '    italianSpeech: |\n         ché la diritta via era smarrita.',
     '    morphemes: |\n         [ché,la,diritt–a,vi–a,era,smarr–it–a]',
     '    morpheme-gloss: |\n         [that,def:FEM:SG,straight-FEM:SG,path-FEM,be:3SG:IMPF,lose–PARTIC–FEM:SG]',
     '    english: |\n         For the straightforward pathway had been lost.',
     '']

    assert(yaml == expected)

    
#--------------------------------------------------------------------------------
def test_toYAML_daylightFull():

    print("--- test_toYAML_daylightFull")

    f = "../testData/validEafYamlFiles/daylight.eaf"
    parser = EafParser(f, verbose=False, fixOverlappingTimeSegments=False)
    parser.run()
    yaml = parser.toYAML("Daylight", "Harry Moses", "Paul Shannon")

#---------------------------------------------------------------------------------------------------
# donkeyTiger has two time-aligned unparented tiers, each with 1 descendent tier with
# comparable line count.  igore the others
#
#   TIER_ID PARENT_REF LINES	LINGUISTIC_TYPE_REF	TIME_ALIGNABLE
#   ref@VG		        117	   ref	               true
#   ref@AM		        117	   ref	               true
#   to@VG	ref@VG	  117	   to	                  false
#   to@AM	ref@AM	  117	   to	                  false
#   ot@VG	ref@VG	  22	   ot	                  false
#   ot@AM	ref@AM	  22	   ot	                  false
#   ft@VG	ref@VG	  22	   ft	                  false
#   ft@AM	ref@AM	  22	   ft	                  false
#
def test_donkeyTiger():

   print("--- test_donkeyTiger")
   f = "../testData/validEafYamlFiles/084_TheWomanOfTheWater-DonkeyTiger.eaf"
   parser = EafParser(f, verbose=False, fixOverlappingTimeSegments=False)
   parser.run()

#---------------------------------------------------------------------------------------------------
# featherSnake has one time-aligned unparented tier, 3 direct children with
# same (or nearly the same) number of lines
# so a simplified version, easy to yaml-ify, drops that 141 last tier
#
#   TIER_ID	              PARENT_REF	    LINES	LINGUISTIC_TYPE_REF	TIME_ALIGNABLE
#   TRS-Ortho		                           15	   default-lt	         true
#   TRS Broad IPA	         TRS-Ortho	      15	   TRS-Broad	         false
#   Free Translation	      TRS-Ortho	      15	   Free Translation	   false
#   Tokenization-cp	      TRS-Ortho	      141	Tokenization 2	      false
#   Tokenization-Gloss-cp	Tokenization-cp	141	POS	false
def test_featherSnake():

   print("--- test_featherSnake")

   f = "../testData/validEafYamlFiles/featherSnake.eaf"
   parser = EafParser(f, verbose=False, fixOverlappingTimeSegments=False)
   parser.run()
   
#---------------------------------------------------------------------------------------------------
def test_richTierTable():

   print("--- test_richTierTable")

   eafs = ["inferno-threeLines.eaf",
           "4EthelAnita230503Slexil.eaf",
           "natalia-yekwana.eaf",
           "186_TheShaman.eaf",
           "084_TheWomanOfTheWater-DonkeyTiger.eaf",
           "featherSnake.eaf",
           "doreco_arap1274_20_Crawford.eaf"]
   eaf = eafs[5]
   eafFile = "/Users/paul/github/slexil2/testData/validEafYamlFiles/%s" % eaf
   parser = EafParser(eafFile, verbose=False, fixOverlappingTimeSegments=False)
   #parser.constructRichTierTable()
   (t,t2) = parser.getRichTierTables()
   assert(t.shape == (5, 6))
   assert(t2.shape == (3, 6))
   tbl0 = parser.getLineTable(0)
   assert(tbl0.shape == (3, 8))
    
#---------------------------------------------------------------------------------------------------
def test_alice61_misorderedTiers():

   print("--- test_alice61_misorderedTiers")
   eafFile = "/Users/paul/github/slexil2/explore/aliceTaff/61/61Margaretmarsha230619Slexil.eaf"
   p = EafParser(eafFile, verbose=False, fixOverlappingTimeSegments=False)
   p.run()
   tbl = p.getLineTable(2)
   yamlLines = p.toYAML("a", "b", "c")
   yamlSubset = yamlLines[:25]  # up to and including line 3
   yamlFile = "/tmp/61.yaml"
   p.writeYAML(yamlSubset, yamlFile)

   from slexil.yamlToText import YamlToText

   text = YamlToText(yamlFile,
                     grammaticalTerms=[],
                     projectDirectory="./",
                     verbose = False,
                     fontSizeControls = True,
                     startLine = None,
                     endLine = None,
                     pageTitle = eafFile,
                     helpFilename = None,
                     helpButtonLabel = None,
                     kbFilename = None,
                     linguisticsFilename = None,
                     fixOverlappingTimeSegments = False,
                     webpackLinksOnly=False,
                     useTooltips=False)
   htmlText = text.toHTML()
   htmlFileName = "61.html"
   print("--- writing html file for at %s" % htmlFileName)
   with open(htmlFileName, "w") as file:
       file.write(htmlText)
    
#---------------------------------------------------------------------------------------------------
def exploreYamlColonAndCharacterCollisions():

   s = """lines:
  - lineNumber: 1
    startTime: 0
    endTime: 2828
    italianSpeech: |
         Nel mezzo del cammin di nostra vita
    morphemes: >
         [en=il,mezz–o,de=il,cammin–Ø,di,nostr–a,vit–a]
    morpheme-gloss: |
         [in=DEF:MASC:SG,middle-MASC:SG,of=DEF:MASC:SG,journey–MASC:SG,of,our-FEM:S\
G,life-FEM]
    english: |
         Midway upon the journey of our life
         """

#---------------------------------------------------------------------------------------------------
# in an early version, morpheme & gloss (analysis) lines were identified by the
# presence of tabs in the text of the tiered line.
# that's too lenient: a single tab in the translation lines was enough
# to judge them analysis lines.   now tabs are counted per tier across
# the entire eaf file.  an average of at least 2 tabs per line across
# the file is needed; that is, an average of 3 morphemes and glosses
# for each spoken line.
def test_basil():

    print("--- test_basil")
    f = "../testData/validEafYamlFiles/from-dbeckServer/bugs/basil.eaf"
    p = EafParser(f, verbose=False, fixOverlappingTimeSegments=False)
    p.run()
    #p.findTiersWithTabs()
    assert(p.tiersWithTabs == [])
    tbl = p.getLineTable(1)   # first line in the story

    assert(tbl['tierID'].values[3] == "translation")
    translation = tbl['text'][3]
   
    assert(translation == "Do you know about munmaanta'qw?")
    y = p.toYAML("Basil", "speaker", "transcriber")


    pyObj = yaml.safe_load("\n".join(y[7:12]))  
    # pprint.pp(pyObj)

       # inspect the first line's tranlsation
    assert(pyObj[0]["translation"] == "Do you know about munmaanta'qw?")
       # now get that line directly
    assert(p.lineToYAML(tbl, 0)[4] ==
           "    translation: |\n         Do you know about munmaanta'qw?")

#---------------------------------------------------------------------------------------------------
# a degenerate 2 tier eaf, just one line, second tier unlinked to first
def test_p05():

    print("--- test_p05")

    f = "../testData/validEafYamlFiles/from-dbeckServer/bugs/p05_s18_n170.eaf"
    p = EafParser(f, verbose=False, fixOverlappingTimeSegments=False)
    p.run()
    assert(p.tiersWithTabs == [])
    tbl = p.getLineTable(1)   # first line in the story

    assert(tbl.shape == (1,8))
    onlyText = tbl['text'][0]
    assert(onlyText == 'REVISAR(M-CI)')
    y = p.toYAML("p05", "unknown", "unknown")
    pyObj = yaml.safe_load("\n".join(y))
    # pprint.pp(pyObj)
    assert(pyObj == {'title': 'p05',
                     'narrator': 'unknown',
                     'textEntry': 'unknown',
                     'mediaFile': './p05_18_n170.mp4',
                     'mimeType': 'video/mp4',
                     'lines': [{'lineNumber': 1,
                                'startTime': 118,
                                'endTime': 998,
                                'M_Glosa': 'REVISAR(M-CI)\n'}]})

#---------------------------------------------------------------------------------------------------
# where "yes" is somehow rendered as True
def test_jitz_yesAsTrue():

    print("--- test_jitz_yesAsTrue")

    f = "../testData/invalidEafFiles/JITZ.eaf"
    p = EafParser(f, verbose=False, fixOverlappingTimeSegments=False)
    p.run()
    p.toYAML("a","b", "c")

#---------------------------------------------------------------------------------------------------
def test_craneCom():

    print("--- test_craneCom")

    f = "../testData/validEafYamlFiles/from-dbeckServer/bugs/Crane_COM_TS_RP.eaf"
    p = EafParser(f, verbose=False, fixOverlappingTimeSegments=False)
    p.run()

    assert(len(p.tiersWithTabs) == 2)
    assert("morphemes" in p.tiersWithTabs)
    assert("morphemeGloss" in p.tiersWithTabs)

    tbl = p.getLineTable(1)   # first line in the story
    y = p.lineToYAML(tbl, 1)
    pyObj = yaml.safe_load("\n".join(y))
    # pprint.pp(pyObj)

    assert(tbl.shape == (4,8))
    onlyTextFirstLine = tbl['text'][0]
    assert(onlyTextFirstLine == 'nilh kwthu smuqw’a’ nu sxwi’em’.')
    y = p.toYAML("p05", "unknown", "unknown")
    pyObj = yaml.safe_load("\n".join(y))
    # pprint.pp(pyObj)

#--------------------------------------------------------------------------------
# empty in the sense that, though valid xml, there are no time-aligned tiers
def test_noTimeAlignedTierLines():

    print("--- test_noTimeAlignedTierLines")
    f = "../testData/validEafYamlFiles/from-dbeck/2016-08-25_ErnestinaVelasquez_McKayTrec-533.eaf"
    caughtException = False

    try:
       parser = EafParser(f, verbose=False, fixOverlappingTimeSegments=False)
       parser.xmlValid()
       parser.run()
    except NoTimeAlignedTierLines as e:
       caughtException = True

    assert(caughtException)

#--------------------------------------------------------------------------------
def runTests():

   test_lineToYAML_multipleTabsSeparatingTokens()
   test_lineToYAML_yesBecomesTrue()
   test_craneCom()
   test_p05()
   test_basil()
   test_ctor()
   test_getLineTable()
   test_toYAML_inferno3()
   test_toYAML_daylightFull()

     # exploreYamlColonAndCharacterCollisions()
   test_xmlValidity_notMemberFunction()
   test_extractAllRootTimeAlignedTiers()
   
   print("--- all done with root test")
   
   test_donkeyTiger()
   test_featherSnake()

   test_parsingSpeed()
   test_invalidXmlRaisesException_misnamedParentRef()
   test_invalidXmlRaisesException_misnamedTierType()
   test_invalidXmlRaisesException_misspelledTag()

   test_tierTable_0()
   test_timeTable()
   test_richTierTable()
   test_checkAgainstTierGuide()
   test_depthFirstTierTraversal()
   test_parseAllLines()
   
   test_sortLinesByTime_inferno()
   test_sortLinesByTime_natalia()
   test_tedsBlueJay()
   test_fixOverlappingTimes()  # very slow
   test_variousGetters()
   test_getSummary()

   test_toYAML_tlingitFunnyCharacters()
   test_noTimeAlignedTierLines()

#---------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    runTests()
 
