import unittest
import pdb
import os
from lxml import etree
import pandas as pd
import numpy as np
pd.set_option('display.width', 1000)
pd.set_option('display.max_columns', None)

from slexil.eafParser import EafParser
from slexil.ijalLine import IjalLine
import pdb
import yaml
import yattag
import pandas as pd
#----------------------------------------------------------------------------------------------------
pd.set_option('display.width', 1000)


#----------------------------------------------------------------------------------------------------
def runTests():

    test_inferno()

#----------------------------------------------------------------------------------------------------
filename = "../testData/inferno/inferno-threeLines.eaf"
parser = EafParser(filename)
parser.parseAllLines()
tbls = parser.getAllLinesTable()  # a list of line tables, in time order

tierGuideFile = "../testData/inferno/tierGuide.yaml"
with open(tierGuideFile, 'r') as f:
    tierGuide = yaml.safe_load(f)
grammaticalTerms = ["hab", "past"]
lineNumber = 0
tbl = tbls[lineNumber]

line = IjalLine(tbl, lineNumber, tierGuide, grammaticalTerms)
	   
assert(line.getTierCount() == 4)
assert(line.getStartTime() == 0.0)
assert(line.getEndTime() == 3093.0)
assert(line.getSpokenText() == "Nel mezzo del cammin di nostra vita")
assert(line.getTranslation() == "Midway upon the journey of our life")
assert(line.getTranslation2() == None)
line.extractMorphemes()
line.extractMorphemeGlosses()
assert(line.getMorphemes() == ["en=il", "mezz–o", "de=il", "cammin–Ø", "di",
							   "nostr–a", "vit–a"])
assert(line.getMorphemeGlosses() == ['in=DEF:MASC:SG', 'middle–MASC:SG',
									 'of=DEF:MASC:SG', 'journey–MASC:SG', 'of',
									 'our–FEM:SG', 'life–FEM'])
assert(line.getGrammaticalTerms() == ['hab', 'past'])
line.calculateMorphemeSpacing()
assert(line.getMorphemeSpacing() == [15, 15, 15, 16, 3, 11, 9])

htmlDoc = yattag.Doc()
line.toHTML(htmlDoc)
htmlText = htmlDoc.getvalue()
htmlTextIndented = yattag.indent(htmlText)

filename = "inferno.html"
f = open(filename, "wb")
f.write(bytes(htmlTextIndented, "utf-8"))
f.close()
print("wrote %s" % f.name)



#assert(tbl.shape == c(4, 14))
#expected = ['ANNOTATION_ID', 'LINGUISTIC_TYPE_REF', 'START', 'END',
#            'TEXT', 'ANNOTATION_REF', 'TIME_SLOT_REF1', 'TIME_SLOT_REF2', 
#            'PARENT_REF', 'TIER_ID', 'TEXT_LENGTH', 
#            'HAS_TABS', 'HAS_SPACES', 'category']
# assert(tbl.columns.tolist() == expected)
# assert(tbl['START'].tolist() == [0, 0, 0, 0])
# assert(tbl['END'].tolist() == [3093, 3093, 3093, 3093])

