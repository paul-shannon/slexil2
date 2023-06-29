import unittest
import pdb
import os
from slexil import text as Text
import xmlschema
from xml.etree import ElementTree as etree
import yaml
import pandas as pd
from pathlib import Path
path = Path(".")

eafFiles = open("../testData/eafFileList.txt").read().split('\n')
if(eafFiles[-1] == ""):
	del eafFiles[-1]
print("eaf file count: %d" % len(eafFiles))

#--------------------------------------------------------------------------------
def xmlValid(eafFile):

   baseDir = "/Users/paul/github/slexil2/testData"
   schemaFile = os.path.join(baseDir, "EAFv3.0.xsd")
   assert(os.path.isfile(schemaFile))

   valid = False
   try:
      result = xmlschema.validate(eafFile, schemaFile)
      valid = True
   except xmlschema.validators.exceptions.XMLSchemaValidationError as e:
      print("error")
      print(e)

   return(valid)

#--------------------------------------------------------------------------------
def linguisticTypeInfo(xmlDoc):
    elements = xmlDoc.findall("LINGUISTIC_TYPE")
    for element in elements:
       attributes = element.attrib.keys()
       for attrib in attributes:
          value = element.attrib[attrib]
          print("    %s: %s" % (attrib, value))
       print ()
#--------------------------------------------------------------------------------
def tierInfo(xmlDoc):
	
    tiers = xmlDoc.findall("TIER")
    for tier in tiers:
       attributes = tier.attrib.keys()
       for attrib in attributes:
          value = tier.attrib[attrib]
          print("    %s: %s" % (attrib, value))
       print()

#--------------------------------------------------------------------------------
def createTierTable(xmlDoc):

       # first get the possible LINGUISTIC_TYPE_REFS.  each tier must have this
    types = xmlDoc.findall("LINGUISTIC_TYPE")
    attributeNamesRaw = [list(type.attrib.keys()) for type in types]
    attributeNamesWithDups = [item for sublist in attributeNamesRaw for item in sublist]
    attributeNames = list(set(attributeNamesWithDups)) # uniquify
    attributeNames.sort()

    tbl_types = pd.DataFrame(columns=attributeNames)

    row = -1
    for type in types:
       row = row + 1
       attributes = type.attrib.keys()
       for attrib in attributes:
          value = type.attrib[attrib]
          #print("    %s: %s" % (attrib, value))
          tbl_types.loc[row, attrib] = value

    tiers = xmlDoc.findall("TIER")
    attributeNamesRaw = [list(tier.attrib.keys()) for tier in tiers]
    attributeNamesWithDups = [item for sublist in attributeNamesRaw for item in sublist]
    attributeNames = list(set(attributeNamesWithDups)) # uniquify
    attributeNames.sort()

    tbl = pd.DataFrame(columns=attributeNames)

    row = -1
    for tier in tiers:
       row = row + 1
       attributes = tier.attrib.keys()
       for attrib in attributes:
          value = tier.attrib[attrib]
          tbl.loc[row, attrib] = value

    coi = ["TIER_ID", "LINGUISTIC_TYPE_REF", "PARENT_REF", "DEFAULT_LOCALE"]
    tbl = tbl.reindex(columns=coi)
    tbl = pd.merge(tbl, tbl_types,
                   left_on="LINGUISTIC_TYPE_REF", right_on="LINGUISTIC_TYPE_ID")
    tbl = tbl.drop(columns=["LINGUISTIC_TYPE_ID"]) # redundant after merge
    return(tbl)
	   
#--------------------------------------------------------------------------------
def getAllTierTables():

   for eafFile in eafFiles:
       print("--- %s: " % eafFile)
       xmlDoc = etree.parse(eafFile)
       print(createTierTable(xmlDoc))
       print("")

#--------------------------------------------------------------------------------
def validateFiles():
		
   for eafFile in eafFiles:
       print("--- %s: " % eafFile)
       print(xmlValid(eafFile))

#--------------------------------------------------------------------------------
# for eafFile in eafFiles:
# 
#    if(len(eafFile) < 10):
#       continue
#    basename = os.path.basename(eafFile)
#    print("--- %s" % basename)
#    print("    %s" % os.path.dirname(eafFile))
#    xmlDoc = etree.parse(eafFile)
#    tierIDs = [tier.attrib["TIER_ID"] for tier in xmlDoc.findall("TIER")]
#    print(tierIDs)
#    print()
# 
#    

# 		root = xmlDoc.getroot()
# 		alignedTiers = root.findall("TIER/ANNOTATION/ALIGNABLE_ANNOTATION")
# 		lineCount = len(alignedTiers)
# 		tmpTbl = ijalLine.buildTable(xmlDoc, alignedTiers)
# 		tierGuideFile = os.path.join(dataDir, "tierGuide.yaml")
# 		with open(tierGuideFile, 'r') as f:
# 			tierGuide = yaml.safe_load(f)
# 		grammaticalTerms = ["hab", "past"]
# 		for i in range(lineCount):
# 			newLine = ijalLine.IjalLine(xmlDoc, i, tierGuide, grammaticalTerms)
# 			newLine.parse()
# 			print(newLine.getSpokenText())
# 			print("   %s" % newLine.getTranslation())
# 			startTime = newLine.getStartTime()
# 			endTime = newLine.getEndTime()
# 			print("   %d - %d" % (startTime, endTime))
# 			assert(endTime - startTime > 1000)


if __name__ == '__main__':
		unittest.main()
