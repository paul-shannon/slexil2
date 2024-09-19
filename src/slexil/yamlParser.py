# -*- tab-width: 3 -*-
#-------------------------------------------------------------------------------
import os, sys
import xmlschema
from urllib.parse import urlparse
from lxml import etree
import yaml
import pandas as pd
pd.set_option('display.width', 1000)
import pdb
#-------------------------------------------------------------------------------
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
class YamlParser:

   yamlFile = ''
   obj = None
   tierGuideFile = None
   htmlLines = []
   ijalLines = []
   lineCount = None
   tierInfo = None
   timeTable = None
   lineTable = None
   linesAll = list()
   verbose = False
   metadata = None
   audioURL = None
   videoURL = None
   mimeType = None
   fixOverlappingTimeSegments = False

   def __init__(self, yamlFile, tierGuideFile=None, verbose=False, fixOverlappingTimeSegments=False):

     self.yamlFile = yamlFile
     self.tierInfo = yaml.load(open(tierGuideFile), Loader=yaml.FullLoader)
     x = yaml.load(open(yamlFile), Loader=yaml.FullLoader)
     self.obj = x
     expectedFields = ['title', 'narrator', 'textEntry', 'mediaFile', 'mimeType', 'lines']
     assert(list(x.keys()) == expectedFields)

     self.title = x['title']
     self.narrator = x['narrator']

     videoExtensions = (".m4v", ".mov", ".mp4")
     audioExtensions = (".wav", ".mp3")

     path = x['mediaFile']
     urlSuffix = os.path.splitext(path)[1].lower()
     assert(urlSuffix in videoExtensions + audioExtensions)

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
        

     self.htmlLines = [line for line in x['lines'] if line['lineType']=='html']
     self.ijalLines = [line for line in x['lines'] if line['lineType']=='ijal']


   def getLineCount(self):
      return len(self.lines)

   def getAudioURL(self):
      return self.audioURL

   def getVideoURL(self):
      return self.videoURL

   def getMimeType(self):
      return self.mimeType

   def getIjalLine(self, number):
      tierMap = self.tierInfo
      tierKeys = list(tierMap.keys())
      tierValues = list(tierMap.values())
      map = {v: k for k, v in tierMap.items()}
      line = self.lines[number]
      assert(line['lineType'] == "ijal")
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
      
   def getHtmlLine(self, number):
      line = self.lines[number]
      assert(line['lineType'] == "html")
      assert('content' in list(line.keys()))
      return(line['content'])
      
   def getAllLines(self):
      return self.linesAll
   

   def getTierInfo(self):
      return self.tierInfo

   def getTimeTable(self):
      startTimes = [line['startTime'] for line in self.ijalLines]
      endTimes = [line['endTime'] for line in self.ijalLines]
      self.timeTable = pd.DataFrame({"start": startTimes, "end": endTimes})
      return self.timeTable

   def parseAndSortAllLines(self):

      self.linesAll = list()
      for i in range(self.getLineCount()):
         if(self.lines[i]['lineType'] == "html"):
            newLine = self.getHtmlLine(i)
         else:
            newLine = self.getIjalLine(i)
         self.linesAll.append(newLine)
      
   def run(self):

      if(self.verbose):
         print("yamlParser.run, parsing & sorting all lines")
      self.parseAndSortAllLines()
   
   
