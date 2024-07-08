# -*- tab-width: 3 -*-
import os, pdb
import yaml

class TierGuide:

  filename = None
  tg = None
  officialTierNames = ['speech', 'morpheme', 'morphemeGloss', 'translation',
                         'translation2', 'soundsLike']

  def __init__(self, filename):
     self.filename = filename
     with open(filename, 'r') as f:
         self.tg = yaml.safe_load(f)
     for key in self.tg.keys():
        valueList = self.tg[key].split(",")
        if(len(valueList)) > 1:
           self.tg[key] =  [x.strip() for x in valueList]

  def getGuide(self):
     return self.tg

  def getTierNames(self):
     return(list(self.tg.keys()))

  def getTierValues(self):
     return(list(self.tg.values()))

  def valid(self):
     invalidTierNames = []
     for usersTierName in self.getTierNames():
         if not usersTierName in self.officialTierNames:
             invalidTierNames.append(usersTierName)
     valid = len(invalidTierNames) == 0
       # at least one tier - speech - must be present
     valid = valid and "speech" in self.getTierNames()
     return {"valid": valid, "invalidNames": invalidTierNames}
      
 
     
       
