# -*- tab-width: 3 -*-
# sfmtToText.py: a class to represent a complete IJAL interlinear text
# with optional interspersed arbitrary HTML
#-------------------------------------------------------------------------------
# import re
# import sys
import os, sys
from pathlib import Path
from numpy import log10;
from yattag import *
from yattag import Doc
import yaml
from tierGuide import TierGuide
from slexil.tieredLine import TieredLine
from slexil.sfmt import *

#from slexil.newYamlParser import NewYamlParser
#from slexil.inferTierStructureFromSFMT import InferTierStructure


from dropDownMenu import DropDownMenu
from webPacker import WebPacker
import pdb
import identifyLines

doc, tag, text, line = Doc().ttl()
#-------------------------------------------------------------------------------
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
class sfmtToWebPage:

   file = ''
   tierGuide = None
   tierGuideFile = None
   yamlParser = None
   pageTitle = ''
   aboutBoxNeeded = None
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
   useTooltips = False
   its = None  # short for inferTierStructure object
   showAnnotations = False  # when true, open that div, auto display
   provideRecording = True

   def __init__(self,
                file,
                grammaticalTerms = [],
                tierGuideFile = None,
                projectDirectory = "./",
                verbose = False,
                fontSizeControls = False,
                startLine = None,
                endLine = None,
                pageTitle = "need title",
                helpFilename = None,
                helpButtonLabel = None,
                kbFilename = None,
                linguisticsFilename = None,
                fixOverlappingTimeSegments = False,
                provideRecording=False,
                webpackLinksOnly=False,
                useTooltips=False,
                showAnnotations=False):

      self.verbose = verbose
      if verbose:
         print("--- sfmtToWebPage.py, ctor")
      self.provideRecording = provideRecording

      self.file = file
      self.grammaticalTerms = grammaticalTerms
      self.sfmt = SFMT(file, self.verbose)
      self.sfmt.parse()

      self.lines = self.sfmt.getTieredLines()
      self.lineCount = len(self.lines)
      if(self.lineCount == 0):
         print("no lines found, exiting...")
         sys.exit(1)

      self.tierGuide = self.sfmt.getTierGuide()
 
      if(pageTitle == None):
         self.pageTitle = "slexil2"
         self.displayTitle = None
      else:
         self.pageTitle = pageTitle
         self.displayTitle = pageTitle
      self.webpackLinksOnly = webpackLinksOnly
      self.fixOverlappingTimeSegments = fixOverlappingTimeSegments
      self.tierGuideFile = tierGuideFile
      self.projectDirectory = projectDirectory
      self.fontSizeControls = fontSizeControls
      self.helpFilename = helpFilename
      self.helpButtonLabel = helpButtonLabel
      self.useTooltips = useTooltips
      self.kbFilename = kbFilename
      self.linguisticsFilename = linguisticsFilename
      self.showAnnotations = showAnnotations
      self.validInputs()
      self.verbose = verbose


      if(startLine != None):
         self.lineNumbers = range(startLine, endLine)
      else:
         self.lineNumbers = range(self.lineCount)
      audioURL = self.sfmt.getAudioURL()
      videoURL = self.sfmt.getVideoURL()
      mimeType = self.sfmt.getMimeType()
         # we give preference to video
      if not videoURL is None:
         self.mediaInfo = {"url": videoURL, "mimeType": "unspecified"}
      else:
         self.mediaInfo = {"url": audioURL, "mimeType": "unspecified"}
      self.startStopTable = self.sfmt.getTimeTable()


   #--------------------------------------------------------------------------------   
   def setPreferredMediaURL(self, url):

      self.mediaUrl = url
      self.mediaType = "not used"
      self.mediaInfo = {"url": url, "mimeType": self.mediaType}


   #--------------------------------------------------------------------------------   
   def getMediaInfo(self):

      return(self.mediaInfo)

   #--------------------------------------------------------------------------------   
   def makeJavascriptStartStopObject(self, tbl):
      if(self.verbose):
         print("--- entering makeJavascriptStartStopObject")
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
         assert(os.path.isfile(self.file))
      except AssertionError as e:
         raise Exception(self.file) from e
      try:
         if(not self.tierGuideFile == None):
            assert(os.path.isfile(self.tierGuideFile))
      except AssertionError as e:
         raise Exception(tierGuideFile)from e

      return(True)

   #--------------------------------------------------------------------------------   
   def determineAudioOrVideo(self):

      url = self.getMediaInfo()["url"]
      self.mediaType = "unrecognized"
      self.mediaUrl = url

      suffix = Path(url).suffix.lower()
      videoExtensions = [".m4v", ".mov", ".mp4", ".mpg"]
      audioExtensions = [".wav", ".mp3", ".ogg", ".webm"]
      mediaExtensions = videoExtensions + audioExtensions

      
      if(suffix in audioExtensions):
         self.mediaType = "audio"
      elif(suffix in videoExtensions):
         self.mediaType = "video"
      else:  
         raise MediaFormatError(mediaExtensions, suffix)
      

   #--------------------------------------------------------------------------------   
   def getPlayer(self):

      if self.verbose:
          print("--- text.getPlayer, mediaUrl: %s" % self.mediaUrl)
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
            htmlDoc.asis(webPacker.getJSText())
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
                                     min="50", max="350", value="250",
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
                           #print("--- annotation topics")
                           #for topic in topics:
                           #   print(topic)
                           with htmlDoc.tag("div", id="topicsMenuDiv"):
                              menu = DropDownMenu(menuTitle = "Linguistic Topics",
                                                  menuID="topics",
                                                  menuOptions=topics)
                              menu.toHTML(htmlDoc)
                        with htmlDoc.tag("div", id="annoNotesDiv"):
                           htmlDoc.asis("")

            htmlDoc.asis('\n\n<!-- bodyBottomInsertionHook -->\n\n')

      self.htmlDoc = htmlDoc
      self.htmlText = htmlDoc.getvalue()
      return(self.htmlText)

   #-------------------------------------------------------------------------------
   def addTitleAndButtons(self, htmlDoc):
      
      with htmlDoc.tag("div", id="titleAndOptionalButtonsDiv"):
         if(self.displayTitle != None):
            with htmlDoc.tag("span", id="pageTitle"):
               htmlDoc.text(self.displayTitle)
         with htmlDoc.tag("div", id="optionalButtonsDiv"):
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
            if(self.provideRecording):
               with htmlDoc.tag("button", id="openRecordDialogButton",
                                klass="standardSlexilButton"):
                  htmlDoc.stag('img',
                               src='https://slexildata.artsrn.ualberta.ca/images/microphone-342.png')
            htmlDoc.asis(self.getRecordingDialogHTML())

   #-------------------------------------------------------------------------------
   def getRecordingDialogHTML(self):

      html = """
     <div id='recordingNotAvailablePopup'></div>
     <div id='recordingPopup'>
        <div id='buttonsDiv' style='float: left; width: 100px;' >
           <button id='recordButton'
                   class='recorderButton' style='margin: 10px; margin-bottom: 0px;'>Record</button><br>
           <button id='playRecordingButton'
                   class='recorderButton' 
                   style='display:none; margin: 10px; margin-bottom: 0px;' >Play</button>
           </div>
        <div id='recorderDiv'
             style='display: none; float: right;  width: calc(100% - 120px); border: 1px solid darkblue; border-radius: 10px; margin-top: 10px; margin-right: 10px;'>
            </div>
        <div id='playerDiv'
             style='display: none; float: right;  width: calc(100% - 120px); border: 1px dotted darkblue;  border-radius:10px; margin-top: 10px; margin-right: 10px;'>
          </div>
      </div>
     """

      return(html)
       
   #--------------------------------------------------------------------------------
   def createOtherControlsDiv(self, htmlDoc):

      with htmlDoc.tag("div", id="otherControlsGridDiv", klass="otherControlsGridWrapper"):
         with htmlDoc.tag("div", id="playbackSpeedDiv", klass="otherControlsGridCell"):
            with htmlDoc.tag("div", id="playbackSpeedLabel"):
               htmlDoc.text("Playback speed ")
            with htmlDoc.tag("div", id="playbackControlsDiv",
                             style='width: 300px;'):
               with htmlDoc.tag("button", id="slowerPlaybackButton",
                                klass="playbackSpeedButton"):
                  htmlDoc.text(" - ")
               htmlDoc.stag("input",  type="range", min="0.25", max="2.0", value="1.0",
                            step="0.25", id="speedSelector", name="speedSelector")
               with htmlDoc.tag("button", id="fasterPlaybackButton",
                                klass="playbackSpeedButton"):
                  htmlDoc.text(" + ")
               with htmlDoc.tag("div", id="playbackSpeedReadout"):
                  htmlDoc.text("1.0")

         with htmlDoc.tag("div", id="printSizeDiv", klass="otherControlsGridCell"):
            with htmlDoc.tag("div", id="printSizeLabel"):
               htmlDoc.text("Print Size ")
            with htmlDoc.tag("form", action=""):
               htmlDoc.stag("input",  type="range", min="0.2", max="4.0", value="1.4",
                            step="0.1", id="fontSizeSlider", name="fontSizeSlider")

         tierNames = list(self.tierGuide.values())

         if(len(self.sfmt.getHtmlLines()) > 0):
            tierNames.append("html")

         with htmlDoc.tag("div", id="tierControlsDiv"):
            with htmlDoc.tag("div"):            
               with htmlDoc.tag("span", id="tiersLabelDiv"):
                  htmlDoc.text("Visible Tiers: ")
                  with htmlDoc.tag("button", id="allNoneTierButton",
                                   klass="standardSlexilButton"):
                      htmlDoc.text("All/None")
                  htmlDoc.asis('\n\n<!-- otherControlsInsertionHook -->\n\n')

            with htmlDoc.tag("div", id="tiersCheckBoxesDiv"):
               with tag('form', action = ""):
                  for tierName in tierNames:
                     with htmlDoc.tag("div", style='display: inline-block'):
                        htmlDoc.input(name=tierName, type = 'checkbox', checked=True,
                                      value=tierName, klass="tierToggleCheckbox",
                                      id="tierToggle-%s" % tierName)
                        htmlDoc.text(" %s" % tierName)

   #-------------------------------------------------------------------------------
   def tieredLineHtmlLeadin(self, htmlDoc, tierNumber, startTime, endTime,
                            numberedLineNumber, numberedLine=True):

        buttonLabel = numberedLineNumber
        if(not numberedLine):
             # create an empty button label, with width roughly the same
             # as that of the surrounding numbered buttons
           buttonLabel = "&nbsp;&nbsp;";
           if(numberedLineNumber > 0):
              if(bool(log10(numberedLineNumber) >= 1)):  # >= 10
                buttonLabel = "%s%s" % (buttonLabel, "&nbsp;&nbsp;")
              if(bool(log10(numberedLineNumber) >= 2)):  # >= 100
                buttonLabel = "%s%s" % (buttonLabel, "&nbsp;&nbsp;")
        clickActionString = "playSample(%s, %d, %d)" % \
                            (tierNumber, startTime, endTime)
        buttonTag = htmlDoc.tag("button", onclick=clickActionString,
                                klass="standardSlexilButton slexilTooltip")
        if(self.useTooltips):
            buttonTag.attrs["class"] = "standardSlexilButton slexilTooltip"
        with buttonTag:
           htmlDoc.asis(str(buttonLabel))
           if(self.useTooltips):
              with htmlDoc.tag("span", klass="slexilTooltipText"):
                  htmlDoc.text("Play Line %d" % buttonLabel)

   #-------------------------------------------------------------------------------
   def createTextDiv(self, htmlDoc):

      if(self.verbose) :
         print("--- entering createTextDiv")
      with htmlDoc.tag("div", id="textDiv"):
         tierNumber = 0
         numberedLineNumber = 0  # so we can exclude un-numbered tiers
         htmlLineNumber = 0
         tbl = self.sfmt.getOrderedLineObjectsTieredAndHTML()
         htmlLines = self.sfmt.getAllHtml()
         tieredLines = self.sfmt.getTieredLines()
         rows = tbl.shape[0]
         for i in range(rows):
            lineNumber = i
            lineType = tbl.loc[i]['type']
            signature = tbl.loc[i]['signature']
            if lineType == "html":
               htmlLine = htmlLines[htmlLineNumber]
               #htmlLine = [html for html in htmlLines if html.find(signature) >= 0][htmlLineNumber]
               if htmlLine.find("html:") >= 0:
                  htmlLine = htmlLine.split("html:")[1].strip()
               with htmlDoc.tag("div", klass="tier tier-html", name="html"):
                   htmlDoc.asis(htmlLine)
                   htmlDoc.asis("\n")
               htmlLineNumber += 1  # indexes into htmlLines array
            elif lineType == "tier":
               tierNumber += 1
               tierGuide = self.sfmt.getTierGuide()
               signature = int(signature)   # startTime in msecs is the signature
               tiers = [tier for tier in tieredLines if tier['startTime'] == signature]
               if(len(tiers) <= 0):
                  print("length of tiers is 0")
                  print("signature: %s" % signature)
                  pdb.set_trace()
               assert(len(tiers) > 0)
               if type(tiers) == bool: #  == bool or len(tiers==0):
                  traceFileName = "sfmtToWebPage.py"
                  traceLineNumber = 413
                  print("--- trace: %s at %d" % (traceFileName, traceLineNumber))
               tier = tiers[0]  # should be only one line matching signature
               tieredLine = TieredLine(self.sfmt,
                                       tiers,  # an array of tier lines expected
                                       lineNumber=0, # always true 
                                       tierNumber=tierNumber,
                                       tierGuide=tierGuide,
                                       grammaticalTerms=self.grammaticalTerms,
                                       useTooltips=False, verbose=self.verbose)
               spokenText = str(tieredLine.getSpokenText())
               if(self.verbose):
                  print("%d: %s" % (i, spokenText))
               #print("\n--- sfmtToWebPage, line 473, spokenText:")
               #print(spokenText)
               # pdb.set_trace()
               numberedLine = True
               if(re.search("^\s*@", spokenText)):
                  numberedLine = False
               if(numberedLine):
                  numberedLineNumber += 1
               start = tier['startTime']
               end = tier['endTime']
               timeCodesForLine = [start,end]
               self.timeCodesForText.append(timeCodesForLine)
               id = tierNumber
               with htmlDoc.tag("div",  klass="line-wrapper", id=tierNumber):
                  with htmlDoc.tag("div", klass="line-sidebar"):
                     #print("sfmtToWebPage, line 477, tierNumber: %d" % tierNumber);
                     #pdb.set_trace()
                     self.tieredLineHtmlLeadin(htmlDoc, tierNumber, start, end,
                                               numberedLineNumber, numberedLine)
                     s = f"\n<!-- sidebarHookLine_{i+1} -->\n"
                     htmlDoc.asis(s)
                  tieredLine.toHTML(htmlDoc)

#   #-------------------------------------------------------------------------------
#   def recovered_createTextDiv(self, htmlDoc):
#
#      if(self.verbose) :
#         print("--- entering createTextDiv")
#      with htmlDoc.tag("div", id="textDiv"):
#         tierNumber = 0
#         tbl = self.sfmt.getOrderedLineObjectsTieredAndHTML()
#         htmlLines = self.sfmt.getAllHtml()
#         tieredLines = self.sfmt.getTieredLines()
#         rows = tbl.shape[0]
#         for i in range(rows):
#            lineType = tbl.loc[i]['type']
#            signature = tbl.loc[i]['signature']
#            if lineType == "html":
#               htmlLine = [html for html in htmlLines if html.find(signature) >= 0][0]
#               if self.verbose:
#                  print(htmlLine)
#               with htmlDoc.tag("div", klass="tier tier-html", name="html"):
#                   htmlDoc.asis(htmlLine)
#            elif lineType == "tier":
#               tierNumber += 1
#               signature = int(signature)   # startTime in msecs is the signature
#               #pdb.set_trace()
#               if self.verbose:
#                   print("---- tierNumber is now: %d" % tierNumber)
#               tier = [tier for tier in tieredLines if tier['startTime'] == signature]
#               tieredLine = TieredLine(tier, 0, tierNumber,
#                                       self.tierGuide,
#                                       grammaticalTerms=self.grammaticalTerms,
#                                       useTooltips=False, verbose=self.verbose)
#               analysisTierNames = tieredLine.getAnalysisTierNames()
#               start = tieredLine.getStartTime()
#               end = tieredLine.getEndTime()
#               timeCodesForLine = [start,end]
#               self.timeCodesForText.append(timeCodesForLine)
#               id = tieredLine.getAnnotationID()
#               with htmlDoc.tag("div",  klass="line-wrapper", id=tierNumber):
#                  # tbl = tieredLine.getTable()
#                  with htmlDoc.tag("div", klass="line-sidebar"):
#                     tieredLine.htmlLeadIn(htmlDoc)
#                     s = f"<!-- sidebarHookLine_{i+1} -->"
#                     htmlDoc.asis(s)
#                  tieredLine.toHTML(htmlDoc)
#
#
#       
#   def old_createTextDiv(self, htmlDoc):
#
#      if(self.verbose) :
#         print("--- entering createTextDiv")
#      with htmlDoc.tag("div", id="textDiv"):
#         tierNumber = 0
#         for i in self.lineNumbers:
#            line = self.lines[i]
#            if self.verbose:
#                print(line)
#            keys = list(line.keys())
#            if keys == ["html"]:
#                if self.verbose:
#                   print("---- found html")
#                   print(line["html"])
#                with htmlDoc.tag("div", klass="tier tier-html", name="html"):
#                   htmlDoc.asis(line["html"])
#            else: # (isinstance(line, dict)):
#               tierNumber += 1
#               if self.verbose:
#                   print("---- tierNumber is now: %d" % tierNumber)
#               #tieredLine = TieredLine(self.lines, i, tierNumber,
#               #                        self.tierGuide,
#               #                        grammaticalTerms=self.grammaticalTerms,
#               #                        useTooltips=False, verbose=self.verbose)
#               analysisTierNames = tieredLine.getAnalysisTierNames()
#               start = tieredLine.getStartTime()
#               end = tieredLine.getEndTime()
#               timeCodesForLine = [start,end]
#               self.timeCodesForText.append(timeCodesForLine)
#               id = tieredLine.getAnnotationID()
#               with htmlDoc.tag("div",  klass="line-wrapper", id=tierNumber):
#                  # tbl = tieredLine.getTable()
#                  with htmlDoc.tag("div", klass="line-sidebar"):
#                     tieredLine.htmlLeadIn(htmlDoc)
#                     s = f"<!-- sidebarHookLine_{i+1} -->"
#                     htmlDoc.asis(s)
#                  tieredLine.toHTML(htmlDoc)

#-------------------------------------------------------------------------------
def getLinguisticsTopics(filename, verbose):

   f = open(filename)
   lines = f.readlines()
   topics = []
   for line in lines:
      #if(verbose):
      #   print(line)
      if line.find('":') > 0:
         cleanLine = line.strip().replace('"', '').replace(':', '')
         #print(cleanLine)
         topics.append(cleanLine)

   topics = sorted(topics, key=lambda s: s.lower())
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
def addFontSizeControls(htmlDoc):

   # print("--- addFontSizeControls new klass")
   with htmlDoc.tag("div", id="fontSizeControlsDiv", klass="sliderControlDiv"):
      with htmlDoc.tag("label", id="playbackSpeedLabel"):
         htmlDoc.asis("Playback Speed &nbsp;")
      htmlDoc.input(name="speedSelector", type="range",
                 min="0.25", max="2.0", value="1.0",
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

   # print("--- addAnnottionControls")
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

