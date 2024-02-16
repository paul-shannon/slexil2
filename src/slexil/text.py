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
from tierGuide import TierGuide
from eafParser import *
from ijalLine import *
from dropDownMenu import DropDownMenu
 
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
   aboutBoxNeeded = None
   grammaticalTermsFile = None
   kbFilename = None
   linguisticsFilename = None
   mediaInfo = {"url": None, "mimetype": None}
   mediaType = None
   mediaUrl = None
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
      if(pageTitle == None):
         self.pageTitle = "slexil2"
         self.displayTitle = None
      else:
         self.pageTitle = pageTitle
         self.displayTitle = pageTitle
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
      with open(tierGuideFile, 'r') as f:
         self.tierGuide = yaml.safe_load(f)

      self.validInputs()
      self.verbose = verbose

      parser = EafParser(xmlFilename, self.verbose, self.fixOverlappingTimeSegments)
      self.eafParser = parser
      parser.parseAllLines()

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
      #  print(startStopTimes)

      startStopTimes = startStopTimes[:-1] + "]"
      startStopTimesJS = "".join(["\n<script>\n", startStopTimes, "\n</script>\n"])
      #if(self.verbose):
      #  print("--- startStopTimesJS")
      #  print(startStopTimesJS)
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
   def determineAudioOrVideo(self):

      url = self.getMediaInfo()["url"]
      self.mediaType = "unrecognized"
      self.mediaUrl = url

      suffix = Path(url).suffix.lower()
      
      if(suffix in [".wav", ".mp3"]):
         self.mediaType = "audio"
      elif(suffix in [".m4v", ".mov", ".mp4"]):
         self.mediaType = "video"
      else:  # todo: raise exception here
         print("unrecognized media file suffix in url: %s" % suffix)
         print("full url: %s" % url)
         

   #--------------------------------------------------------------------------------   
   def getPlayer(self):

      if(self.mediaType == "audio"):
         playerDiv = '<audio class="player" id="audioPlayer" src="%s" controls></audio>' % self.mediaUrl
      elif(self.mediaType == "video"):
         playerDiv = '<video class="player" id="videoPlayer" src="%s" controls></video>' % self.mediaUrl
      else:
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

         self.aboutBoxNeeded = self.helpFilename != None
         self.determineAudioOrVideo()

         with htmlDoc.tag('body'):
            with htmlDoc.tag("div", id="mainDiv"):
               if(self.aboutBoxNeeded): # initially invisible, displayed on demand
                  addAboutBox(htmlDoc, self.helpFilename)

                  #-------------------------------------------------------------------------
                  # if audio:  player, title, about and other controls button all in top div
                  #-------------------------------------------------------------------------
               if(self.mediaType == "audio"):
                  with htmlDoc.tag("div", id="mediaPlayerAndControlsDiv"):
                     htmlDoc.tag("div", id="videoSizeControllerDiv", style="display: none")
                     with htmlDoc.tag("div", id="playerDivWithOptionalButtons"):
                        with htmlDoc.tag("div", id="audioPlayerDiv"):
                           htmlDoc.asis(self.getPlayer())
                        self.addTitleAndButtons(htmlDoc)

                  #-------------------------------------------------------------------------
                  # if video:  size slider, title, about and other controls button in top.
                  # video player in the next div
                  #-------------------------------------------------------------------------
               if(self.mediaType == "video"):
                  with htmlDoc.tag("div", id="mediaPlayerAndControlsDiv"):
                     with htmlDoc.tag("div", id="videoSizeControllerDiv"):
                        with htmlDoc.tag("span", id="videoSizeLabel"):
                           htmlDoc.text("Video Size ")
                        htmlDoc.stag("input",  type="range",
                                     min="50", max="800", value="150",
                                     step="10", id="videoSizeSelector",
                                     name="videoSizeSelector")
                        self.addTitleAndButtons(htmlDoc)
                     with htmlDoc.tag("div", id="playerDivWithOptionalButtons"):
                        htmlDoc.asis(self.getPlayer())

                  #-------------------------------------------------------------------------
                  # both audio and video have this initially hidden "other controls" div
                  #-------------------------------------------------------------------------
               with htmlDoc.tag("div", id="otherControlsDiv", style="display: none"):
                  self.createOtherControlsDiv(htmlDoc)
                 
               with htmlDoc.tag("div", id="textAndAnnoDiv"):
                  self.createTextDiv(htmlDoc);
                  with htmlDoc.tag("div", id="annoDiv"):
                     with htmlDoc.tag("div", id="annoAndTopicsDiv"):
                        if(self.linguisticsFilename != None):
                           topics = getLinguisticsTopics(self.linguisticsFilename,
                                                         self.verbose)
                           with htmlDoc.tag("div", id="topicsMenuDiv"):
                              menu = DropDownMenu(menuTitle = "Linguistic Topics",
                                                  menuID="topics",
                                                  menuOptions=topics)
                              menu.toHTML(htmlDoc)
                        with htmlDoc.tag("div", id="annoNotesDiv"):
                           htmlDoc.asis("")

            htmlDoc.asis(webPacker.getJSText())

      self.htmlDoc = htmlDoc
      self.htmlText = htmlDoc.getvalue()
      return(self.htmlText)

   #-------------------------------------------------------------------------------
   def addTitleAndButtons(self, htmlDoc):
      
      with htmlDoc.tag("div", id="optionalButtonsDiv"):
         if(self.displayTitle != None):
            with htmlDoc.tag("span", id="pageTitle"):
               htmlDoc.text(self.displayTitle)
         if(self.aboutBoxNeeded):
            with htmlDoc.tag("button", id="aboutBoxButton",
                             klass="standardSlexilButton"):
               htmlDoc.text(self.helpButtonLabel)
         if(self.kbFilename != None):
            #with htmlDoc.tag("div", id="annoButtonDiv"):
            with htmlDoc.tag("button", id="toggleAnnotationsButton",
                             klass="standardSlexilButton"):
               htmlDoc.text("Show Annotations")

         with htmlDoc.tag("button", id="showHideOtherControlsButton",
                          klass="standardSlexilButton"):
            htmlDoc.text("Other Controls")


   #-------------------------------------------------------------------------------
   def createOtherControlsDiv(self, htmlDoc):

          #-----------------
          # playback speed 
          #-----------------
      with htmlDoc.tag("span", id="playbackSpeedLabel"):
         htmlDoc.text("Playback speed ")
      with htmlDoc.tag("form", action=""):
         htmlDoc.stag("input",  type="range", min="0.25", max="1.25", value="1.0",
                     step="0.25", id="speedSelector", name="speedSelector")
         with htmlDoc.tag("div", id="playbackSpeedReadout"):
            htmlDoc.text("1.0")
      
          #-----------------
          # font size
          #-----------------
      with htmlDoc.tag("span", id="printSizeLabel"):
         htmlDoc.text("Print Size ")
      with htmlDoc.tag("form", action=""):
         htmlDoc.stag("input",  type="range", min="0.2", max="4.0", value="1.4",
					       step="0.1", id="fontSizeSlider", name="fontSizeSlider")

          #-----------------
          # tier visibility
          #-----------------

      tg = TierGuide(self.tierGuideFile)
      if(not tg.valid()["valid"]):
         print("--- text.py finds invalid tierGuide")
         print(tg.valid())
         sys.exit()
         
      
      with htmlDoc.tag("div", id="tierControlsDiv"):
         with htmlDoc.tag("span", id="tiersLabelDiv"):
            htmlDoc.text("Visible Tiers: ")
      with htmlDoc.tag("div", id="tiersCheckBoxesDiv"):
         with tag('form', action = ""):
            tierName = "transcription"
            htmlDoc.input(name=tierName, type = 'checkbox', checked=True,
                          value=tierName, klass="tierToggleCheckbox",
                          id="tierToggle-%s" % tierName)
            htmlDoc.text(" %s" % tierName)

            if("translation" in tg.getTierNames()):
               tierName = "translation"
               htmlDoc.input(name=tierName, type = 'checkbox', checked=True,
                             value=tierName, klass="tierToggleCheckbox",
                             id="tierToggle-%s" % tierName)
               htmlDoc.text(" %s" % tierName)

            if("morpheme" in tg.getTierNames()):
               tierName = "analysis"
               htmlDoc.input(name=tierName, type = 'checkbox', checked=True,
                             value=tierName, klass="tierToggleCheckbox",
                             id="tierToggle-%s" % tierName)
               htmlDoc.text(" %s" % tierName)

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

   with htmlDoc.tag("dialog", id="aboutBoxDialog"):
      with htmlDoc.tag('form', method="dialog"):
         htmlDoc.asis(helpText)

#---------------------------------------------------------------
def addVideoSizeSlider(htmlDoc):

   #with htmlDoc.tag("div", id="videoSizeSliderDiv", klass="sliderControlDiv"):

   with htmlDoc.tag("label"):
      htmlDoc.asis("Media Player Size &nbsp;")
   htmlDoc.input(name="videoSizeSelector", type="range",
                 min="100", max="800", value="400", step="100",
                 id="videoSizeSelector")

#-------------------------------------------------------------------------------
def addTierVisibilityControls(htmlDoc):

   with htmlDoc.tag('div', id="tierControlsDiv"):
      #with htmlDoc.tag("button", id="showHideTiersButton",
      #                 klass="btn btn-outline-dark"):
      #  htmlDoc.text('Show/Hide Tiers...')
      with htmlDoc.tag('div', id='tierControlsSubDiv'):
         with htmlDoc.tag('div', id="tiersLabelDiv"):
            htmlDoc.asis("Tiers: ")
         with htmlDoc.tag('div', id="tiersCheckBoxesDiv"):
            with htmlDoc.tag('form', action = ""):
               with htmlDoc.tag('div'):
                  for tier in ('speech', 'morphemes', 'translation'):
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
      with htmlDoc.tag("label", id="playbackSpeedLabel"):
         htmlDoc.asis("Playback Speed &nbsp;")
      htmlDoc.input(name="speedSelector", type="range",
                 min="0.25", max="1.25", value="1.0",
                 step="0.25", id="speedSelector")
      with htmlDoc.tag("div", id="playbackSpeedReadout"):
            htmlDoc.asis("1.0")
      with htmlDoc.tag("label", id="printSizeLabel"):
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

