# -*- tab-width: 3 -*-
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
from pathlib import Path
from yattag import *
from yattag import Doc
import yaml
from eafParser import *
from ijalLine import *
from webPacker import WebPacker
pd.set_option('display.width', 1000)
import pdb
import identifyLines
doc, tag, text, line = Doc().ttl()
#-------------------------------------------------------------------------------
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
class Text:

	xmlFilename = ''
	eafParser = None
	pageTitle = ''
	grammaticalTermsFile = None
	kbFilename = None
	linguisticsFilename = None
	mediaInfo = {"url": None, "mimetype": None}
	grammaticalTerms = []
	htmlDoc = None
	lineCount = 0
	verbose = False
	timeCodesForText = []
	startStopTable = None
	lineTables = None

	def __init__(self,
                 xmlFilename,
		         grammaticalTermsFile,
		         tierGuideFile,
		         projectDirectory,
		         verbose,
		         fontSizeControls,
		         startLine,
		         endLine,
		         pageTitle,
		         helpFilename,
		         helpButtonLabel,
		         kbFilename,
		         linguisticsFilename,
		         fixOverlappingTimeSegments,
		         webpackLinksOnly=False):

		self.xmlFilename = xmlFilename
		if(len(pageTitle) == 0):
			pageTitle = "slexil2"
		self.pageTitle = pageTitle
		self.webpackLinksOnly = webpackLinksOnly
		self.fixOverlappingTimeSegments = fixOverlappingTimeSegments
		self.tierGuideFile = tierGuideFile
		self.grammaticalTermsFile = grammaticalTermsFile
		self.projectDirectory = projectDirectory
		self.fontSizeControls = fontSizeControls
		self.helpFilename = helpFilename
		self.helpButtonLabel = helpButtonLabel
		self.kbFilename = kbFilename
		self.linguisticsFilename = linguisticsFilename
		self.validInputs()
		self.verbose = verbose

		parser = EafParser(xmlFilename, self.verbose, self.fixOverlappingTimeSegments)
		self.eafParser = parser
		parser.parseAllLines()

		with open(tierGuideFile, 'r') as f:
			self.tierGuide = yaml.safe_load(f)
		self.lineCount = parser.getLineCount()
		if(self.lineCount == 0):
			print("no lines found, disagreement between tierGuide and eaf? ")
			print("perhaps case disagreement?")
			print(self.tierGuide)
			sys.exit(1)
		if(startLine != None):
			self.lineNumbers = range(startLine, endLine)
		else:
			self.lineNumbers = range(self.lineCount)
		if os.path.isfile(os.path.join(projectDirectory,"ERRORS.log")):
			os.remove(os.path.join(projectDirectory,"ERRORS.log"))
		f = os.path.join(projectDirectory, "ERRORS.log")
		self.metadata = parser.getMetadata()
		self.mediaInfo = parser.getMediaInfo()
		self.lineTables = parser.getAllLinesTable() 
		self.startStopTable = parser.getTimeTable()
		self.eafParser = parser

	#--------------------------------------------------------------------------------	
	def getMediaInfo(self):

		return(self.mediaInfo)

	#--------------------------------------------------------------------------------	
	def makeJavascriptStartStopObject(self, tbl):
		if(self.verbose):
			print("--- entering makeStartStopTable")
		startStopTimes = "window.timeStamps=["
		rows = tbl.shape[0]
		for i in range(rows):
			start = tbl.loc[i, "start"]
			end = tbl.loc[i, "end"]
			entry = "{ 'id' : '%s', 'start' : %s, 'end' : %s},\n" %(str(i+1),start,end)
			startStopTimes += entry
		#if(self.verbose):
		#	print(startStopTimes)

		startStopTimes = startStopTimes[:-1] + "]"
		startStopTimesJS = "".join(["\n<script>\n", startStopTimes, "\n</script>\n"])
		#if(self.verbose):
		#	print("--- startStopTimesJS")
		#	print(startStopTimesJS)
		return(startStopTimesJS)

	#--------------------------------------------------------------------------------	
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

	#--------------------------------------------------------------------------------	
	def getPlayer(self):

		url = self.getMediaInfo()["url"]
		suffix = Path(url).suffix.lower()
		if(suffix in [".wav", ".mp3"]):
			playerDiv = '<audio class="player" id="mediaPlayer" src="%s" controls></audio>' % url
		elif(suffix in [".m4v", ".mov", ".mp4"]):
			playerDiv = '<video class="player" id="mediaPlayer" src="%s" controls></video>' % url
		else:
			print("unrecognized media file suffix in url: %s" % suffix)
			print("full url: %s" % url)
			playerDiv = ""
		return playerDiv

	#--------------------------------------------------------------------------------	
	def toHTML(self, lineNumber=None):
		if(self.verbose):
			print("--- entering toHTML")
		htmlDoc = Doc()
		self.timeCodesForText = []
		if(self.verbose):
			print("toHTML, lineNumber count: %d" % len(self.lineNumbers))

		htmlDoc.asis('<!DOCTYPE html>\n')
		webPacker = WebPacker(fullText = (not self.webpackLinksOnly))
		webPacker.readCSS()
		webPacker.readJS()
		startStopTimesJSText = self.makeJavascriptStartStopObject(self.startStopTable)

		annotationLinks = ""
		if(self.kbFilename != None):
			annotationLinks += '<script src="%s"></script>\n' % self.kbFilename
		if(self.linguisticsFilename != None):
			annotationLinks += '<script src="%s"></script>\n' % self.linguisticsFilename
		with htmlDoc.tag('html', lang="en"):
			with htmlDoc.tag('head'):
				htmlDoc.asis('<meta charset="UTF-8"/>')
				htmlDoc.asis('<title>%s</title>' % self.pageTitle)
				htmlDoc.asis(webPacker.getCSSText())
				htmlDoc.asis(startStopTimesJSText)
				htmlDoc.asis(annotationLinks)
				htmlDoc.asis("<!-- headCustomizationHook -->")
			with htmlDoc.tag('body'):
				aboutBoxNeeded = self.helpFilename != None
				with htmlDoc.tag("div", id="infoDiv"):
					if(aboutBoxNeeded):
						addAboutBox(htmlDoc, self.helpFilename)

				htmlDoc.asis("<!-- bodyTopCustomizationHook -->")
				if(self.fontSizeControls):
					addVideoSizeSlider(htmlDoc)
				addTierVisibilityControls(htmlDoc)
				with htmlDoc.tag("div", id="mediaAndButtonDiv"):
					with htmlDoc.tag("div", id="mediaPlayerDiv"):
						htmlDoc.asis(self.getPlayer())
					with htmlDoc.tag("div", id="aboutBoxButtonDiv"):
						with htmlDoc.tag("h5", id="titleHeader"):
							htmlDoc.asis(self.pageTitle)
						if(aboutBoxNeeded):
							addAboutBoxButton(htmlDoc, self.helpButtonLabel)

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
				htmlDoc.asis(webPacker.getJSText())
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
				lineTable = self.lineTables[i]	
				line = IjalLine(lineTable, i, self.tierGuide,
								self.grammaticalTerms, self.verbose)
				line.extractMorphemes()
				line.extractMorphemeGlosses()
				line.calculateMorphemeSpacing()
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
def addAboutBoxButton(htmlDoc, buttonLabel):

	with htmlDoc.tag("button",
			  ('data-bs-toggle','modal'),
			  ('data-bs-target', '#aboutModalDialog'),
			  klass="btn btn-primary"):
		htmlDoc.text(buttonLabel)

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
def addAboutBox(htmlDoc, helpFilename):

	helpText = open(helpFilename).read()

	with htmlDoc.tag("div",
		('tabindex', "-1"),
		('aria-labelledby', "modalLabel"),
		('aria-hidden', "true"),
		klass="modal fade", id="aboutModalDialog"):
			with htmlDoc.tag("div", klass="modal-dialog modal-lg"):
				with htmlDoc.tag("div", klass="modal-content"):
					with htmlDoc.tag("div", klass="modal-body"):
						htmlDoc.asis(helpText)

#---------------------------------------------------------------
def addVideoSizeSlider(htmlDoc):

	with htmlDoc.tag("div", id="videoSizeSliderDiv", klass="sliderControlDiv"):

		with htmlDoc.tag("label"):
				htmlDoc.asis("Media Player Size &nbsp;")
		htmlDoc.input(name="videoSizeSelector", type="range",
					  min="100", max="800", value="400", step="100",
					  id="videoSizeSelector")

#-------------------------------------------------------------------------------
def addTierVisibilityControls(htmlDoc):

	with htmlDoc.tag('div', id="tierControlsDiv"):
		with htmlDoc.tag("button", id="showHideTiersButton",
                       klass="btn btn-outline-dark"):
			htmlDoc.text('Show/Hide Tiers...')

		with htmlDoc.tag('div', id='tierControlsSubDiv'):
			with htmlDoc.tag('form', action = ""):
				with htmlDoc.tag('div'):
					for tier in ('speech', 'morphemes', 'translation'):
						with htmlDoc.tag('div'):
							id = "%s-toggle" % tier
							htmlDoc.input(name=id, klass="tierToggleCheckbox", id=id,
                                   type='checkbox', value=tier, checked=True)
							htmlDoc.asis(tier)

#----------------------------------------------------------------------------------------------------        
def addTierVisibilityControls_v1(htmlDoc):

	with htmlDoc.tag('div', id="tierControlsDiv"):
		with htmlDoc.tag('form', action = ""):
			with htmlDoc.tag('div'):
				with htmlDoc.tag('p'):
					htmlDoc.asis("Tier visibility:")
					for tier in ('speech', 'morphemes', 'morpheme glosses', 'translation'):
						with htmlDoc.tag('div'):
							id = "%s-toggle" % tier
							htmlDoc.input(name=id, klass="tierToggleCheckbox", id=id,
                                   type='checkbox', value=tier)
							htmlDoc.asis(tier)

#----------------------------------------------------------------------------------------------------        
def addFontSizeControls(htmlDoc):

	print("--- addFontSizeControls new klass")
	with htmlDoc.tag("div", id="fontSizeControlsDiv", klass="sliderControlDiv"):

		with htmlDoc.tag("label"):
			htmlDoc.asis("Playback Speed &nbsp;")
		htmlDoc.input(name="speedSelector", type="range",
					  min="0.25", max="1.25", value="1.0",
					  step="0.25", id="speedSelector")
		with htmlDoc.tag("div", id="playbackSpeedReadout"):
				htmlDoc.asis("1.0")
		htmlDoc.stag("br")

		with htmlDoc.tag("label"):
			htmlDoc.asis("Print Size &nbsp;")
		htmlDoc.input(name="fontSizeSlider", type="range",
					  min="0.2", max="4.0", value="1.4", step="0.1",
					  id="fontSizeSlider")


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

