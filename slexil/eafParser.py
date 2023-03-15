
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

# eafParser.py: a class to extract core information from ELAN XML files
#----------------------------------------------------------------------------------------------------
#import re
# import sys
import pandas as pd
from xml.etree import ElementTree as etree
import os
import pdb
import logging
#----------------------------------------------------------------------------------------------------
class EAFParser:
   elanXmlFilename = ''

   def __init__(self, elanXmlFilename):
       self.elanXmlFilename = elanXmlFilename

   def getFilename(self):
       return(self.elanXmlFilename)

   def extractStartAndEndTimes(self):
        # print("entering determine start and end times")
        xmlDoc = etree.parse(self.elanXmlFilename)
        timeSlotElements = xmlDoc.findall("TIME_ORDER/TIME_SLOT")
        timeIDs = [x.attrib["TIME_SLOT_ID"] for x in timeSlotElements]
        times = [int(x.attrib["TIME_VALUE"]) for x in timeSlotElements]
        audioTiers = xmlDoc.findall("TIER/ANNOTATION/ALIGNABLE_ANNOTATION")
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
        # still need to rename, maybe also reorder columns
        tbl.columns = ["lineID", "t1", "start", "t2", "end"]
        list(tbl.columns)
        tbl = tbl[["lineID", "start", "end", "t1", "t2"]]
        #        tbl = tbl.sort('start')
        self.startStopTable = self.makeStartStopTable(tbl)
        # print("+++\n",tbl,"\n+++")
        return (tbl)

   def makeStartStopTable(self, tbl):
        CSV = tbl.to_csv(index=False)
        phraseList = CSV.split('\n')
        if phraseList[-1] == '':
            del phraseList[-1]
        startStopByLine = []
        for i, phrase in enumerate(phraseList):
            parts = phrase.split(',')
            # print(parts)
            newParts = [str(i), parts[1], parts[2], parts[0]]
            line = ",".join(newParts)
            startStopByLine.append(line)
        startStopTable = '\n'.join(startStopByLine)
        return (startStopTable)

