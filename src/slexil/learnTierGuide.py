# -*- tab-width: 3 -*-
#-------------------------------------------------------------------------------
from slexil.eafParser import EafParser
from lxml import etree
import pandas as pd
import pdb
#-------------------------------------------------------------------------------
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
class LearnTierGuide:

   xmlFilename = ''
   parser = None
   doc = None
   tierTable = None

   #------------------------------------------------------------
   def __init__(self, xmlFilename, verbose=False):

      self.xmlFilename = xmlFilename
      self.parser = EafParser(xmlFilename, verbose=verbose)
      self.verbose = verbose

   #------------------------------------------------------------
   def constructTierTable(self):

      self.parser.constructTierTable()

   #------------------------------------------------------------
   def getTierTable(self):

       return self.parser.getTierTable()
   
   #------------------------------------------------------------
   def getTimeAlignedTiers(self):

      return(self.parser.getTimeAlignedTiers())

   #------------------------------------------------------------
   # todo: at present this ignores timeAlignedTierID parent
   # todo: must be fixed when plural time-aligned tiers are supported
   def getTimeAlignedTierChildren(self, timeAlignedTierID):

      tbl = self.getTierTable()
      allChildren = tbl[tbl["PARENT_REF"].notnull()]['TIER_ID'].tolist()
      return allChildren
      
   #------------------------------------------------------------
   def getTokenizedTierPairs(self, parentTier):
      tbl = self.getTierTable()
      self.parser.run()
      lines = self.parser.getAllLinesTable()
      lines = [line for line in lines if line["tierID"][0] == parentTier]
      # tbl2 = tbl[tbl["PARENT_REF"] == parentTier]
      candidateTiers = tbl[tbl["PARENT_REF"].notnull()]['TIER_ID'].tolist()
      tabCounts = {k: 0 for k in candidateTiers}
      pd.set_option('display.max_colwidth', None)
      for line in lines:
         for tier in candidateTiers:
            text = str(line[line["tierID"] == tier]["text"])
            tabCount = text.count("\\t")
            #print("  tabCount this line %d" % tabCount)
            tabCounts[tier] += tabCount
            
      numericCounts = [value for key, value in tabCounts.items()]

        # in nataliaCaceres 085_TheMotherOfTheFishAndThePrankster.eaf
        # the second speaker says little, mostly monosyllables,
        # not needing tab delimiters
        # so we now need just one tab across two tiers in the speakers lines
        # in order to judge those tiers to be a tokenized pair
        #-----------------------------------------------------------

      possiblePairs = {k:tabCounts[k] for k,v in tabCounts.items() if v > 0}
      return possiblePairs

   def oldGetTokenizedTierPairs(self):
      tbl = self.tierTable
      lines = self.linesAll
      candidateTiers = list(tbl[tbl["TIME_ALIGNABLE"] == "false"]["TIER_ID"])
      tabCounts = {k: 0 for k in candidateTiers}
      pd.set_option('display.max_colwidth', None)
      for line in lines:
         for tier in candidateTiers:
            text = str(line[line["tierID"] == tier]["text"])
            tabCount = text.count("\\t")
            tabCounts[tier] += tabCount
            
      numericCounts = [value for key, value in tabCounts.items()]
        #-----------------------------------------------------------
        # a conservative guess: we should find at least 3 delimited
        # tokens per line
        #-----------------------------------------------------------

      highCount = len(lines) * 3
        # allow for a few mistaken pairings
      possiblePairs = {k:tabCounts[k] for k,v in tabCounts.items() if v > highCount}
      return possiblePairs


   #--------------------------------------------------------------------------------
   def learnTierGuide(self):

     officialTierNames = ['speech', 'morpheme', 'morphemeGloss', 'translation']

     timeAlignedTier = self.getTimeAlignedTiers()[0]
     x = {}

     x["speech"] = timeAlignedTier
     
     tierKids = self.getTimeAlignedTierChildren(timeAlignedTier)
     pairedTokenTiers = self.getTokenizedTierPairs(timeAlignedTier)
     if(len(pairedTokenTiers) == 2):
        newMorpheme  = list(pairedTokenTiers.keys())[0]
        newMorphemeGloss = list(pairedTokenTiers.keys())[1]
        x["morpheme"] = newMorpheme
        x["morphemeGloss"] = newMorphemeGloss

     claimedTiers = [v for k,v in x.items()]
     remainingTiers = [x for x in tierKids if x not in claimedTiers]

     assert(len(remainingTiers) >= 1)
     x["translation"] = remainingTiers[0]
     return x
      
   #----------------------------------------------------------------------------------
