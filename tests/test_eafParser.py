import unittest
import pdb
import os
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

packageRoot = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dataDir = os.path.join(packageRoot, "data")

class TestEafParser(unittest.TestCase):

	def notest_ctor(self):
		print("--- test_ctor")
		f = eafFiles[3]
		parser = EafParser(f)
		self.assertEqual(parser.getFilename(), f)
		self.assertEqual(parser.xmlValid(), True)
		
	def notest_tiersTable(self):

		print("--- test_tiersTable")
		f = eafFiles[3]
		parser = EafParser(f)
		parser.constructTiersTable()
		tbl = parser.getTierTable()

		   # this is the table we expect: 
		   # TIER_ID LINGUISTIC_TYPE_REF PARENT_REF DEFAULT_LOCALE           CONSTRAINTS GRAPHIC_REFERENCES TIME_ALIGNABLE
		   # 0         utterance          default-lt        NaN            NaN                   NaN              false           true
		   # 1       translation         translation  utterance             en  Symbolic_Association              false          false
		   # 2         verb form         translation  utterance             en  Symbolic_Association              false          false
		   # 3  Speaker Initials           utterance  utterance            NaN  Symbolic_Association              false          false

		self.assertEqual(tbl.shape, (4,7))
		   # check column names
		expected = ['TIER_ID', 'LINGUISTIC_TYPE_REF', 'PARENT_REF', 'DEFAULT_LOCALE',
					'CONSTRAINTS', 'GRAPHIC_REFERENCES', 'TIME_ALIGNABLE']
		self.assertEqual(tbl.columns.values.tolist(), expected)
		   # check 1st column 
		self.assertEqual(tbl["TIER_ID"].tolist(),
						 ['utterance', 'translation', 'verb form', 'Speaker Initials'])
		self.assertEqual(tbl["TIME_ALIGNABLE"].tolist(),
						  ['true', 'false', 'false', 'false'])

		  # parent_ref column values: [nan, 'utterance', 'utterance', 'utterance'])
		  # must use 2 steps to handle nan
		self.assertEqual(np.isnan(tbl.loc[0, "PARENT_REF"]), True)
		self.assertEqual(tbl.loc[1:3, "PARENT_REF"].tolist(),
						 ['utterance', 'utterance', 'utterance'])


	def notest_timeTable(self):

		print("--- test_timeTable")
		f = eafFiles[3]
		parser = EafParser(f)
		parser.constructTimeTable()
		tbl = parser.getTimeTable()
		self.assertEqual(tbl.shape, (170,5))
		   # looks like this:
		   # tbl.loc[1:3]
		   #   lineID  start   end   t1   t2
		   # 1  a1358   1400  2475  ts3  ts4
		   # 2  a1376   2665  5090  ts5  ts6
		   # 3  a1377   5090  7530  ts7  ts8

		self.assertEqual(tbl.columns.values.tolist(),
						 ['lineID', 'start', 'end', 't1', 't2'])
		startTimes = tbl["start"].tolist()
		endTimes = tbl["end"].tolist()
		self.assertEqual(startTimes[0:3], [116,  1400, 2665])
		self.assertEqual(endTimes[0:3],   [1380, 2475, 5090])
		
	#--------------------------------------------------------------------------------
	# lines from typically all tiers are grouped with a time-aligned spoken tier
	# we need to recover all of those lines, some of which may be nested > 1 level
	# below the spoken tier line.  this recursive capability is tested here.
	def notest_depthFirstTierTraversal(self):

		print("--- test_depthFirstTierTraversal")
		f = eafFiles[0]
		parser = EafParser(f)

		nestedTierIDs = parser.depthFirstTierTraversal("a2")
		self.assertEqual(nestedTierIDs, ['a6', 'a10', 'a14'])

		  # a10 is a child of a6 (morpheme -> morphemeGloss)
		nestedTierIDs = parser.depthFirstTierTraversal("a6")
		self.assertEqual(nestedTierIDs, ['a10'])

		  # a10 is a leaf node: no children
		nestedTierIDs = parser.depthFirstTierTraversal("a10")
		self.assertEqual(nestedTierIDs, [])

		  # a1 is aligned.  it too should have 2 direct &
		  # 1 indirect children
		nestedTierIDs = parser.depthFirstTierTraversal("a1")
		self.assertEqual(nestedTierIDs, ['a5', 'a9', 'a13'])

		  # now a tlingit eaf
		  # '../explore/aliceTaff/incoming/eafs/12HelenFloBaby230503Slexil.eaf'

		f = eafFiles[12]
		print(f)
		parser = EafParser(f)
		nestedTierIDs = parser.depthFirstTierTraversal("a1")
		print(nestedTierIDs)
		#self.assertEquals(nestedTierIDs, ['a365'])


	#--------------------------------------------------------------------------------
	# a "line" is the parent time-aligned tier, and all of its associated child tiers
	def test_constructLineTable(self):

		print("--- test_constructLineTable")
		f = eafFiles[0]
		parser = EafParser(f)
		self.assertEquals(parser.getLineCount(), 3)

		parser.constructTiersTable()
		tiers = parser.getTierTable()

		parser.constructTimeTable()
		times = parser.getTimeTable()
		print(times)

		parser.constructLineTable(1)
		line = parser.getLineTable()
		print(line)

		print("---- traversing %s", eafFiles[0])
		for i in range(parser.getLineCount()):
			parser.constructLineTable(i)
			line = parser.getLineTable()
			print(line)

	#--------------------------------------------------------------------------------
	# a "line" is the parent time-aligned tier, and all of its associated child tiers
	def test_parseAllLines(self):

		print("--- test_parseAllLines")
		f = eafFiles[0]
		parser = EafParser(f)
		self.assertEqual(parser.getLineCount(), 3)
		parser.constructTiersTable()
		parser.constructTimeTable()
		parser.parseAllLines()
		x = parser.getAllLines()
		startTimes = [tbl.loc[0, "startTime"] for tbl in x]
		self.assertEqual(startTimes, [0.0, 3093.0, 5624.0])


	#--------------------------------------------------------------------------------
