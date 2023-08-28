# -*- tab-width: 4 -*-
import unittest
import pdb
import os, sys
from slexil.eafParser import EafParser
import xmlschema
from xml.etree import ElementTree as etree
import pandas as pd
import numpy as np
pd.set_option('display.width', 1000)
pd.set_option('display.max_columns', None)
from pathlib import Path
path = Path(".")

eafFiles = open("../testData/eafFileList.txt").read().split('\n')
if(eafFiles[-1] == ""):
	del eafFiles[-1]
print("eaf file count: %d" % len(eafFiles))

#---------------------------------------------------------------------------------------------------
def runTests():

	test_ctor()
	test_tierTable()
	test_timeTable()
	test_depthFirstTierTraversal()
	test_getLineTable()
	test_parseAllLines()
	test_fixOverlappingTimes()

#---------------------------------------------------------------------------------------------------
def test_ctor():

	print("--- test_ctor")
	f = eafFiles[3]
	parser = EafParser(f, verbose=False, fixOverlappingTimeSegments=False)
	assert(parser.getFilename() == f)
	assert(parser.xmlValid())

#---------------------------------------------------------------------------------------------------
def test_tierTable():

	print("--- test_tierTable")
	f = eafFiles[3]
	parser = EafParser(f, verbose=False, fixOverlappingTimeSegments=False)
	tbl = parser.getTierTable()

	   # this is the table we expect: 
	   # TIER_ID LINGUISTIC_TYPE_REF PARENT_REF DEFAULT_LOCALE           CONSTRAINTS GRAPHIC_REFERENCES TIME_ALIGNABLE
	   # 0         utterance          default-lt        NaN            NaN                   NaN              false           true
	   # 1       translation         translation  utterance             en  Symbolic_Association              false          false
	   # 2         verb form         translation  utterance             en  Symbolic_Association              false          false
	   # 3  Speaker Initials           utterance  utterance            NaN  Symbolic_Association              false          false

	assert(tbl.shape == (4,7))
	   # check column names
	expected = ['TIER_ID', 'LINGUISTIC_TYPE_REF', 'PARENT_REF', 'DEFAULT_LOCALE',
				'CONSTRAINTS', 'GRAPHIC_REFERENCES', 'TIME_ALIGNABLE']
	assert(tbl.columns.values.tolist() == expected)
	   # check 1st column 
	assert(tbl["TIER_ID"].tolist() ==
					 ['utterance', 'translation', 'verb form', 'Speaker Initials'])
	assert(tbl["TIME_ALIGNABLE"].tolist() ==
					  ['true', 'false', 'false', 'false'])

	  # parent_ref column values: [nan, 'utterance', 'utterance', 'utterance'])
	  # must use 2 steps to handle nan
	assert(np.isnan(tbl.loc[0, "PARENT_REF"]))
	assert(tbl.loc[1:3, "PARENT_REF"].tolist() ==
					 ['utterance', 'utterance', 'utterance'])


#---------------------------------------------------------------------------------------------------
def test_timeTable():

	print("--- test_timeTable")
	f = eafFiles[3]
	parser = EafParser(f, verbose=False, fixOverlappingTimeSegments=False)
	tbl = parser.getTimeTable()
	assert(tbl.shape == (170,5))
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
	assert(startTimes[0:3] == [116,  1400, 2665])
	assert(endTimes[0:3] ==   [1380, 2475, 5090])
	
#---------------------------------------------------------------------------------------------------
# lines from typically all tiers are grouped with a time-aligned spoken tier
# we need to recover all of those lines, some of which may be nested > 1 level
# below the spoken tier line.  this recursive capability is tested here.
#---------------------------------------------------------------------------------------------------
def test_depthFirstTierTraversal():

	print("--- test_depthFirstTierTraversal")
	f = eafFiles[0]
	parser = EafParser(f, verbose=False, fixOverlappingTimeSegments=False)

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
	  # '../explore/aliceTaff/incoming/eafs/12HelenFloBaby230503Slexil.eaf'

	f = eafFiles[12]  # ../explore/aliceTaff/incoming/eafs/12HelenFloBaby230503Slexil.eaf
	parser = EafParser(f, verbose=False, fixOverlappingTimeSegments=False)
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
	assert(parser.getLineCount() == 3)
	#parser.constructTierTable()
	#parser.constructTimeTable()
	parser.parseAllLines()
	x = parser.getAllLinesTable()  # a list of time-ordered line tables
	startTimes = [tbl.loc[0, "startTime"] for tbl in x]
	assert(startTimes == [0.0, 3093.0, 5624.0])


#---------------------------------------------------------------------------------------------------
# we usually want disjoint times, so that only one is selected at a time
# in manual playback.  test that optional capability here
def test_fixOverlappingTimes():

	print("--- test_fixOverlappingTimes")
	f = "../testData/overlappingTimes.eaf"
	parser = EafParser(f, verbose=False, fixOverlappingTimeSegments=False)
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
	tbl = parser.getTimeTable()
	overlaps = [tbl.iloc[i,2] >= tbl.iloc[i+1,1] for i in range(0,rowCount-1)]
	assert(pd.DataFrame(overlaps).groupby(0).size()[False] == 1131)

#---------------------------------------------------------------------------------------------------
if __name__ == '__main__':
	runTests()
