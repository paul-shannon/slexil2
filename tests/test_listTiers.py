import os
import slexil
from xml.etree import ElementTree as etree

packageRoot = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dataDir = os.path.join(packageRoot, "testData")
eafFile = os.path.join(dataDir, "inferno", "inferno-threeLines.eaf")
tierGuideFile = os.path.join(dataDir, "inferno", "tierGuide.yaml")

#--------------------------------------------------------------------------------
def test_tierCount():

   print("--- running test_listTiers.py, test_tierCount")

   tree = etree.parse(eafFile)
   root = tree.getroot()
   root.tag
   root.attrib
   tierElements = root.findall("TIER")
   assert(len(tierElements) == 4)

#--------------------------------------------------------------------------------
def runTests():

   test_tierCount()

#--------------------------------------------------------------------------------
if __name__ == '__main__':
   runTests()
