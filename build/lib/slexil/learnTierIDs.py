
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

import sys
import os
from xml.etree import ElementTree as etree

if(len(sys.argv) != 2):
   print("usage:  python learnTierIDs.py <fullPath to eaf xml file>")
   sys.exit()

xmlFilename = sys.argv[1]

fileFound = os.path.isfile(xmlFilename)

if(not fileFound):
    print("error.  could not read eaf xml file'%s'" % xmlFilename)
    sys.exit()

#xmlFilename = "../testData/HMDLsafe/HMDL.eaf"
tmpDoc = etree.parse(xmlFilename)
tierIDs = [tier.attrib["TIER_ID"] for tier in tmpDoc.findall("TIER")]
tiers = tmpDoc.findall("TIER")

for tier in tiers:
   tierID = tier.attrib["TIER_ID"]
   count = len(tier.findall("ANNOTATION"))
   print(" %30s: %4d" % (tierID, count))
   
   
