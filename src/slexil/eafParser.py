# -*- tab-width: 3 -*-
#-------------------------------------------------------------------------------
import os, sys
import xmlschema
from urllib.parse import urlparse
#from xml.etree import ElementTree as etree
from lxml import etree
import yaml
import pandas as pd
import numpy as np
pd.set_option('display.width', 1000)
pd.set_option('display.max_columns', None)
import pdb
#-------------------------------------------------------------------------------
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
class EafParser:

   xmlFilename = ''
   doc = None
   lineCount = None
   tierTable = None
   timeTable = None
   lineTable = None
   linesAll = list()
   tiersWithTabs = None
   verbose = False
   metadata = None
   audioURL = None
   videoURL = None
   mediaURL = None
   audioMimeType = None
   videoMimeType = None
   fixOverlappingTimeSegments = False

   def __init__(self, xmlFilename, verbose=False, fixOverlappingTimeSegments=False):

      self.xmlFilename = xmlFilename
      self.xmlValid()
      self.verbose = verbose
      self.fixOverlappingTimeSegments = fixOverlappingTimeSegments
      self.tiersWithTabs = list()

      if(verbose):
         print("EafParser etree parse")
      self.doc = etree.parse(xmlFilename)
      self.rootTimeAlignedTiers = extractAllTimeAlignedTierIDs(xmlFilename)

      if(verbose):
         print("EafParser extracting metadata")
      self.extractMetadata()

      if(verbose):
         print("EafParser extracting media info")
      self.extractMediaInfo()

      if(verbose):
         print("EafParser count lines")
      self.lineCount = len(self.doc.findall("TIER/ANNOTATION/ALIGNABLE_ANNOTATION"))

      if(verbose):
         print("EafParser.run, constructing tier table")
      self.constructTierTable()
      self.constructRichTierTable()

      if(verbose):
         print("EafParser.run, constructing time table")
      self.constructTimeTable()

      if(verbose):
         print("EafParser leaving constructor")

   #----------------------------------------------------------------------------------
   def run(self):

      if(self.verbose):
         print("EafParser.run, parsing & sorting all lines")
      self.parseAndSortAllLines()

      if(self.verbose):
         print("EafParser.run, complete")
      
   #----------------------------------------------------------------------------------
   def xmlValid(self):
      assert(len(self.xmlFilename) > 4)
      #baseDir = "/Users/paul/github/slexil2/testData"
      #schemaFile = os.path.join(baseDir, "EAFv3.0.xsd")
      #assert(os.path.isfile(schemaFile))
          # takes only ~500 msecs to load the schema file
      schemaFile = "http://www.mpi.nl/tools/elan/EAFv3.0.xsd" 
      valid = False
      #try:
      if(self.verbose): 
         print("--- about to call xmlschema.validate")
      xmlschema.validate(self.xmlFilename, schemaFile)
      if(self.verbose): 
         print("--- after call to xmlschema.validate")
      return(True)
      #valid = True
      #except xmlschema.validators.exceptions.XMLSchemaValidationError as e:
      #  print("error")
      #  print(e)
      #return(valid)

      
   #----------------------------------------------------------------------------------
   def getFilename(self):
      return(self.xmlFilename)

   def getRootTimeAlignedTiers(self):
      return(self.rootTimeAlignedTiers)

   def getLineCount(self):
      return(self.lineCount)

   def getTierTable(self):
      return self.tierTable
   
   def getRichTierTables(self):
      return (self.richTierTable, self.richTierTableDistilled)
   
   def setAudioURL(self, newURL):
      self.audioURL = newURL

   def getAudioURL(self):
      return self.audioURL

   def getAudioMimeType(self):
      return self.audioMimeType

   def getVideoURL(self):
      return self.videoURL

   def getVideoMimeType(self):
      return self.videoMimeType

   def getMediaURL(self):
      return self.mediaURL

   def getMetadata(self):
      return(self.metadata)

   def getAudioInfo(self):
      return({"url": self.audioURL, "mimetype": self.mediaMimeType})

   def getVideoInfo(self):
      return({"url": self.videoURL, "mimetype": self.mediaMimeType})

   def getTierTable(self):
      return(self.tierTable)

   def getTimeTable(self):
      return(self.timeTable)

   def getAllLinesTable(self):
      return(self.linesAll)

   #----------------------------------------------------------------------------------
   def checkAgainstTierGuide(self, tierGuideFile):

      tierElements = self.doc.findall("TIER")
      tierIDs = [tier.attrib["TIER_ID"] for tier in tierElements]
      with open(tierGuideFile, 'r') as f:
         tierGuide = yaml.safe_load(f)
      documentedTierIDs = list(tierGuide.values())
      undocumentedInXmlFile = list(set(documentedTierIDs).difference(set(tierIDs)))
      valid = (undocumentedInXmlFile == [])
      return ({"valid": valid, "failures": undocumentedInXmlFile})

#     try:
#     assert(len(undocumentedInXmlFile) == 0)
#        except AssertionError as e:
#     msg = "unrecognized tierIDs in eaf file: "
#           for unknown in undocumentedInXmlFile:
#            unknowns = "%s %s" % (unknowns, unknown)
#         msg = "%s %s" % (msg, unknowns)
#         raise Exception(msg)
            
   #----------------------------------------------------------------------------------
   def extractMetadata(self):
      if (self.verbose):
         print("--- entering extractMetadata")
      properties = self.doc.findall("HEADER")[0].findall("PROPERTY")
      metadata = {}
      for prop in properties:
         name = prop.attrib["NAME"]
         if("metadata:" in name):
            name = name.replace("metadata:","")
            value = prop.text
            metadata[name] = value
      self.metadata = metadata

   #--------------------------------------------------------------------------------   
   def extractMediaInfo(self):
      if(self.verbose):
         print("--- entering extractMediaInfo")
      x = self.doc.findall("HEADER")[0].findall("MEDIA_DESCRIPTOR")

      videoExtensions = (".m4v", ".mov", ".mp4")
      audioExtensions = (".wav", ".mp3")

      for el in x:
        url = el.attrib["MEDIA_URL"]
        path = urlparse(el.attrib["MEDIA_URL"]).path
        urlSuffix = os.path.splitext(path)[1].lower()

        if(urlSuffix in videoExtensions):
           self.videoURL = url
           self.videoMimeType = el.attrib["MIME_TYPE"]
           self.mediaURL = self.videoURL
           self.mediaMimeType = self.videoMimeType
           break;   # video preferred over audio if both are present
        else:
           self.audioURL = url
           self.audioMimeType = el.attrib["MIME_TYPE"]
           self.mediaURL = self.audioURL
           self.mediaMimeType = self.audioMimeType


   #--------------------------------------------------------------------------------   
   # the rich tierTables add extra information to the historically
   # basic one:
   #                  TIER_ID       PARENT_REF  LINES LINGUISTIC_TYPE_REF TIME_ALIGNABLE
   # 0              TRS-Ortho              NaN     15          default-lt           true
   # 1          TRS Broad IPA        TRS-Ortho     15           TRS-Broad          false
   # 2       Free Translation        TRS-Ortho     15    Free Translation          false
   # 3        Tokenization-cp        TRS-Ortho    141      Tokenization 2          false
   # 4  Tokenization-Gloss-cp  Tokenization-cp    141                 POS          false
   #
   # richTierTable:
   #                  TIER_ID       PARENT_REF  LINES LINGUISTIC_TYPE_REF   root                                                ids
   # 0              TRS-Ortho              NaN     15          default-lt   True                                                 []
   # 1          TRS Broad IPA        TRS-Ortho     15           TRS-Broad  False  [a8, a9, a67, a69, a10, a70, a11, a71, a72, a1...
   # 2       Free Translation        TRS-Ortho     15    Free Translation  False  [a15, a16, a662, a373, a17, a656, a18, a657, a...
   # 3        Tokenization-cp        TRS-Ortho    141      Tokenization 2  False  [a374, a375, a376, a377, a378, a379, a380, a38...
   # 4  Tokenization-Gloss-cp  Tokenization-cp    141                 POS  False  [a515, a516, a620, a517, a518, a519, a621, a52...
   #
   # richTierTableTrimmed (keeps only the tiers with ~same number of lines
   # in this example, the 141 line tiers have analyses separated out,
   # which slexil at present cannot handle.
   #             TIER_ID LINGUISTIC_TYPE_REF PARENT_REF   root  LINES                                                ids
   # 0         TRS-Ortho          default-lt        NaN   True     15                                                 []
   # 1     TRS Broad IPA           TRS-Broad  TRS-Ortho  False     15  [a8, a9, a67, a69, a10, a70, a11, a71, a72, a1...
   # 2  Free Translation    Free Translation  TRS-Ortho  False     15  [a15, a16, a662, a373, a17, a656, a18, a657, a...

   def constructRichTierTable(self):

      #----------------------------------------------------
      def getTimeAlignedTierIDs(doc):
         tierTypes = doc.findall("LINGUISTIC_TYPE")
         timeAlignedTierIDs = []
         for tierType in tierTypes:
            id = tierType.attrib['LINGUISTIC_TYPE_ID']
            if 'TIME_ALIGNABLE' in tierType.attrib.keys():
              value = tierType.attrib['TIME_ALIGNABLE']
              if value == "true":
                 timeAlignedTierIDs.append(id)
         return(timeAlignedTierIDs)

      #----------------------------------------------------
      def findRootTiers(doc):
         timeAlignedTiers = getTimeAlignedTierIDs(doc)
         tiers = doc.findall("TIER")
         rootTiers = []
         for tier in tiers:
            attributes = tier.attrib.keys()
            orphan = not 'PARENT_REF' in attributes
            tierType = tier.attrib['LINGUISTIC_TYPE_REF']
            timeAligned = tierType in timeAlignedTiers
            if orphan and timeAligned:
              rootTiers.append(tier.attrib['TIER_ID'])
         return(rootTiers)
      #----------------------------------------------------
      tiers = self.doc.findall("TIER")
      attributeNamesRaw = [list(tier.attrib.keys()) for tier in tiers]
      attributeNamesWithDups = [item for sublist in attributeNamesRaw for item in sublist]
      attributeNames = list(set(attributeNamesWithDups)) # uniquify
      attributeNames.sort()
   
      tbl = pd.DataFrame(columns=attributeNames)
  
      row = -1
      for tier in tiers:
         row = row + 1
         attributes = tier.attrib.keys()
         for attrib in attributes:
            value = tier.attrib[attrib]
            tbl.loc[row, attrib] = value
          
      coi = ["TIER_ID", "LINGUISTIC_TYPE_REF", "PARENT_REF", "DEFAULT_LOCALE"]
      tbl = tbl.reindex(columns=coi)
      isRootTier = [id in findRootTiers(self.doc) for id in tbl['TIER_ID']]
      tbl['root'] = isRootTier

      kidCount = [len(tier.getchildren()) for tier in tiers]
      tbl['LINES'] = kidCount

        # we may wish to exclude a tier's dependent  elements
        # for example, of there more dependents than parents,
        # 
      kidIDs = []
      for tier in tiers:
        kidIDs.append([el.get("ANNOTATION_ID") for el in tier.findall("ANNOTATION/REF_ANNOTATION")])
      tbl['ids'] = kidIDs
          
       # we only want tiers which have very nearly the same
       # number of lines as the root.  this avoids trying
       # to render descendnet tiers in which, for instance,
       # each morpheme is a separate entry

  
      cDrops = ["LINGUISTIC_TYPE_ID", "DEFAULT_LOCALE",
                "CONSTRAINTS", "GRAPHIC_REFERENCES"]
      for cDrop in cDrops:
        if cDrop in list(tbl.columns):
           tbl = tbl.drop(columns=cDrop)


      coi = ["TIER_ID", "PARENT_REF", "LINES", "LINGUISTIC_TYPE_REF", "root", "ids"]
      tierTable = tbl[coi]

      rootLineCount = int(tbl[tbl['root'] == True]['LINES'][0])
      lowerBound = (rootLineCount * 0.9)
      upperBound = (rootLineCount * 1.1)
      tierTableDistilled = tbl[(tbl['LINES'] > lowerBound) & (tbl['LINES'] < upperBound)]
      tierTableDistilled.reset_index(inplace=True, drop=True)

      self.richTierTable = tierTable
      self.richTierTableDistilled = tierTableDistilled
       
   #----------------------------------------------------------------------------------
   def constructTierTable(self):

         # first get the possible LINGUISTIC_TYPE_REFS.  each tier must have this
      types = self.doc.findall("LINGUISTIC_TYPE")
      attributeNamesRaw = [list(type.attrib.keys()) for type in types]
      attributeNamesWithDups = [item for sublist in attributeNamesRaw for item in sublist]
      attributeNames = list(set(attributeNamesWithDups)) # uniquify
      attributeNames.sort()

      tbl_types = pd.DataFrame(columns=attributeNames)

      row = -1
      for type in types:
         row = row + 1
         attributes = type.attrib.keys()
         for attrib in attributes:
            value = type.attrib[attrib]
            #print("    %s: %s" % (attrib, value))
            tbl_types.loc[row, attrib] = value
            
      tiers = self.doc.findall("TIER")
      attributeNamesRaw = [list(tier.attrib.keys()) for tier in tiers]
      attributeNamesWithDups = [item for sublist in attributeNamesRaw for item in sublist]
      attributeNames = list(set(attributeNamesWithDups)) # uniquify
      attributeNames.sort()
         
      tbl = pd.DataFrame(columns=attributeNames)
         
      row = -1
      for tier in tiers:
         row = row + 1
         attributes = tier.attrib.keys()
         for attrib in attributes:
            value = tier.attrib[attrib]
            tbl.loc[row, attrib] = value
            
      coi = ["TIER_ID", "LINGUISTIC_TYPE_REF", "PARENT_REF", "DEFAULT_LOCALE"]
      tbl = tbl.reindex(columns=coi)
      tbl = pd.merge(tbl, tbl_types,
                  left_on="LINGUISTIC_TYPE_REF", right_on="LINGUISTIC_TYPE_ID")

      kidCount = [len(tier.getchildren()) for tier in tiers]
      tbl['LINES'] = kidCount

      cDrops = ["LINGUISTIC_TYPE_ID", "DEFAULT_LOCALE",
               "CONSTRAINTS", "GRAPHIC_REFERENCES"]
      for cDrop in cDrops:
         if cDrop in list(tbl.columns):
           tbl = tbl.drop(columns=cDrop)

      coi = ["TIER_ID", "PARENT_REF", "LINES", "LINGUISTIC_TYPE_REF",
             "TIME_ALIGNABLE"]
      self.tierTable = tbl[coi]
      



   #----------------------------------------------------------------------------------
    # def testParentTierReferences(self):
    #   # get the unique ids of supposed parents.  the first tier has no parent
    #
    #    allFound = True
    #
    #    for ref in parentReferences:
    #
    #       if not found:
    #
    #          missing.append(ref)#
    #        

   def constructTimeTable(self):

      timeSlotElements = self.doc.findall("TIME_ORDER/TIME_SLOT")
      timeIDs = [x.attrib["TIME_SLOT_ID"] for x in timeSlotElements]
      times = [int(x.attrib["TIME_VALUE"]) for x in timeSlotElements]
      audioTiers = self.doc.findall("TIER/ANNOTATION/ALIGNABLE_ANNOTATION")
      self.lineCount = len(audioTiers)
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
         # now to rename, then reorder columns
      tbl.columns = ["lineID", "t1", "start", "t2", "end"]
      tbl = tbl[["lineID", "start", "end", "t1", "t2"]]

         # sort these times, and the row numbers (indices)
      tbl = tbl.sort_values(by="start")
      tbl.reset_index(inplace=True, drop=True)

         # to ensure clean single line playback, the start time of the
         # n+1 line must be larger than the end time of the nth line.
         # find offenders here and fix them

      if(self.fixOverlappingTimeSegments):
         starts = list(tbl["start"])
         ends = list(tbl["end"])
         rowCount = tbl.shape[0]
         for i in range(0,rowCount-1):
            if (ends[i] >= starts[i+1]):
               ends[i] = starts[i+1] - 100
         tbl["end"] = ends

      self.timeTable = tbl


   #----------------------------------------------------------------------------------
   def fixOverlappingTimeSegments(self):

      self.timeTable["end"] = ends

   #----------------------------------------------------------------------------------
      # a hack: recursive, it works but only via visitList, at surrounding
      # function scope.  to be improved.
   def depthFirstTierTraversal(self, parentID):
      visitList = []
      def dfs(visited, doc, annotationID):
            if(annotationID not in visitList):
                  visitList.append(annotationID)
                  pattern = "TIER/ANNOTATION/REF_ANNOTATION[@ANNOTATION_REF='%s']" % annotationID
                  kidElements = doc.findall(pattern)
                  kids = [kid.attrib["ANNOTATION_ID"] for kid in kidElements]
                  for kid in kids:
                        dfs(visitList, doc, kid)

      dfs(visitList, self.doc, parentID)
      visitList.remove(parentID)
      return(visitList)

   #----------------------------------------------------------------------------------
   def getLineTable(self, lineNumber):

      rowNumber = lineNumber - 1 # rows are 0-based, lines are 1-based
      x = self.doc.findall('TIER/ANNOTATION/ALIGNABLE_ANNOTATION')[rowNumber]
      parentID = x.attrib["ANNOTATION_ID"]
      tierType = x.getparent().getparent().attrib["LINGUISTIC_TYPE_REF"]
      tierID   = x.getparent().getparent().attrib["TIER_ID"]
      xValue = x.find("ANNOTATION_VALUE")
      alignedID = x.attrib["ANNOTATION_ID"]
      timeSlotRefStart = x.attrib["TIME_SLOT_REF1"]
      timeSlotRefEnd = x.attrib["TIME_SLOT_REF2"]
      startTime = self.timeTable[self.timeTable['t1'] == timeSlotRefStart]["start"].tolist()[0]
      endTime = self.timeTable[self.timeTable['t2'] == timeSlotRefEnd]["end"].tolist()[0]
      contents = xValue.text
      tbl = pd.DataFrame({"id": alignedID,
                          "parent": "",
                          "startTime": startTime,
                          "endTime": endTime,
                          "tierID": tierID,
                          "tierType": tierType,
                          "text": contents,
                          "tabCount": 0}, index=[0])
      
      childIDs = self.depthFirstTierTraversal(parentID)
        # the rich tierTables add extra information to the historically
        # basic tierTable
        #                  TIER_ID       PARENT_REF  LINES LINGUISTIC_TYPE_REF TIME_ALIGNABLE
        # 0              TRS-Ortho              NaN     15          default-lt           true
        # 1          TRS Broad IPA        TRS-Ortho     15           TRS-Broad          false
        # 2       Free Translation        TRS-Ortho     15    Free Translation          false
        # 3        Tokenization-cp        TRS-Ortho    141      Tokenization 2          false
        # 4  Tokenization-Gloss-cp  Tokenization-cp    141                 POS          false
        #
        # richTierTable:
        #                  TIER_ID       PARENT_REF  LINES LINGUISTIC_TYPE_REF   root                                                ids
        # 0              TRS-Ortho              NaN     15          default-lt   True                                                 []
        # 1          TRS Broad IPA        TRS-Ortho     15           TRS-Broad  False  [a8, a9, a67, a69, a10, a70, a11, a71, a72, a1...
        # 2       Free Translation        TRS-Ortho     15    Free Translation  False  [a15, a16, a662, a373, a17, a656, a18, a657, a...
        # 3        Tokenization-cp        TRS-Ortho    141      Tokenization 2  False  [a374, a375, a376, a377, a378, a379, a380, a38...
        # 4  Tokenization-Gloss-cp  Tokenization-cp    141                 POS  False  [a515, a516, a620, a517, a518, a519, a621, a52...
        #
        # richTierTableTrimmed (keeps only the tiers with ~same number of lines
        # in this example, the 141 line tiers have analyses separated out,
        # which slexil at present cannot handle.
        #             TIER_ID LINGUISTIC_TYPE_REF PARENT_REF   root  LINES                                                ids
        # 0         TRS-Ortho          default-lt        NaN   True     15                                                 []
        # 1     TRS Broad IPA           TRS-Broad  TRS-Ortho  False     15  [a8, a9, a67, a69, a10, a70, a11, a71, a72, a1...
        # 2  Free Translation    Free Translation  TRS-Ortho  False     15  [a15, a16, a662, a373, a17, a656, a18, a657, a...

      (richTierTable, richTierTableTrimmed) = self.getRichTierTables()
      keepers = []
      [keepers.extend(ids) for ids in richTierTableTrimmed['ids']]
      
      for childID in childIDs:
         if not childID in keepers:
             continue
         searchPattern = "TIER/ANNOTATION/REF_ANNOTATION[@ANNOTATION_ID='%s']" %  childID
         #print("childID: %s  searchPattern: %s" % (childID, searchPattern))
         child = self.doc.find(searchPattern)
         tierType = child.getparent().getparent().attrib["LINGUISTIC_TYPE_REF"]
         tierID = child.getparent().getparent().attrib["TIER_ID"]
         parentID = ""
         if("ANNOTATION_REF" in child.attrib):
            parentID = child.attrib["ANNOTATION_REF"]
         childContents = child.find("ANNOTATION_VALUE").text
         tabCount = 0
         if childContents:
            tabCount = childContents.count("\t")
            if(tabCount > 0):
               self.tiersWithTabs.append(tierID)
               self.tiersWithTabs = list(set(self.tiersWithTabs))
         nextRow = tbl.shape[0]
         tbl.loc[nextRow] = {"id": childID,
                             "parent": parentID,
                             "tierType": tierType,
                             "tierID": tierID,
                             "text": childContents,
                             "tabCount": tabCount}

      self.lineTable = tbl
      return(tbl)
      
   #----------------------------------------------------------------------------------
   def parseAndSortAllLines(self):

      self.linesAll = list()


      for i in range(self.getLineCount()):
         tbl = self.getLineTable(i+1)
         self.linesAll.append(tbl)
         # do in-place sort of self.linesAll, using startTime
         # of the time aligned tier in each line 
      def sortFunction(tbl):
         return(tbl.loc[0].startTime)

      self.linesAll.sort(reverse=False, key=sortFunction)
      
   #----------------------------------------------------------------------------------
   def lineToYAML(self, tbl, lineNumber):

      rowCount = tbl.shape[0]
      textOut = []
      textOut.append("  - lineNumber: %d" % lineNumber)
      textOut.append("    startTime: %d"  % tbl.loc[0]['startTime'])
      textOut.append("    endTime: %d"  % tbl.loc[0]['endTime'])

        # first tier (first row) is presumed to be time-aligned, the
        # spoken text.  quote it, with pipe character, so that characters
        # (like curly brace, question mark, square bracket), reserved by yaml,
        # are left uninterpreted.
        #
      for row in range(0, rowCount):
         tierName = tbl.loc[row]['tierID']
         rawText = tbl.loc[row]['text']
         if rawText == None:
            continue
         rawText = rawText.replace("\n", " ")
         tabsFound = rawText.find("\t") > 0
         # if tabsFound:
         if tierName in self.tiersWithTabs:
            text = str(rawText.split("\t"))
            text = text.replace(": ", ":")
            text = text.replace("'", "")
            text = text.replace(" ", "")
            text = text.replace("?", "ʔ")
            textOut.append("    %s: %s" % (tierName, text))
            #textOut.append("    %s: |\n         %s" % (tierName, text))
         else:
            textOut.append("    %s: |\n         %s" % (tierName, rawText))
            #if row == 0:
            #   text = '"%s"' % rawText
            #else:
            #   text = rawText
      return textOut
        

   #----------------------------------------------------------------------------------
   def getTimeAlignedTiers(self):

      tbl = self.tierTable
      timeAlignedTiers = list(tbl[tbl["TIME_ALIGNABLE"] == "true"]["TIER_ID"])
      return timeAlignedTiers

   #----------------------------------------------------------------------------------
   def getTimeAlignedTierChildren(self, timeAlignedTierID):
           # find a line whose 0th tierID is timeAlignedTierID
           # these relationships are figured out above in
           # depthFirstTierTraversal, and used to assemble tiered lines
           # pandas data table extracted from the eaf xml
      found = False
      line = 0
      while not found:
         parent = list(self.getLineTable(line)["tierID"])[0]
         if parent == timeAlignedTierID:
               #print("found parent tier %s at line %d" % (tier, line))
            found = True
         else:
            line += 1
      tierFamily = list(self.getLineTable(line)["tierID"])
      tierFamily.pop(0)  # remove the parent
      return tierFamily

   #----------------------------------------------------------------------------------
   def getSummary(self):

      x = {}
      x['lineCount'] = self.getLineCount()
      x['tierTable'] = self.getTierTable()
      x['audioURL'] = self.getAudioURL()
      x['videoURL'] = self.getVideoURL()
      x['audioMimeType'] = self.getAudioMimeType()
      x['videoMimeType'] = self.getVideoMimeType()
      tbl = self.getTierTable()
      timeAlignedTiers = self.getTimeAlignedTiers()
      x['timeAlignedTiers'] = timeAlignedTiers
      i = 1
      for tier in timeAlignedTiers:
         x["timeAlignedTierFamily.%d" % i] = self.getTimeAlignedTierChildren(tier)
         i += 1

      return(x)

   #----------------------------------------------------------------------------------
   def getYAMLHeader(self, title, narrator, textEntry):

      textOut = []
      textOut.append("title: %s" % title)
      textOut.append("narrator: %s" % narrator)
      textOut.append("textEntry: %s" % textEntry)
      textOut.append("mediaFile: %s" % self.mediaURL)
      textOut.append("mimeType: %s" % self.mediaMimeType)
      textOut.append("")

      return(textOut)
      
   #----------------------------------------------------------------------------------
   def toYAML(self, title, narrator, textEntry):

      textOut = []
      textOut = self.getYAMLHeader(title, narrator, textEntry)
      textOut.append("lines:")
      lineNumber = 1
      # pdb.set_trace()
      for tbl in self.getAllLinesTable():
         newLines = self.lineToYAML(tbl, lineNumber)
         #pdb.set_trace()
         textOut.extend(newLines)
         textOut.append("")
         lineNumber += 1
      return(textOut)
     
   #----------------------------------------------------------------------------------
   def writeYAML(self, textOut, outputFilename):

      # print("--- writing %d lines to %s" % (len(textOut), outputFilename))
      #pdb.set_trace()
      with open(outputFilename, 'w') as f:
         f.writelines(s + '\n' for s in textOut)

#----------------------------------------------------------------------------------
def extractAllTimeAlignedTierIDs(xmlFilename):

   doc = etree.parse(xmlFilename)

   tierDescriptors = doc.findall("LINGUISTIC_TYPE")
   timeAlignedTierIDs = []

   for tierType in tierDescriptors:
      refID = tierType.attrib['LINGUISTIC_TYPE_ID']
      if 'TIME_ALIGNABLE' in tierType.attrib.keys():
         value = tierType.attrib['TIME_ALIGNABLE']
         if value == "true":
               # find all the text's tiers with this linguistic type
            tiers = doc.findall("TIER[@LINGUISTIC_TYPE_REF='%s']" % refID)
            for tier in tiers:
              id = tier.attrib['TIER_ID']
              timeAlignedTierIDs.append(id)

   #pdb.set_trace()
   return(timeAlignedTierIDs)

#----------------------------------------------------------------------------------
def xmlValid(xmlFilename):

   schemaFile = "http://www.mpi.nl/tools/elan/EAFv3.0.xsd" 
   valid = False
   xmlschema.validate(xmlFilename, schemaFile)

#----------------------------------------------------------------------------------
