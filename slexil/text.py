'''
******************************************************************
SLEXIL—Software Linking Elan XML to Illuminated Language
Copyright (C) 2019 Paul Shannon and David Beck

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

The full version of the GNU General Public License is found at
<https://www.gnu.org/licenses/>.

Information about the software can be obtained by contacting
david.beck at ualberta.ca.
******************************************************************
'''

# text.py: a class to represent a complete IJAL interlinear text, and to transform its
# represention in ELAN xml (eaf) format, accompanied by audio, into html
#----------------------------------------------------------------------------------------------------
# import re
# import sys
import os
from yattag import *
import yaml
from ijalLine import *
pd.set_option('display.width', 1000)
import pdb
import logging
import identifyLines

#----------------------------------------------------------------------------------------------------
# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------------------------------------------------
class Text:

	xmlFilename = ''
	grammaticalTermsFile = None
	grammaticalTerms = []
	xmlDoc = None
	htmlDoc = None
	lineCount = 0
	quiet = True

	def __init__(self, xmlFilename, grammaticalTermsFile, tierGuideFile, projectDirectory, lineNumberForDebugging=None, quiet=True):
		self.xmlFilename = xmlFilename
		self.grammaticalTermsFile = grammaticalTermsFile
		self.tierGuideFile = tierGuideFile
		self.projectDirectory = projectDirectory
		self.validInputs()
		self.lineNumberForDebugging = lineNumberForDebugging
		self.quiet = quiet
		self.xmlDoc = etree.parse(self.xmlFilename)
		self.metadata = self.extractMetadata()
		self.extractMediaInfo()
		with open(tierGuideFile, 'r') as f:
			self.tierGuide = yaml.safe_load(f)
		self.speechTier = self.tierGuide['speech']
		self.speechTierList = identifyLines.getList(self.xmlDoc,self.tierGuide)
		self.lineCount = len(self.speechTierList)
		if os.path.isfile(os.path.join(projectDirectory,"ERRORS.log")):
			os.remove(os.path.join(projectDirectory,"ERRORS.log"))
		logging.basicConfig(filename=os.path.join(projectDirectory,"ERRORS.log"),format="%(levelname)s %(message)s")
		logging.getLogger().setLevel(logging.WARNING)
		targetDirectory = os.path.join(projectDirectory,"audio")

	def extractMetadata(self):
		properties = self.xmlDoc.findall("HEADER")[0].findall("PROPERTY")
		metadata = {}
		for prop in properties:
			name = prop.attrib["NAME"]
			if("metadata:" in name):
				name = name.replace("metadata:","")
				value = prop.text
				metadata[name] = value
		return(metadata)

	def extractMediaInfo(self):
		# todo: test for the presence of these elements and the attributes
		x = self.xmlDoc.findall("HEADER")[0].findall("MEDIA_DESCRIPTOR")[0]
		self.mediaURL = x.attrib["MEDIA_URL"]
		self.mediaMimeType = x.attrib["MIME_TYPE"]
		#print("media url: %s" % self.mediaURL)
		#print("mimeType:  %s" % self.mediaMimeType)
		
	def getMediaInfo(self):
		return({"url": self.mediaURL,  "mimeType": self.mediaMimeType})
		
	def getTierSummary(self):
		tmpDoc = etree.parse(self.xmlFilename)
		tierIDs = [tier.attrib["TIER_ID"] for tier in tmpDoc.findall("TIER")]
		tiers = tmpDoc.findall("TIER")
		#print(self.tierGuide)
		itemList = pd.DataFrame(list(self.tierGuide.items()), columns=['key', 'value'])
		tbl = itemList[:-1].copy()
		#print(tbl)
		#tbl = pd.DataFrame(list(self.tierGuide.items()), columns=['key', 'value']).ix[0:3]
		tierValues = tbl["value"].tolist()
		tblSize = len(tierValues)
		countList = []
		for i in range(0,tblSize):
			countList.append(0)
		tbl['count'] = countList
		#tbl['count'] = [0, 0, 0, 0]
		for i in range(tblSize):
			try:
				#exception raised by None tiers
				tier = tiers[i]
				tierValue = tierValues[i]
				tierID = tier.attrib["TIER_ID"]
				count = len(tier.findall("ANNOTATION"))
				#pdb.set_trace()
				rowNumber = tbl[tbl['value']==tierValue].index
				#tbl.ix[rowNumber, 'count'] = count
				tbl.iloc[rowNumber, tbl.columns.values.tolist().index('count')] = count
			#print(" %30s: %4d" % (tierID, count))
			except IndexError:
				break
		self.tierTable = tbl
		return(tbl)

	def determineStartAndEndTimes(self):
		# print("entering determine start and end times")
		xmlDoc = etree.parse(self.xmlFilename)
		timeSlotElements = xmlDoc.findall("TIME_ORDER/TIME_SLOT")
		timeIDs = [x.attrib["TIME_SLOT_ID"] for x in timeSlotElements]
		times = [int(x.attrib["TIME_VALUE"]) for x in timeSlotElements]
		audioTiers = xmlDoc.findall("TIER/ANNOTATION/ALIGNABLE_ANNOTATION")
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
		# still need to rename, maybe also reorder columns
		tbl.columns = ["lineID", "t1", "start", "t2", "end"]
		list(tbl.columns)
		tbl = tbl[["lineID", "start", "end", "t1", "t2"]]
		#        tbl = tbl.sort('start')
		self.startStopTable = self.makeStartStopTable(tbl)
		# print("+++\n",tbl,"\n+++")
		return (tbl)


	def makeStartStopTable(self, annotations):
		self.audioTable = []
		startStopTimes = "window.timeStamps=["
		for i,annotation in enumerate(annotations):
			start = annotation[0]
			end = annotation[1]
			entry = "{ 'id' : '%s', 'start' : %s, 'end' : %s},\n" %(str(i+1),start,end)
			startStopTimes += entry
			self.audioTable.append(annotation)
		startStopTimes = startStopTimes[:-1] + "]"
		# print(startStopTimes)
		return(startStopTimes)

	def validInputs(self):
		try:
			assert(os.path.isfile(self.xmlFilename))
		except AssertionError as e:
			raise Exception(self.xmlFilename) from e
		try:
			assert(os.path.isfile(self.tierGuideFile))
		except AssertionError as e:
			raise Exception(tierGuideFile)from e
		# the audioPath points to a relative directory "./audio" in which wav files are found
		# but without a handle on the project directory, we cannot easily test this
		# skip it for now
		if(not self.grammaticalTermsFile == None):
			try:
				assert(os.path.isfile(self.grammaticalTermsFile))
			except AssertionError as e:
				raise Exception(self.grammaticalTermsFile) from e
			# parse the terms in _makeAbbreviations, read in a single line here
			grammaticalTerms_raw = open(self.grammaticalTermsFile).read()
			assert(len(grammaticalTerms_raw) > 0)
			self.grammaticalTerms = _makeAbbreviationListLowerCase(grammaticalTerms_raw)
		return(True)

	def getLineAsTable(self, lineNumber):
		audioData = lineNumber+1 #self.audioTable[int(lineNumber)]
		print("audio data: %s" %audioData)
		x = IjalLine(self.xmlDoc, lineNumber, self.tierGuide, audioData, quiet=self.quiet)
		x.parse()
		return(x.getTable())

	def traverseStructure(self):
		lineNumbers = range(self.lineCount)
		for i in lineNumbers:
			x = IjalLine(self.xmlDoc, i, self.tierGuide, quiet=self.quiet)
			x.parse()
			tbl = x.getTable()
			print("%d: %d tiers" % (i, tbl.shape[0]))

	def getCSS(self):
		cssFilename = "slexil.css"
		#assert(os.path.exists(cssFilename))
		css = '<link rel = "stylesheet" type = "text/css" href = "%s" />' % cssFilename
		return(css)

	def getJQuery(self):
		scriptTag = '<script src="https://code.jquery.com/jquery-3.6.3.min.js"></script>\n'
		#scriptTag = '<script src="jquery-3.3.1.min.js"></script>\n'
		return(scriptTag)

	def getBootstrap(self):
		style = """<link rel="stylesheet"
  href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css"
  integrity="sha384-rbsA2VBKQhggwzxH7pPCaAqO46MgnOM80zW1RWuH61DGLwZJEdK2Kadq2F9CUG65"
  crossorigin="anonymous">"""
		script_1 = '<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.min.js"></script>'
		script_2 = '<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.bundle.min.js"></script>'
		scriptTag = "%s\n%s\n%s" % (style, script_1, script_2)
		return(scriptTag)


	def getJavascript(self,timeCodesForText):
		startStopTimes = self.makeStartStopTable(timeCodesForText)
		jsSource = '<script src="slexil.js"></script>\n'
		jsSource += '<script type="text/javascript">%s</script>\n' %startStopTimes
		return(jsSource)

	def getPlayer(self):
		mimeType = self.getMediaInfo()["mimeType"]
		try:
			mimeType in ["audio/x-wav", "video/m4v"]
		except:
			sys.exit(1)
		url = self.getMediaInfo()["url"]
		if(mimeType in ["audio/x-wav", "audio/mp3"]):
			playerDiv = '<audio class="player" id="mediaPlayer" src="%s" controls></audio>' % url
		if(mimeType in ["video/m4v"]):
			playerDiv = '<video class="player" id="mediaPlayer" src="%s" controls></video>' % url
		return playerDiv

	def toHTML(self, lineNumber=None):
		htmlDoc = Doc()
		timeCodesForText = []
		if(lineNumber == None):
			lineNumbers = range(self.lineCount)
		else:
			lineNumbers = [lineNumber]
		if(not self.lineNumberForDebugging == None):
			lineNumbers = [self.lineNumberForDebugging]
		htmlDoc.asis('<!DOCTYPE html>')
		#pdb.set_trace()
		with htmlDoc.tag('html', lang="en"):
			with htmlDoc.tag('head'):
				htmlDoc.asis('<meta charset="UTF-8"/>')
				htmlDoc.asis(self.getJQuery())
				htmlDoc.asis(self.getBootstrap())
				htmlDoc.asis(self.getCSS())
				htmlDoc.asis("<!-- headCustomizationHook -->")
			with htmlDoc.tag('body'):
				aboutBoxNeeded = False
				with htmlDoc.tag("div", id="infoDiv"):
					with htmlDoc.tag("div", id="titleRow", klass="row"):
						with htmlDoc.tag("div", klass="col-md-10 col-12"):
							if ("Title" in self.metadata.keys()):
								with htmlDoc.tag("h3", id="h3Title"):
									title = self.metadata["Title"]
									htmlDoc.asis(title)
						aboutBoxNeeded = optionallyAddAboutButton(htmlDoc, self.metadata)
					if(aboutBoxNeeded):
						addAboutBox(htmlDoc, self.metadata)

				htmlDoc.asis("<!-- bodyTopCustomizationHook -->")
				with htmlDoc.tag("div", id="mediaPlayerDiv"):
					htmlDoc.asis(self.getPlayer())
				with htmlDoc.tag("div", id="textDiv"):
					for i in lineNumbers:
						if(not self.quiet):
						        print("line %d/%d" % (i, self.lineCount))
						line = IjalLine(self.xmlDoc, i, self.tierGuide, self.grammaticalTerms, quiet=self.quiet)
						line.parse()
						start = line.getStartTime()
						end = line.getEndTime()
						timeCodesForLine = [start,end]
						timeCodesForText.append(timeCodesForLine)
						id = line.getAnnotationID()
						#self.audio.makeLineAudio(i, id, start, end)
						with htmlDoc.tag("div",  klass="line-wrapper", id=i+1):
							tbl = line.getTable()
							#lineID = tbl.ix[0]['ANNOTATION_ID']
							# lineID = tbl.iloc[0][tbl.columns.values.tolist().index('ANNOTATION_ID')]
							with htmlDoc.tag("div", klass="line-sidebar"):
								line.htmlLeadIn(htmlDoc) # , self.audioPath, self.audioFileType)
								s = f"<!-- sidebarHookLine_{i+1} -->"
								htmlDoc.asis(s)
							line.toHTML(htmlDoc)
				with htmlDoc.tag("div", klass="spacer"):
					htmlDoc.asis('')
				htmlDoc.asis(self.getJavascript(timeCodesForText))
				htmlDoc.asis("<!-- bodyBottomCustomizationHook -->")
		self.htmlDoc = htmlDoc
		self.htmlText = htmlDoc.getvalue()
		return(self.htmlText)

#--------------------------------------------------------------------------------
def optionallyAddAboutButton(htmlDoc, metadata):

	if(not "Title" in metadata.keys()):
		return(False)

	if("Title" in metadata.keys()):  # no metadata beyond Title: skip
		if(len(metadata) == 1):
			return(False)

	with htmlDoc.tag("div", klass="col-md-2 col-12"):
		with htmlDoc.tag("button",
							  ('data-bs-toggle','modal'),
							  ('data-bs-target', '#aboutModalDialog'),
							  klass="btn btn-primary"):
			htmlDoc.text('About')

	return(True)

#--------------------------------------------------------------------------------
def addAboutBox(htmlDoc, metadata):

	with htmlDoc.tag("div",
		('tabindex', "-1"),
		('aria-labelledby', "modalLabel"),
		('aria-hidden', "true"),
		klass="modal fade", id="aboutModalDialog"):
			with htmlDoc.tag("div", klass="modal-dialog modal-lg"):
				with htmlDoc.tag("div", klass="modal-content"):
					with htmlDoc.tag("div", klass="modal-body"):
						if(len(metadata.keys()) > 0):
							for topic in metadata.keys():
								with htmlDoc.tag("h1"):
									htmlDoc.text("%s:" % topic)
								htmlDoc.text(metadata[topic])
								htmlDoc.tag("p")
								htmlDoc.tag("br")
								htmlDoc.tag("br")
											  
#---------------------------------------------------------------
def _makeAbbreviationListLowerCase(grammaticalTerms):
	''' ensures grammatical terms in user list are lower case '''
	exceptions  = ["A","S","O","P"]
	newTerms = []
	grammaticalTerms = grammaticalTerms.replace(".","\n")
	grammaticalTerms = grammaticalTerms.replace("<sub>","\n")
	grammaticalTerms = grammaticalTerms.replace("</sub>","\n")
	grammaticalTerms = grammaticalTerms.replace("<sup>","\n")
	grammaticalTerms = grammaticalTerms.replace("</sup>","\n")
	grammaticalTerms = grammaticalTerms.replace("<sub>","\n")
	grammaticalTerms = grammaticalTerms.replace("\n\n","\n")
	terms = grammaticalTerms.split("\n")
	#print()terms
	'''first run through needs to deal with super/subscripts'''
	for term in terms:
		term = term.strip()
		if term in exceptions:
			newTerms.append(term)
		elif term.isupper():
			newTerm = term.lower()
			newTerms.append(newTerm)
		else:
			newTerms.append(term)
	#print(newTerms)
	uniqueTerms = list(set(newTerms))
	#print(uniqueTerms)
	return(uniqueTerms)

