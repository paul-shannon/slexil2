import pdb
import os, re
from pathlib import Path
import pandas as pd
import numpy as np

class SFMT:

   textFile: None
   title = None
   speakers = []
   textEntry: None
   mediaFile: None
   lines = []
   htmlLines = []
   tieredLines = []
   lineOrderTable = None
   startLocs = []
   requiredFields = ["title", "speakers", "textEntry", "mediaFile",
                     "startTime", "endTime"]
   
   #------------------------------------------------------
   def __init__(self, textFile):

      assert(Path(textFile).is_file())
      self.textFile = textFile

      with open(self.textFile, 'r') as f:
        self.lines = f.readlines()
        self.lines = [line for line in self.lines if not re.search("^ *#", line)]
        self.lines = [line.rstrip("\n") for line in self.lines]
      lastLine = len(self.lines) - 1   # zero-based
      while (len(self.lines[lastLine].strip()) == 0):
          self.lines.pop()
          lastLine = lastLine - 1
      self.lastLine = lastLine

      self.parse()
      self.inferTierStructure()

   #------------------------------------------------------
   def getRawLines(self):
       return self.lines

   #------------------------------------------------------
   def getAllLines(self):

       return self.getRawLines()

   #------------------------------------------------------
   def getTierCount(self):

      return(len(self.blockStarts))

   #------------------------------------------------------
   def parse(self):

      self.linesSectionStart = [i for i in range(len(self.lines))
                                  if self.lines[i] == "lines:"][0]
      self.titleLine = [i for i in range(len(self.lines)) if "title: " in self.lines[i]]
      self.blankLines = [i for i in range(len(self.lines)) if len(self.lines[i].strip()) == 0]
      self.startLines = [i for i in range(len(self.lines))
                           if re.search("startTime", self.lines[i])]
      self.endLines = [i for i in range(len(self.lines)) if "endTime:" in self.lines[i]]
      assert(len(self.startLines) == len(self.endLines))
      self.htmlLines = [i for i in range(len(self.lines)) if "html:" in self.lines[i]]

      self.identifyTierBlocks()

      self.tieredLines = self.getTiers()
 
      titleLine = [line for line in self.lines if line.find("title:") == 0][0]
      title = titleLine.split("title:")[1].strip()
      self.title = title

      narratorLine = [line for line in self.lines if line.find("narrator:") == 0]
      speakersLine = [line for line in self.lines if line.find("speakers:") == 0]
      self.narrator = "unknown"
      
      if speakersLine:
         speakerString = speakersLine[0].split("speakers:")[1].strip()
         self.narrator = speakerString

      elif narratorLine:
         speakerString = narratorLine[0].split("narrator:")[1].strip()
         self.narrator = speakerString

      textEntryLine = [line for line in self.lines if line.find("textEntry:") == 0][0]
      textEntryString = textEntryLine.split("textEntry:")[1].strip()
      self.textEntry = textEntryString

      self.parseMediaInfo()

   #------------------------------------------------------
   def parseMediaInfo(self):
       
          #-----------------------------------------------
          # first, the media file url (or local filename)
          #-----------------------------------------------

     videoExtensions = [".m4v", ".mov", ".mp4", ".mpg"]
     audioExtensions = [".wav", ".mp3", ".ogg"]
     mediaExtensions = videoExtensions + audioExtensions

     mediaFileLine = [line for line in self.lines if line.find("mediaFile:") == 0][0]
     path = mediaFileLine.split("mediaFile: ")[1]
     self.mediaFile = path

     urlSuffix = os.path.splitext(path)[1].lower()

     if not urlSuffix in mediaExtensions:
        raise MediaFormatError(mediaExtensions, urlSuffix)

     self.videoURL = None
     if(urlSuffix in videoExtensions):
       self.videoURL = path

     self.audioURL = None
     if(urlSuffix in audioExtensions):
       self.audioURL = path

          #-----------------------------------------------
          # now the mimeType
          #-----------------------------------------------

     self.mimeType = "unknown"
     mimeTypeLines = [line for line in self.lines if line.find("mimeType:") == 0]
     if mimeTypeLines:
        mimeTypeLine = mimeTypeLines[0]
        self.mimeType = mimeTypeLine.split("mimeType: ")[1]

   #------------------------------------------------------
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
   def getTitle(self):
      return self.title

   #----------------------------------------------------------------------
   def getSpeakers(self):
      return self.narrator

   #----------------------------------------------------------------------
   def getTextEntry(self):
      return self.textEntry

   #----------------------------------------------------------------------
   def identifyTierBlocks(self):

      blockStarts = self.startLines
      self.blockStarts = blockStarts
      blockEnds = []
        # with each blockStart, look for the next blank line
      for i in blockStarts:
         j = i
         while not j in self.blankLines and j <= self.lastLine:
            j += 1
         blockEnds.append(j)
      self.blockEnds = blockEnds
      self.tierCount = len(self.blockStarts)

   #------------------------------------------------------
   # a 2-column table, with fields (tier names) and their
   # respective line counts
   def getTierTable(self):

      tierNames = self.allTierNames

         # initialize the counts
      fieldCounts = {}
      for field in tierNames:
         fieldCounts[field] = 0
     
      for line in self.tieredLines:
         fields = list(line.keys())
         for field in fields:
             if field in tierNames:
                fieldCounts[field] += 1
      tbl = pd.DataFrame(columns=["Field", "Lines"])
      tbl["Field"] = list(fieldCounts.keys())
      tbl["Lines"] = list(fieldCounts.values())
      #tbl = tbl.reset_index() # move rownames to a new column
      #tbl.columns = ['Field', 'Lines']

      return(tbl)

   #----------------------------------------------------------------------
   def getTier(self, i):

      tier = {}

      lineElements = self.lines[self.blockStarts[i]:self.blockEnds[i]]
      for lineElement in lineElements:
         lineElement = lineElement.strip()
         firstColonPos = lineElement.find(":")
         key = lineElement[:firstColonPos].strip()
         key = key.replace("- ", "") # in case, e.g., "- startTime: 1212"
         value = lineElement[firstColonPos+1:].strip()
           # is this a list, of the sort found in morpheme analysis tiers?
         if re.search("^\[", value) and re.search("\]$", value):
            s = re.sub("^\[", "", value)
            s = re.sub("\]$", "", s)
            value = s.split(",")
           # is it a time in milliseconds, convertible to int?
         elif key in ["startTime", "endTime"]:
            value = int(value)
         tier[key] = value

      return(tier)

   #------------------------------------------------------
   def getTiers(self):

      x = [self.getTier(i) for i in range(self.getTierCount())]

      return(x)

   #------------------------------------------------------
   def getTieredLines(self):

       return(self.getTiers())
   
   #------------------------------------------------------
   def getHtmlLines(self):

       return self.htmlLines

   #------------------------------------------------------
   # independently numbered html lines, starting at 0
   def getHtml(self, i):

      assert(i < len(self.htmlLines))

      lineNumber = self.htmlLines[i]
      htmlTextRaw = self.lines[lineNumber]
      htmlText = re.sub(r' *- *html: *', '', htmlTextRaw)

      done = False
      while not done:
          lineNumber += 1
          if lineNumber >= self.lastLine:
              done = True
          else:
             nextLine = self.lines[lineNumber]
             if len(nextLine.strip()) == 0:
                done = True
             else:
                #print(self.lines[lineNumber])
                htmlText = htmlText + self.lines[lineNumber]

          # remove any trailing quote if present

      htmlText = re.sub(r'^"', '', htmlText)
      htmlText = re.sub(r'"$', '', htmlText)
      
      return(htmlText)

   #------------------------------------------------------
   def getAllHtml(self):

      x = [self.getHtml(i) for i in range(len(self.htmlLines))]
      return(x)
  
   #------------------------------------------------------
   # when rendering a webpage, we want the tiered & html
   # lines in order, as specified in the input file
   # in the current design, we read
   #   all lines
   #   separate out each line by its key
   #   construct a TieredLine where we can
   #   collect, independently, the html lines
   # the strategy here is a bit of a hack, proceeds by
   #   finding the raw line number of each tiered and html line
   #   build a new heterogeneous list, tiered & html
   #   based upon the startTime or html key which identifies the line
   def getOrderedLineObjectsTieredAndHTML(self):

      htmlLineIndices = [i for i in range(len(self.lines)) if self.lines[i].find("html:") >= 0]
      tieredLineIndices = [i for i in range(len(self.lines)) if self.lines[i].find("startTime:") >= 0]
      tbl = pd.DataFrame(columns=["type", "rawIndex", "signature"])
      rowNumber = 0 
      for i in htmlLineIndices:
         signature = self.lines[i].split("html:")[1].strip()
         signature = signature.replace('"', '')
         row = {"type": "html", "rawIndex": i, "signature": signature}
         tbl.loc[rowNumber] = row
         rowNumber += 1

      for i in tieredLineIndices:
         row = {"type": "tier", "rawIndex": i,
                "signature": self.lines[i].split("startTime:")[1].strip()}
         tbl.loc[rowNumber] = row
         rowNumber += 1

     
      tbl = tbl.sort_values('rawIndex')
      tbl = tbl.reset_index()
      tbl = tbl.drop(['index'], axis=1)
      self.lineOrderTable = tbl
      return self.lineOrderTable

   #------------------------------------------------------
   def getTimeTable(self):

      startTimes = [line['startTime'] for line in self.tieredLines]
      endTimes = [line['endTime'] for line in self.tieredLines]
      self.timeTable = pd.DataFrame({"start": startTimes, "end": endTimes})
      return self.timeTable

   #------------------------------------------------------
   def inferTierStructure(self):

      self.nonTierFields = ["lineType", "startTime", "endTime", "lineNumber", "number"]

      self.tieredLines = self.getTiers()
      self.htmlLines = self.htmlLines

         #--------------------------------------------------
         # seed allTierNames, first, from the line with
         # the most tier names, in the order which they
         # appear there.  this order is the one most likely
         # desired by the user.
         # this solves the problem in which an early line
         # omits a higher ordered tier, only first seen
         # in a later line.
         #--------------------------------------------------
      maxFieldsInOneLine = max([len(line.keys()) for line in self.tieredLines])

      longestLines = [line for line in self.tieredLines if len(line.keys()) == maxFieldsInOneLine]

      allTierNames = list(longestLines[0].keys())

      if(len(longestLines) > 1):
         for longLine in longestLines[2:]:
            newKeys = list(longLine.keys())
            uniqueKeys = [k for k in newKeys if not k in allTierNames]
            allTierNames.extend(uniqueKeys)

      self.allTierNames = [el for el in allTierNames if el not in self.nonTierFields]


      self.identifyAnalysisTiers()
      self.identifyGenericTierNames()
      self.buildTierNameMap()

   #------------------------------------------------------------
   # in full IJAL mode, there will be two tiers containing, not
   # the usual text string, but an array of an equal number of tokens,
   # like this:
   #  morphemes: [en=il,mezz–o,de=il,cammin–Ø,di,nostr–a,vit–a]
   #  morpheme-gloss: [in=DEF:MASC:SG,middle-MASC:SG,of=DEF:MASC:SG,journey–MASC:SG,of,our-FEM:SG,life-FEM]
   #  find them here 
   def identifyAnalysisTiers(self):

      i = 0
      tiers = []
      tierListCounts = {}

      for tier in self.allTierNames:
         print("initializing counts for %s" % tier)
         tierListCounts[tier] = 0
      
      for line in self.tieredLines:
         i += 1
         for tierName in self.allTierNames:
            if tierName in line.keys():
                 # to handle "escaped sfmt", where even lists are simple strings,
                 # this next sfmt-parses  each incoming string, to reveal
                 # it's internal list structure, if present
               s = line[tierName]
               if type(s) is list:
                  tierListCounts[tierName] += 1
                   
         # we recognized analysis tiers as those
         #   with a high percentage of list values, e.g., [aa, bb]
         # an equal, or nearly equal number of matched lines in
         # a second tier

      tierCount = len(tierListCounts)
      total = 0
      [total := total + x for x in tierListCounts.values()]
      fraction = 0.8  # allow for a few possibly scalar single analysis terms
      threshold = len(self.tieredLines) * fraction
      analysisCandidates = []
      for tierName in list(tierListCounts.keys()):
         if tierListCounts[tierName] > threshold:
             analysisCandidates.append(tierName)
      self.allAnalysisTierNames = []
      if len(analysisCandidates) > 1:
         self.allAnalysisTierNames = list(sorted(set(analysisCandidates),
                                          key=analysisCandidates.index))
      print("atn: %s" % repr (self.allAnalysisTierNames))

   #------------------------------------------------------------
   # tiers which are neither speech, meta-fields, nor analysis
   def identifyGenericTierNames(self):

      #traceFileName = "inferTierStructureFromSFMT"
      #traceLineNumber = 102
      #print("--- trace: %s at %d" % (traceFileName, traceLineNumber))

      candidateTiers = self.allTierNames
      speechTierName = list(self.getSpeechTierNameMap().values())
      analysisTierNames = self.allAnalysisTierNames #list(self.getAnalysisTierNameMap().values())
      
      generics = [el for el in candidateTiers if el not in speechTierName]
      generics = [el for el in generics       if el not in analysisTierNames]
      #pdb.set_trace()
      self.genericTierNames = generics
      
   #------------------------------------------------------------
   def getAllTierNames(self):

      return(self.allTierNames)

   #------------------------------------------------------------
   def getSpeechTierNameMap(self):

      return({"speech": self.allTierNames[0]})

   #------------------------------------------------------------
   def getSpeechTierName(self):

      return(self.allTierNames[0])

   #------------------------------------------------------------
   def getGenericTierNameMap(self):

      allKeys = list(self.tierNameMap.keys())
      genericKeys = [string for string in allKeys if string.startswith("tier_")]
      subMap = dict((k, self.tierNameMap[k]) for k in genericKeys)
      #print("returning subMap from getGenericTierNameMap")
      #print(repr(subMap))
      return(subMap)

   #------------------------------------------------------------
   def getAnalysisTierNameMap(self):

      allKeys = list(self.tierNameMap.keys())
      analysisKeys = [string for string in allKeys if string.startswith("analysis_")]
      subMap = dict((k, self.tierNameMap[k]) for k in analysisKeys)
      return(subMap)

   #------------------------------------------------------------
   # with tierGuides now being (mostly) obsolete, not sure if
   # the approach encoded below does the job
   def writeTierGuide(self, tierGuideFilename):

      with open(tierGuideFilename, 'w') as f:
         f.write(repr(self.tierNameMap))

   #------------------------------------------------------------
   # map from standard names (e.g., speech; tier_[1..N]; analysis_[1,2])
   # to the given tier names
   #   (e.g., italianSpeech; soundsLike,english,speaker; analysis_1, analysis_2
   def buildTierNameMap(self):

      tg = {}
      tg["speech"] = self.getSpeechTierName()
      atn = self.allAnalysisTierNames #list(self.getAnalysisTierNameMap().values())

      tierNames = self.getAllTierNames()

      analysisTierCount = 0
      genericTierCount = 0


      for tier in tierNames[1:]:
         if tier in atn:
            analysisTierCount += 1
            tg["analysis_%d" % analysisTierCount] = tier
         else:
            genericTierCount += 1
            tg["tier_%d" % genericTierCount] = tier

      self.tierNameMap = tg
      
   #------------------------------------------------------------
   def getTierGuide(self):

      return(self.tierNameMap)
