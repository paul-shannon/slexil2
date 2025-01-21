# -*- tab-width: 3 -*-
#-------------------------------------------------------------------------------
import os, sys
from slexil.inferTierStructure import InferTierStructure
from slexil.tieredLine import TieredLine
from slexil.exceptions import *
import xmlschema
from urllib.parse import urlparse
from lxml import etree
import yaml
import pandas as pd
import numpy as np
pd.set_option('display.width', 1000)
import pdb
#-------------------------------------------------------------------------------
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
class NewYamlParser:

   yamlFile = ''
   obj = None
   tierGuideFile = None
   htmlLines = []
   tieredLines = []
   lineCount = None
   tierInfo = None
   timeTable = None
   lineTable = None
   lines = list()
   verbose = False
   metadata = None
   audioURL = None
   videoURL = None
   mimeType = None
   lineTypeSpecified = False
   fixOverlappingTimeSegments = False

   #----------------------------------------------------------------------
   def __init__(self, yamlFile, verbose=False, fixOverlappingTimeSegments=False):

     self.yamlFile = yamlFile
     x = yaml.load(open(yamlFile), Loader=yaml.FullLoader)
     self.obj = x
     expectedFields = ['title', 'narrator', 'textEntry', 'mediaFile', 'mimeType', 'lines']
     fields = list(x.keys())
     extraFields = set(fields).difference(set(expectedFields))
     missingFields = set(expectedFields).difference(set(fields))
     if not fields == expectedFields:
        msg = "Missing or unsupported fields in the yaml file.\n"
        msg += "expected fields: %s\n" % ", ".join(expectedFields)
        if(len(missingFields) > 0):
           msg += "missing fields: %s\n" % ", ".join(missingFields)
        if(len(extraFields) > 0):
           msg += "extra fields: %s\n"   % ", ".join(extraFields)
        raise Exception(msg)

     self.its = InferTierStructure(self.yamlFile)
     self.tieredLines = self.its.getTieredLines()
     self.allLines = self.its.getAllLines()
     self.htmlLines = self.its.getHtmlLines()
     self.tierGuide = self.its.getTierGuide()

     self.title = x['title']
     self.narrator = x['narrator']

         # todo: these are repeated in eafParser.py  
     videoExtensions = [".m4v", ".mov", ".mp4", ".mpg"]
     audioExtensions = [".wav", ".mp3", ".ogg"]
     mediaExtensions = videoExtensions + audioExtensions

     path = x['mediaFile']
     urlSuffix = os.path.splitext(path)[1].lower()

     if not urlSuffix in mediaExtensions:
        raise MediaFormatError(mediaExtensions, urlSuffix)

     if(urlSuffix in videoExtensions):
       self.videoURL = path
     if(urlSuffix in audioExtensions):
       self.audioURL = path

     self.mediaFile = x['mediaFile']
     self.mimeType = x['mimeType']
     self.textEntry = x['textEntry']

     self.lines = x["lines"]
     lineCount = len(self.lines)

     for i in range(0, lineCount):
        self.lines[i]['number'] = i

     self.checkLines()  # throw exception if found invalid

   #----------------------------------------------------------------------
   # add quality checks here, just of the tieredLines
   #   all startTime and endTime must be integers
   #
   def checkLines(self):

         # first test: make sure all start and endTimes are integers
         # milliseconds from the beginning of the media recording

      startTimes = [x['startTime'] for x in self.tieredLines]
      endTimes   = [x['endTime'] for x in self.tieredLines]
      allTimes = startTimes + endTimes

      try:
         for time in allTimes:
           intTime = int(time)
      except ValueError as ve:
           # "None" suppresses the ValueError display
         raise(MillisecondTimeError(time)) from None

   #----------------------------------------------------------------------
   def getYamlObject(self):
      return self.obj

   #----------------------------------------------------------------------
   def getLineCount(self):
      return len(self.lines)

   #----------------------------------------------------------------------
   def getAudioURL(self):
      return self.audioURL

   #----------------------------------------------------------------------
   def getVideoURL(self):
      return self.videoURL

   #----------------------------------------------------------------------
   def getMediaURL(self):
      return self.mediaFile

   #----------------------------------------------------------------------
   def getMimeType(self):
      return self.mimeType

   #----------------------------------------------------------------------
   def getAllLines(self):
       return self.allLines
    
   def getHtmlLines(self):
      return self.htmlLines

   def getTieredLines(self):
      return self.tieredLines
       
   def getTieredLine(self, number):
      line = self.lines[number]
      
   #----------------------------------------------------------------------
   def getIjalLine(self, number):
      tierMap = self.tierInfo
      tierKeys = list(tierMap.keys())
      tierValues = list(tierMap.values())
      map = {v: k for k, v in tierMap.items()}
      line = self.lines[number]
      #assert(line['lineType'] == "ijal")
      keys = list(line.keys())
      canonicalKeys = ["startTime", "endTime", "speech", "morphemes",
                      "morpheme-gloss", "translation", "number"]
      lineNumber = line["number"]
      startTime = line["startTime"]
      endTime = line["endTime"]
      speech = line[tierMap["speech"]]
      morphemes = None
      if "morpheme" in tierKeys:
         morphemes = line[tierMap["morpheme"]]
      morphemeGlosses = None
      if "morphemeGloss" in tierKeys:
         morphemeGlosses = line[tierMap["morphemeGloss"]]
      translation = None
      if "translation" in tierKeys:
         translation = line[tierMap["translation"]]
      return{"lineNumber": lineNumber,
             "startTime": startTime,
             "endTime": endTime,
             "speech": speech,
             "morphemes": morphemes,
             "morphemeGlosses": morphemeGlosses,
             "translation": translation}
      
   #----------------------------------------------------------------------
   # line number and tier number, when different, accomodate the possible
   # presence of html lines in the self.lines list
   def getTieredLineObject(self, lineNumber, tierNumber):

      pdb.set_trace()
      tieredLine = TieredLine(self.lines, lineNumber, tierNumber,
                              self.getTierGuide(),
                              verbose=self.verbose)
      return (tieredLine)
      
   #----------------------------------------------------------------------
   def getHtmlLine(self, number):
      line = self.htmlLines[number]
      #assert(line['lineType'] == "html")
      #assert('content' in list(line.keys()))
      return(line['html'])
      
   #----------------------------------------------------------------------
   def getRawLines(self):
      return self.lines

   #----------------------------------------------------------------------
   def getLines(self):
      return self.lines

   #----------------------------------------------------------------------
   def getTierGuide(self):
      return self.tierGuide

   #----------------------------------------------------------------------
   def getTimeTable(self):

      startTimes = [line['startTime'] for line in self.tieredLines]
      endTimes = [line['endTime'] for line in self.tieredLines]
      self.timeTable = pd.DataFrame({"start": startTimes, "end": endTimes})
      return self.timeTable

   #----------------------------------------------------------------------
   def getTierTable(self):

      x = self.getYamlObject()
      lines = x['lines']
      fields = []
      for line in lines:
         fields.extend(list(line.keys()))
      tbl = pd.DataFrame({'fields':np.array(fields)})
      tbl = tbl['fields'].value_counts().to_frame()
      tbl.drop(['number'], inplace=True)
      tbl = tbl.reset_index() # move rownames to a new column
      tbl.columns = ['Field', 'Lines']

      return(tbl)

   #----------------------------------------------------------------------
   def parseAndSortAllLines(self):

      self.lines = list()
      for i in range(self.getLineCount()):
         if self.lineTypeSpecified:
            if(self.lines[i]['lineType'] == "html"):
               newLine = self.getHtmlLine(i)
            else:
               if self.tierGuideFile:
                  newLine = self.getTieredLine(i)
                  #newLine = self.getIjalLine(i)
         else:
            newLine = self.getTieredLine(i)
            #newLine = self.getIjalLine(i)
         self.lines.append(newLine)
      
   #----------------------------------------------------------------------
   def run(self):

      if(self.verbose):
         print("yamlParser.run, parsing & sorting all lines")
      self.parseAndSortAllLines()
   
   
