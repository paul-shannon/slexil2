# every line in the text is transformed from ELAN xml to a pandas table.
# each row in the table corresponds to a tier in the xml.  Here we
# aassociate canonical IJAL tiers (e.g., speech, morpheme, morphemeGloss, translation)
# with each of the tiers in the xml, using the user-supplied tierGuide.
# for example: 	tierGuide = {'speech': 'italianSpeech',
#                            'transcription2': None,
#                            'morpheme': 'morphemes',
#                            'morphemeGloss': 'morpheme-gloss',
#                            'translation': 'english',
#                            'translation2': None}
# futhermore, since a speech tier is a mandatory minimum, we chack for that,
# return None if insufficient information is provided.

#-------------------------------------------------------------------------------
# -*- tab-width: 4 -*-
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
import os, sys
import pandas as pd
import numpy as np
pd.set_option('display.width', 1000)
import pdb

class StandardizeIjalTierTable:

   tbl = None
   tierGuide = None
   allUserTierNames = None
   userTiersAreMultiple = False   # i.e., speech may be in 2 tiers, for 2 speakers
   verbose = True
   ijalCanonicalTierNames = ('speech', 'morpheme', 'morphemeGloss',
                               'translation', 'translation2', 'soundsLike')

   def __init__(self, tbl, tierGuide, verbose):

      self.tierGuide = tierGuide
      self.verbose = verbose
      self.allUserTierNames = np.array(list(self.tierGuide.values())).flatten().tolist()
      if(len(self.allUserTierNames) > len(self.tierGuide.keys())):
         self.userTiersAreMultiple = True

         #------------------------------------------------------
         # trim tbl to include only tiers named in the tierGuide
         #------------------------------------------------------
      if(not "speech" in tierGuide.keys()):
         msg = "required 'speech' tier not found in the tierGuide"
         raise Exception(msg)

      #print()
      #print("--- standardizeIjalTierTable, all tierIDs:")
      #print(list(tbl['tierID']))
      #print()
         # extract the tier names.  flatten because some tiers may have two values
      self.tbl = tbl[tbl["tierID"].isin(self.allUserTierNames)]
      #pdb.set_trace()
      if(self.tbl.shape[0] == 0):
         msg = "none of the tbl tier names are in the tierGuide"
         raise Exception(msg)

      #---------------------------------------------------------------------------------
      # the tierGuide maps user's choice of tier names (e.g., "italianSpeech", "english"
      # to our IJAL canonical tier names ("speech", "translation")
      # self.tbl is a dataframe representation of the ELAN XML (eaf) data strucutre
      # in which the user's tier names are listed.
      # here we ensure that every one of the user's tierNames, from the eaf file, now
      # in self.tbl, is mapped in tierGuide to an IJAL canonical tier name
      #---------------------------------------------------------------------------------

   def guideAndLinesAgree(self):
         # italianSpeech, morphemes, morpheme-gloss, english
      eafTierNames = set(self.tbl["tierID"].tolist())
         # those names should be in the tierGuide as well
      
      guideTierNames = set(self.allUserTierNames)
      matchingTierNames = list(guideTierNames.intersection(eafTierNames))
      missingTierNames = list(guideTierNames.difference(eafTierNames))
      # todo:  speech tier must be present.  others are optionsl
      # todo:  check this here
      #if(missingTierNames != [None]):
      #   if(len(missingTierNames) == 1 and missingTierNames[0] == "translation"):
      #      msg = "error in IjalLine standardizeTable. tier name/s not found in tierGuide: "
      #      for unmatchedTierName in missingTierNames:
      #          msg += " %s" % unmatchedTierName
      #      print(self.tbl)
      #      raise Exception(msg)
         #-------------------------------------------------------
         # tierGuide keys should be IJAL canonical tier names.
         # not all IJAL tiers are required, but all tierGuide keys
         # must be in the IJAL canonical set
         #---------------------------------------------------
      tierGuideKeys = set(self.tierGuide.keys())
      illegalTierGuideKeys = list(tierGuideKeys.difference(set(self.ijalCanonicalTierNames)))
      #pdb.set_trace()
      if(len(illegalTierGuideKeys) > 0):
         msg = "error in IjalLine standardizeTable. tier name keys not IJAL canonicals: "
         for unmatchedTierName in illegalTierGuideKeys:
             msg += " %s" % unmatchedTierName
         raise Exception(msg)
      return(True)
  
      # the table comes with user tier names, associated via tierGuide.yaml
      # with cannonical names. look up the canonical names, add them in a column.
   def addCanonicalTierNameColumn(self):
      assert(self.guideAndLinesAgree())
      if(self.userTiersAreMultiple):
         canonicalNames = []
         userTiersThisLine = self.tbl["tierID"].tolist()
            # todo: accurate, but loopy!  3 loops...
         for userTierName in userTiersThisLine:
            for key in list(self.tierGuide.keys()):
                values = self.tierGuide[key]
                for value in values:
                   if(value == userTierName):
                      canonicalNames.append(key)
      else:
         tierGuideReversed = {v: k for k, v in self.tierGuide.items()}
         canonicalNames = [tierGuideReversed[key] for key in self.tbl["tierID"]]

         # some weird & fancy footwork to avoid "SettingWithCopyWarning"
      tbl = self.tbl.copy()
      tbl.loc[:, "canonicalTier"] = canonicalNames
      self.tbl = tbl

   def getTable(self):
      return(self.tbl)
      
