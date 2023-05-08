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

# text.py: a class to represent a complete IJAL interlinear text, and to
# transform its
# represention in ELAN xml (eaf) format, accompanied by audio, into html
#-------------------------------------------------------------------------------
# import re
# import sys
import os, sys
from yattag import *
import yaml
from ijalLine import *
pd.set_option('display.width', 1000)
import pdb
import logging
import identifyLines

#-------------------------------------------------------------------------------
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
class Text:

	xmlFilename = ''
	grammaticalTermsFile = None
	kbFilename = None
	linguisticsFilename = None
	grammaticalTerms = []
	xmlDoc = None
	htmlDoc = None
	lineCount = 0
	verbose = False
	timeCodesForText = []

	def __init__(self,
				 xmlFilename,
				 grammaticalTermsFile,
				 tierGuideFile,
				 projectDirectory,
				 verbose,
				 fontSizeControls,
				 startLine,
				 endLine,
				 kbFilename,
				 linguisticsFilename):
		print("debug? %s" % (verbose))
		self.xmlFilename = xmlFilename
		self.grammaticalTermsFile = grammaticalTermsFile
		self.tierGuideFile = tierGuideFile
		self.projectDirectory = projectDirectory
		self.fontSizeControls = fontSizeControls
		self.kbFilename = kbFilename
		self.linguisticsFilename = linguisticsFilename
		self.validInputs()
		self.verbose = verbose
		self.xmlDoc = etree.parse(self.xmlFilename)
		self.metadata = self.extractMetadata()
		self.extractMediaInfo()
		with open(tierGuideFile, 'r') as f:
			self.tierGuide = yaml.safe_load(f)
		self.speechTier = self.tierGuide['speech']
		self.speechTierList = identifyLines.getList(self.xmlDoc,self.tierGuide)
		self.lineCount = len(self.speechTierList)
		if(self.lineCount == 0):
			print("no lines found, disagreement between tierGuide and eaf?")
			sys.exit(1)
		if(startLine != None):
			self.lineNumbers = range(startLine, endLine)
		else:
			self.lineNumbers = range(self.lineCount)
		if os.path.isfile(os.path.join(projectDirectory,"ERRORS.log")):
			os.remove(os.path.join(projectDirectory,"ERRORS.log"))
		f = os.path.join(projectDirectory, "ERRORS.log")
		logging.basicConfig(filename=f,format="%(levelname)s %(message)")
		logging.getLogger().setLevel(logging.WARNING)
		targetDirectory = os.path.join(projectDirectory,"audio")

	def extractMetadata(self):
		if (self.verbose):
			print("--- entering extractMetadata")
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
		if(self.verbose):
			print("--- entering extractMediaInfo")
		# todo: test for the presence of these elements and the attributes
		x = self.xmlDoc.findall("HEADER")[0].findall("MEDIA_DESCRIPTOR")[0]
		self.mediaURL = x.attrib["MEDIA_URL"]
		self.mediaMimeType = x.attrib["MIME_TYPE"]
		#print("media url: %s" % self.mediaURL)
		#print("mimeType:  %s" % self.mediaMimeType)

	def getMediaInfo(self):
		return({"url": self.mediaURL,  "mimeType": self.mediaMimeType})

	def getTierSummary(self):
		if(self.verbose):
			print("--- entering getTierSummary")
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
				rowNumber = tbl[tbl['value']==tierValue].index
				#tbl.ix[rowNumber, 'count'] = count
				tbl.iloc[rowNumber, tbl.columns.values.tolist().index('count')] = count
			#print(" %30s: %4d" % (tierID, count))
			except IndexError:
				break
		self.tierTable = tbl
		return(tbl)

	def determineStartAndEndTimes(self):
		if(self.verbose):
			print("--- entering determineStartAndEndTimes")
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
		print("+++\n",tbl,"\n+++")
		self.startStopTable = self.makeStartStopTable(tbl)
		return (tbl)

	def makeStartStopTable(self, annotations):
		if(self.verbose):
			print("--- entering makeStartStopTable")
		self.audioTable = []
		startStopTimes = "window.timeStamps=["
		for i,annotation in enumerate(annotations):
			start = annotation[0]
			end = annotation[1]
			entry = "{ 'id' : '%s', 'start' : %s, 'end' : %s},\n" \
					%(str(i+1),start,end)
			startStopTimes += entry
			self.audioTable.append(annotation)
		startStopTimes = startStopTimes[:-1] + "]"
		if(self.verbose):
			print("--- startStopTimes")
			print(startStopTimes)
		return(startStopTimes)

	def validInputs(self):
		if(self.verbose):
			print("--- entering validInputs")
		try:
			assert(os.path.isfile(self.xmlFilename))
		except AssertionError as e:
			raise Exception(self.xmlFilename) from e
		try:
			assert(os.path.isfile(self.tierGuideFile))
		except AssertionError as e:
			raise Exception(tierGuideFile)from e
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
		if(self.verbose):
			print("--- entering getLineAsTable")
		audioData = lineNumber+1 #self.audioTable[int(lineNumber)]
		print("audio data: %s" % audioData)
		x = IjalLine(self.xmlDoc, lineNumber, self.tierGuide, audioData, quiet=(not self.verbose))
		x.parse()
		return(x.getTable())

	def traverseStructure(self):
		if(self.verbose):
			print("--- entering traverseStructure")
		for i in self.lineNumbers:
			x = IjalLine(self.xmlDoc, i, self.tierGuide, quiet=(not self.verbose))
			x.parse()
			tbl = x.getTable()
			print("%d: %d tiers" % (i, tbl.shape[0]))

	def getCSS(self):
		if(self.verbose):
			print("--- entering getCSS")
		cssFilename = "slexil.css"
		#assert(os.path.exists(cssFilename))
		css = '<link rel = "stylesheet" type = "text/css" href = "%s" />' % cssFilename
		return(css)

	def getJQuery(self):
		if(self.verbose):
			print("--- entering getJQuery")
		scriptTag = '<script src="https://code.jquery.com/jquery-3.6.3.min.js"></script>\n'
		#scriptTag = '<script src="jquery-3.3.1.min.js"></script>\n'
		return(scriptTag)

	def getBootstrap(self):
		if(self.verbose):
			print("--- entering getBootstrap")
		style = """<link rel="stylesheet"
  href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css"
  integrity="sha384-rbsA2VBKQhggwzxH7pPCaAqO46MgnOM80zW1RWuH61DGLwZJEdK2Kadq2F9CUG65"
  crossorigin="anonymous">"""
		#script_1 = '<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.min.js"></script>'
		script_2 = '<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.bundle.min.js"></script>'
		scriptTag = "%s\n%s\n" % (style, script_2)
		return(scriptTag)


	def getJavascript(self):
		if(self.verbose):
			print("--- entering getJavascript")
		jsSource = ""
		if(self.kbFilename != None):
			jsSource += '<script src="%s"></script>\n' % self.kbFilename
		if(self.linguisticsFilename != None):
			jsSource += '<script src="%s"></script>\n' % self.linguisticsFilename
		showDownScript = "showdown.js"
		annoScript = "annotations.js"
		jsSource += '<script src="slexil.js"></script>\n'
		jsSource += '<script src="%s"></script>\n' % showDownScript
		jsSource += '<script src="%s"></script>\n' % annoScript
		startStopTimes = self.makeStartStopTable(self.timeCodesForText)
		jsSource += '<script type="text/javascript">%s</script>\n' %startStopTimes
		return(jsSource)

	def getPlayer(self):
		mimeType = self.getMediaInfo()["mimeType"]
		try:
			mimeType in ["audio/x-wav", "video/m4v", "video/mp4", "video/quicktime"]
		except:
			sys.exit(1)
		url = self.getMediaInfo()["url"]
		if(mimeType in ["audio/x-wav", "audio/mp3"]):
			playerDiv = '<audio class="player" id="mediaPlayer" src="%s" controls></audio>' % url
		if(mimeType in ["video/m4v", "video/quicktime", "video/mp4"]):
			playerDiv = '<video class="player" id="mediaPlayer" src="%s" controls></video>' % url
		return playerDiv

	def toHTML(self, lineNumber=None):
		if(self.verbose):
			print("--- entering toHTML")
		htmlDoc = Doc()
		self.timeCodesForText = []
		if(self.verbose):
			print("toHTML, lineNumber count: %d" % len(self.lineNumbers))

		htmlDoc.asis('<!DOCTYPE html>')
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
						aboutBoxNeeded = optionallyAddAboutButton(htmlDoc,
																  self.metadata)
					if(aboutBoxNeeded):
						addAboutBox(htmlDoc, self.metadata)

				htmlDoc.asis("<!-- bodyTopCustomizationHook -->")
				if(self.fontSizeControls):
					addVideoSizeSlider(htmlDoc)
				with htmlDoc.tag("div", id="mediaPlayerDiv"):
					htmlDoc.asis(self.getPlayer())
				if(self.fontSizeControls):
					addFontSizeControls(htmlDoc)
				if(self.kbFilename != None):
					if(self.verbose):
						print("kbFilename triggered")
					linguisticsTopics = []
					if(self.linguisticsFilename != None):
						linguisticsTopics = getLinguisticsTopics(self.linguisticsFilename, self.verbose)
						print("--- linguisticsTopics")
						for topic in linguisticsTopics:
							print(topic)
					addAnnotationControls(htmlDoc, linguisticsTopics)
				with htmlDoc.tag("div", id="textAndAnnoDiv", klass="row"):
					with htmlDoc.tag("div", id="textLeftColumn", klass="col-12"):
						self.createTextDiv(htmlDoc);
					with htmlDoc.tag("div", id="annoDiv", klass="col-4"):
						htmlDoc.asis("")

				with htmlDoc.tag("div", klass="spacer"):
					htmlDoc.asis('')
				htmlDoc.asis(self.getJavascript())
				htmlDoc.asis("<!-- bodyBottomCustomizationHook -->")
		self.htmlDoc = htmlDoc
		self.htmlText = htmlDoc.getvalue()
		return(self.htmlText)

#-------------------------------------------------------------------------------
	def createTextDiv(self, htmlDoc):

		if(self.verbose) :
			print("--- entering createTextDiv")
		with htmlDoc.tag("div", id="textDiv"):
			for i in self.lineNumbers:
				if(self.verbose):
					print("line %d/%d" % (i, self.lineCount))
				line = IjalLine(self.xmlDoc, i, self.tierGuide,
								self.grammaticalTerms, quiet=(not self.verbose))
				line.parse()
				start = line.getStartTime()
				end = line.getEndTime()
				timeCodesForLine = [start,end]
				self.timeCodesForText.append(timeCodesForLine)
				id = line.getAnnotationID()
				with htmlDoc.tag("div",  klass="line-wrapper", id=i+1):
					tbl = line.getTable()
					with htmlDoc.tag("div", klass="line-sidebar"):
						line.htmlLeadIn(htmlDoc)
						s = f"<!-- sidebarHookLine_{i+1} -->"
						htmlDoc.asis(s)
					line.toHTML(htmlDoc)

#-------------------------------------------------------------------------------
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

#-------------------------------------------------------------------------------
def getLinguisticsTopics(filename, verbose):

	f = open(filename)
	lines = f.readlines()
	topics = []
	for line in lines:
		if(verbose):
			print(line)
		if line.find('":') > 0:
			cleanLine = line.strip().replace('"', '').replace(':', '')
			print(cleanLine)
			topics.append(cleanLine)

	topics.sort()
	return(topics)

#-------------------------------------------------------------------------------
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
def addVideoSizeSlider(htmlDoc):

	with htmlDoc.tag("div", id="videoSizeSliderDiv", klass="sliderControlDiv"):

		with htmlDoc.tag("label"):
				htmlDoc.asis("Media Player Size")
		htmlDoc.input(name="videoSizeSelector", type="range",
					  min="100", max="800", value="400", step="100",
					  id="videoSizeSelector")

#-------------------------------------------------------------------------------
def addFontSizeControls(htmlDoc):

	print("--- addFontSizeControls new klass")
	with htmlDoc.tag("div", id="fontSizeControlsDiv", klass="sliderControlDiv"):

		with htmlDoc.tag("label"):
			htmlDoc.asis("Playback Speed")
		htmlDoc.input(name="speedSelector", type="range",
					  min="0.5", max="1.25", value="0.8",
					  step="0.25", id="speedSelector")
		with htmlDoc.tag("div", id="playbackSpeedReadout"):
				htmlDoc.asis("1.0")
		htmlDoc.stag("br")

		with htmlDoc.tag("label"):
			htmlDoc.asis("Print Size")
		htmlDoc.input(name="fontSizeSlider", type="range",
					  min="0.2", max="4.0", value="1.4", step="0.1",
					  id="fontSizeSlider")
		htmlDoc.stag("br")


#---------------------------------------------------------------
def addAnnotationControls(htmlDoc, linguisticsTopics):

	print("--- addAnnottionControls")
	with htmlDoc.tag("div", id="annoButtonsDiv", klass="row"):
		with htmlDoc.tag("div", klass="col-8 text-left"):
			with htmlDoc.tag("button", id="toggleAnnotationsButton",
						 klass="btn btn-outline-dark"):
				htmlDoc.text('Show Annotations')
		with htmlDoc.tag("div", klass="col-4 text-right"):
			with htmlDoc.tag("span", id="linguisticTopicController"):
				with htmlDoc.tag("label", id="linguisticTopicSelectorLabel"):
					htmlDoc.asis("Linguistic Topic:")
				with htmlDoc.tag("select", id="languageTopicsSelector",
								 klass="seletpicker btn btn-outline-dark"):
					with htmlDoc.tag("option"):
						htmlDoc.asis("")
					for topic in linguisticsTopics:
						with htmlDoc.tag("option"):
							htmlDoc.asis(topic)

#-------------------------------------------------------------------------------
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

