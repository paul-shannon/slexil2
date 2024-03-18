# -*- tab-width: 3 -*-
#-------------------------------------------------------------------------------
import os, sys
import xmlschema
#from xml.etree import ElementTree as etree
from lxml import etree
import yaml
import pandas as pd
pd.set_option('display.width', 1000)
import pdb
#-------------------------------------------------------------------------------
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
class EafParser:

	xmlFilename = ''
	doc = None
	lineCount = None
	tierTable = None
	timeTable = None
	lineTable = None
	linesAll = list()
	verbose = False
	metadata = None
	mediaURL = None
	mediaMimeType = None
	fixOverlappingTimeSegments = False

	def __init__(self, xmlFilename, verbose, fixOverlappingTimeSegments):

		self.xmlFilename = xmlFilename
		self.verbose = verbose
		self.fixOverlappingTimeSegments = fixOverlappingTimeSegments
		valid = self.xmlValid()
		self.doc = etree.parse(xmlFilename)
		self.extractMetadata()
		self.extractMediaInfo()
		self.lineCount = len(self.doc.findall("TIER/ANNOTATION/ALIGNABLE_ANNOTATION"))
		self.constructTierTable()
		self.constructTimeTable()
		# self.parseAllLines()

	#----------------------------------------------------------------------------------
	def xmlValid(self):
		assert(len(self.xmlFilename) > 4)
		#baseDir = "/Users/paul/github/slexil2/testData"
		#schemaFile = os.path.join(baseDir, "EAFv3.0.xsd")
		#assert(os.path.isfile(schemaFile))
		schemaFile = "http://www.mpi.nl/tools/elan/EAFv3.0.xsd" 
		valid = False
		#try:
		if(self.verbose):
			print("--- about to call xmlschema.validate")
		xmlschema.validate(self.xmlFilename, schemaFile)
		if(self.verbose):
			print("--- after call xmlschema.validate")
		return(True)
		#valid = True
		#except xmlschema.validators.exceptions.XMLSchemaValidationError as e:
	   #	print("error")
		#	print(e)
		#return(valid)

		
	#----------------------------------------------------------------------------------
	def getFilename(self):
		return(self.xmlFilename)
	def getLineCount(self):
		return(self.lineCount)
	def getMetadata(self):
		return(self.metadata)
	def getMediaInfo(self):
		return({"url": self.mediaURL, "mimetype": self.mediaMimeType})
	def getTierTable(self):
		return(self.tierTable)
	def getTimeTable(self):
		return(self.timeTable)
	def getAllLinesTable(self):
		return(self.linesAll)

	#----------------------------------------------------------------------------------
	def checkAgainstTierGuide(self, tierGuideFile):

		tierElements = self.doc.findall("TIER")
		tierIDs = [tier.attrib["TIER_ID"] for tier in tierElements]
		with open(tierGuideFile, 'r') as f:
			tierGuide = yaml.safe_load(f)
		documentedTierIDs = list(tierGuide.values())
		undocumentedInXmlFile = list(set(documentedTierIDs).difference(set(tierIDs)))
		valid = (undocumentedInXmlFile == [])
		return ({"valid": valid, "failures": undocumentedInXmlFile})

#		try:
#		assert(len(undocumentedInXmlFile) == 0)
#	      except AssertionError as e:
#		msg = "unrecognized tierIDs in eaf file: "
#	         for unknown in undocumentedInXmlFile:
#            unknowns = "%s %s" % (unknowns, unknown)
#         msg = "%s %s" % (msg, unknowns)
#         raise Exception(msg)
            
	#----------------------------------------------------------------------------------
	def extractMetadata(self):
		if (self.verbose):
			print("--- entering extractMetadata")
		properties = self.doc.findall("HEADER")[0].findall("PROPERTY")
		metadata = {}
		for prop in properties:
			name = prop.attrib["NAME"]
			if("metadata:" in name):
				name = name.replace("metadata:","")
				value = prop.text
				metadata[name] = value
		self.metadata = metadata

	#--------------------------------------------------------------------------------	
	def extractMediaInfo(self):
		if(self.verbose):
			print("--- entering extractMediaInfo")
		# todo: test for the presence of these elements and the attributes
		x = self.doc.findall("HEADER")[0].findall("MEDIA_DESCRIPTOR")[0]
		self.mediaURL = x.attrib["MEDIA_URL"]
		self.mediaMimeType = x.attrib["MIME_TYPE"]

	#--------------------------------------------------------------------------------	
	def constructTierTable(self):

		   # first get the possible LINGUISTIC_TYPE_REFS.  each tier must have this
		types = self.doc.findall("LINGUISTIC_TYPE")
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
				
		tiers = self.doc.findall("TIER")
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
		self.tierTable = tbl.drop(columns=["LINGUISTIC_TYPE_ID"]) # redundant after merge

	#----------------------------------------------------------------------------------
    # def testParentTierReferences(self):
    #   # get the unique ids of supposed parents.  the first tier has no parent
    #
    #    allFound = True
    #
    #    for ref in parentReferences:
    #
    #       if not found:
    #
    #          missing.append(ref)#
    #        

	def constructTimeTable(self):

		timeSlotElements = self.doc.findall("TIME_ORDER/TIME_SLOT")
		timeIDs = [x.attrib["TIME_SLOT_ID"] for x in timeSlotElements]
		times = [int(x.attrib["TIME_VALUE"]) for x in timeSlotElements]
		audioTiers = self.doc.findall("TIER/ANNOTATION/ALIGNABLE_ANNOTATION")
		self.lineCount = len(audioTiers)
		audioIDs = [x.attrib["ANNOTATION_ID"] for x in audioTiers]
		tsRef1 = [x.attrib["TIME_SLOT_REF1"] for x in audioTiers]
		tsRef2 = [x.attrib["TIME_SLOT_REF2"] for x in audioTiers]
		d = {"id": audioIDs, "t1": tsRef1, "t2": tsRef2}
		tbl_t1 = pd.DataFrame({"id": audioIDs, "t1": tsRef1})
		tbl_t2 = pd.DataFrame({"id": audioIDs, "t2": tsRef2})
		tbl_times = pd.DataFrame({"id": timeIDs, "timeValue": times})
		tbl_t1m = pd.merge(tbl_t1, tbl_times, left_on="t1", right_on="id")
		tbl_t2m = pd.merge(tbl_t2, tbl_times, left_on="t2", right_on="id")
		tbl_raw = pd.merge(tbl_t1m, tbl_t2m, on="id_x")
		tbl = tbl_raw.drop(["id_y_x", "id_y_y"], axis=1)
		   # now to rename, then reorder columns
		tbl.columns = ["lineID", "t1", "start", "t2", "end"]
		tbl = tbl[["lineID", "start", "end", "t1", "t2"]]

			# to ensure clean single line playback, the start time of the
         # n+1 line must be larger than the end time of the nth line.
         # find offenders here and fix them

		if(self.fixOverlappingTimeSegments):
			starts = list(tbl["start"])
			ends = list(tbl["end"])
			rowCount = tbl.shape[0]
			for i in range(0,rowCount-1):
				if (ends[i] >= starts[i+1]):
					ends[i] = starts[i+1] - 100
			tbl["end"] = ends

		self.timeTable = tbl


	#----------------------------------------------------------------------------------
	def fixOverlappingTimeSegments(self):

		self.timeTable["end"] = ends

	#----------------------------------------------------------------------------------
	   # a hack: recursive, it works but only via visitList, at surrounding
	   # function scope.  to be improved.
	def depthFirstTierTraversal(self, parentID):
		visitList = []
		def dfs(visited, doc, annotationID):
				if(annotationID not in visitList):
						visitList.append(annotationID)
						pattern = "TIER/ANNOTATION/REF_ANNOTATION[@ANNOTATION_REF='%s']" % annotationID
						kidElements = doc.findall(pattern)
						kids = [kid.attrib["ANNOTATION_ID"] for kid in kidElements]
						for kid in kids:
								dfs(visitList, doc, kid)

		dfs(visitList, self.doc, parentID)
		visitList.remove(parentID)
		return(visitList)

	#----------------------------------------------------------------------------------
	def getLineTable(self, lineNumber):
		rowNumber = lineNumber - 1 # rows are 0-based, lines are 1-based
		x = self.doc.findall('TIER/ANNOTATION/ALIGNABLE_ANNOTATION')[rowNumber]
		parentID = x.attrib["ANNOTATION_ID"]
		tierType = x.getparent().getparent().attrib["LINGUISTIC_TYPE_REF"]
		tierID   = x.getparent().getparent().attrib["TIER_ID"]
		xValue = x.find("ANNOTATION_VALUE")
		alignedID = x.attrib["ANNOTATION_ID"]
		timeSlotRefStart = x.attrib["TIME_SLOT_REF1"]
		timeSlotRefEnd = x.attrib["TIME_SLOT_REF2"]
		startTime = self.timeTable[self.timeTable['t1'] == timeSlotRefStart]["start"].tolist()[0]
		endTime = self.timeTable[self.timeTable['t2'] == timeSlotRefEnd]["end"].tolist()[0]
		contents = xValue.text
		tbl = pd.DataFrame({"id": alignedID,
							"parent": "",
							"startTime": startTime,
							"endTime": endTime,
							"tierID": tierID,
							"tierType": tierType,
							"text": contents}, index=[0])
		
		childIDs = self.depthFirstTierTraversal(parentID)
		#pattern = "TIER/ANNOTATION/REF_ANNOTATION[@ANNOTATION_REF='%s']" % alignedID
		#children = self.doc.findall(pattern)
		for childID in childIDs:
			searchPattern = "TIER/ANNOTATION/REF_ANNOTATION[@ANNOTATION_ID='%s']" %  childID
			#print("childID: %s  searchPattern: %s" % (childID, searchPattern))
			child = self.doc.find(searchPattern)
			tierType = child.getparent().getparent().attrib["LINGUISTIC_TYPE_REF"]
			tierID = child.getparent().getparent().attrib["TIER_ID"]
			parentID = ""
			if("ANNOTATION_REF" in child.attrib):
				parentID = child.attrib["ANNOTATION_REF"]
			childContents = child.find("ANNOTATION_VALUE").text
			nextRow = tbl.shape[0]
			tbl.loc[nextRow] = {"id": childID,
								"parent": parentID,
#								"startTime": "",
#								"endTime": "",
								"tierType": tierType,
								"tierID": tierID,
								"text": childContents}

		self.lineTable = tbl
		return(tbl)
		
	#----------------------------------------------------------------------------------
	def parseAllLines(self):

		self.linesAll = list()

		for i in range(self.getLineCount()):
			self.linesAll.append(self.getLineTable(i+1))

			# do in-place sort of self.linesAll, using startTime
			# of the time aligned tier in each line 
		def sortFunction(tbl):
			return(tbl.loc[0].startTime)

		self.linesAll.sort(reverse=False, key=sortFunction)
		
	#----------------------------------------------------------------------------------


