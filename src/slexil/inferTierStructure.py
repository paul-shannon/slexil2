# -*- tab-width: 3 -*-
#-------------------------------------------------------------------------------
import yaml
# import pandas as pd
import os
import pdb
#-------------------------------------------------------------------------------
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
class InferTierStructure:

   xmlFilename = ''
   parser = None
   doc = None
   tiersList = []
   lineDict = None
   tbl = None
   allAnalysisTierNames = []

   #------------------------------------------------------------
   def __init__(self, yamlFilenameOrParsedLines, verbose=False):

      if(not isinstance(yamlFilenameOrParsedLines, list)):
         assert(os.path.isfile(yamlFilenameOrParsedLines))
         x = yaml.load(open(yamlFilenameOrParsedLines), Loader=yaml.FullLoader)
         self.lines = x['lines']
      elif((isinstance(yamlFilenameOrParsedLines, list) and
            isinstance(yamlFilenameOrParsedLines[0], dict))):
         self.lines = yamlFilenameOrParsedLines
      else:
         msg = "inferTierStructure requires a yaml file name or a list of slexil lines"
         raise Exception(msg)
      self.nonTierFields = ["lineType", "startTime", "endTime", "lineNumber", "number"]

      self.tieredLines = []
      self.htmlLines = []

         #--------------------------------------------------
         # seed allTierNames, first, from the line with
         # the most tier names, in the order which they
         # appear there.  this order is the one most likely
         # desired by the user.
         # this solves the problem in which an early line
         # omits a higher ordered tier, only first seen
         # in a later line.
         #--------------------------------------------------
      self.allTierNames = []
      maxFieldsInOneLine = max([len(line.keys()) for line in self.lines])
      longestLine = [line for line in self.lines if len(line.keys()) == maxFieldsInOneLine]
      allTierNames = list(longestLine[0].keys())
      self.allTierNames = [el for el in allTierNames if el not in self.nonTierFields]
      
      for i in range(len(self.lines)):
         line = self.lines[i]
         if list(line.keys())[0] == "html":
            self.htmlLines.append(line)
         else:
            self.tieredLines.append(line)
            fields = list(line.keys())
            candidates = [el for el in fields if el not in self.nonTierFields]
            newTierNames = [el for el in candidates if el not in self.allTierNames]
            self.allTierNames.extend(newTierNames)

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
      for line in self.tieredLines:
         i += 1
         analysisTiers = []
         for tierName in self.allTierNames:
            if tierName in line.keys():
                 # to handle "escaped yaml", where even lists are simple strings,
                 # this next yaml-parses  each incoming string, to reveal
                 # it's internal list structure, if present
               s = line[tierName]
               #traceFileName = "inferTierStructure.py"
               #traceLineNumber = 89
               #print("--- trace: %s at %d" % (traceFileName, traceLineNumber))
               #print(s)               
               # pdb.set_trace()
               if type(s) is str:
                  text = yaml.safe_load(s)
               else:  # a list
                  text = s
               #print("--- trace: %s at %d" % ("inferTierStructure.py", 85))
               #print("text: %s" % line[tierName])
               #print("type: %s" % type(line[tierName]))
               #pdb.set_trace()
               #text = yaml.safe_load(line[tierName])
               if type(text) is list:
                  tokenCount = len(text)
                  analysisTiers.append(tierName)
         if len(analysisTiers) > 1:
            tiers.extend(analysisTiers)

      tiers = list(sorted(set(tiers), key=tiers.index))
      self.allAnalysisTierNames = []

      if(len(tiers) >= 2):   # if just 1, it will be treated as a generic tier
         self.allAnalysisTierNames = tiers

   #------------------------------------------------------------
   # tiers which are neither speech, meta-fields, nor analysis
   def identifyGenericTierNames(self):

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
      return(subMap)

   #------------------------------------------------------------
   def getAnalysisTierNameMap(self):

      allKeys = list(self.tierNameMap.keys())
      analysisKeys = [string for string in allKeys if string.startswith("analysis_")]
      subMap = dict((k, self.tierNameMap[k]) for k in analysisKeys)
      return(subMap)

   #------------------------------------------------------------
   def writeTierGuide(self, tierGuideFilename):

      string = yaml.dump(self.tierNameMap, default_flow_style=False, sort_keys=False)

      with open(tierGuideFilename, 'w') as f:
         f.write(string)

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
   def getAllLines(self):
      return self.lines
   
   #------------------------------------------------------------
   def getTieredLines(self):
      return self.tieredLines
   
   #------------------------------------------------------------
   def getHtmlLines(self):
      return self.htmlLines
   
   #------------------------------------------------------------
   def getTierGuide(self):

      return(self.tierNameMap)
      
#----------------------------------------------------------------------------------
