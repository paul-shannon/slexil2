
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
# from yattag import *
import yaml
# import unittest
from ijalLine import *
# import importlib
pd.set_option('display.width', 1000)
import pdb
# from decimal import Decimal
import logging
import identifyLines
from audioExtractor import AudioExtractor

#----------------------------------------------------------------------------------------------------
# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------------------------------------------------
class Text:

	xmlFilename = ''
	audioPath = ''
	grammaticalTermsFile = None
	grammaticalTerms = []
	xmlDoc = None
	htmlDoc = None
	lineCount = 0
	quiet = True

	def __init__(self, xmlFilename, soundFileName, grammaticalTermsFile, tierGuideFile, projectDirectory, lineNumberForDebugging=None, quiet=True):
		self.xmlFilename = xmlFilename
		self.soundFileName = soundFileName
		self.audioPath = "audio"
		self.audioFileType = self.soundFileName[-3:]
		self.grammaticalTermsFile = grammaticalTermsFile
		self.tierGuideFile = tierGuideFile
		self.projectDirectory = projectDirectory
		self.validInputs()
		self.lineNumberForDebugging = lineNumberForDebugging
		self.quiet = quiet
		self.xmlDoc = etree.parse(self.xmlFilename)
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
		self.audio = AudioExtractor(soundFileName, xmlFilename, targetDirectory)

	def getTierSummary(self):
		tmpDoc = etree.parse(self.xmlFilename)
		tierIDs = [tier.attrib["TIER_ID"] for tier in tmpDoc.findall("TIER")]
		tiers = tmpDoc.findall("TIER")
		#pdb.set_trace()
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

	def makeStartStopTable(self, annotations):
		self.audioTable = []
		startStopTimes = "window.timeStamps=["
		for i,annotation in enumerate(annotations):
			start = annotation[0]
			end = annotation[1]
			entry = "{ 'id' : '%s', 'start' : %s, 'end' : %s},\n" %(str(i+1),start,end)
			startStopTimes += entry
			self.audioTable.append(annotation)
		startStopTimes =startStopTimes[:-1] + "]"
		# 		print(startStopTimes)
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
			grammaticalTerms = open(self.grammaticalTermsFile).read()#.split("\n")
			assert(len(grammaticalTerms) > 0)
			self.grammaticalTerms = _makeAbbreviationListLowerCase(grammaticalTerms)
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
		cssFilename = "ijal.css"
		#assert(os.path.exists(cssFilename))
		css = '<link rel = "stylesheet" type = "text/css" href = "%s" />' % cssFilename
		return(css)

	def getJQuery(self):
		scriptTag = '<script src="https://code.jquery.com/jquery-3.6.3.min.js"></script>\n'
		#scriptTag = '<script src="jquery-3.3.1.min.js"></script>\n'
		return(scriptTag)

	def getJavascript(self,timeCodesForText):
		startStopTimes = self.makeStartStopTable(timeCodesForText)
		jsSource = '<script src="ijalUtils.js"></script>\n'
		jsSource += '<script type="text/javascript">%s</script>\n' %startStopTimes
		return(jsSource)

	def getPlayer(self):
		soundFile = os.path.join(self.audioPath,os.path.basename(self.soundFileName))
		playerDiv = '<audio class="player" id="audioplayer" src="%s" controls></audio></audio>' %soundFile
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
		# pdb.set_trace()
		with htmlDoc.tag('html', lang="en"):
			with htmlDoc.tag('head'):
				htmlDoc.asis('<meta charset="UTF-8"/>')
				htmlDoc.asis(self.getJQuery())
				htmlDoc.asis(self.getCSS())
				htmlDoc.asis("<!-- headCustomizationHook -->")
			with htmlDoc.tag('body'):
				htmlDoc.asis("<!-- bodyTopCustomizationHook -->")
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
						self.audio.makeLineAudio(i, id, start, end)
						with htmlDoc.tag("div",  klass="line-wrapper", id=i+1):
							tbl = line.getTable()
							#lineID = tbl.ix[0]['ANNOTATION_ID']
							# lineID = tbl.iloc[0][tbl.columns.values.tolist().index('ANNOTATION_ID')]
							with htmlDoc.tag("div", klass="line-sidebar"):
								line.htmlLeadIn(htmlDoc, self.audioPath, self.audioFileType)
								s = f"<!-- sidebarHookLine_{i+1} -->"
								htmlDoc.asis(s)
							line.toHTML(htmlDoc)
				with htmlDoc.tag("div", klass="spacer"):
					htmlDoc.asis('')
				#htmlDoc.asis(self.getPlayer())
				htmlDoc.asis(self.getJavascript(timeCodesForText))
				htmlDoc.asis("<!-- bodyBottomCustomizationHook -->")
		self.htmlDoc = htmlDoc
		self.htmlText = htmlDoc.getvalue()
		return(self.htmlText)

#---------------------------------------------------------
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

