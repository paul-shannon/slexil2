import sys
import pathlib
import pdb
from xml.etree import ElementTree as etree

if (len(sys.argv) != 2):
   print("usage:  python segmentSeparation.py <filename>")
   sys.exit(1)
   
if (not pathlib.Path(sys.argv[1]).suffix == ".eaf"):
   print("usage: no eaf suffix in file %s" % sys.argv[1])
   sys.exit(1)
        
        
pdb.set_trace()

# eafFile = 

print("--- test_inferno")

eafFile = sys.argv[1]
xmlDoc = etree.parse(eafFile)
root = xmlDoc.getroot()
alignedTiers = root.findall("TIER/ANNOTATION/ALIGNABLE_ANNOTATION")
lineCount = len(alignedTiers)
tmpTbl = ijalLine.buildTable(xmlDoc, alignedTiers)
tierGuideFile = os.path.join(dataDir, "tierGuide.yaml")
with open(tierGuideFile, 'r') as f:
	tierGuide = yaml.safe_load(f)
grammaticalTerms = ["hab", "past"]
for i in range(lineCount):
	newLine = ijalLine.IjalLine(xmlDoc, i, tierGuide, grammaticalTerms)
	newLine.parse()
	print(newLine.getSpokenText())
	print("   %s" % newLine.getTranslation())
	startTime = newLine.getStartTime()
	endTime = newLine.getEndTime()
	print("   %d - %d" % (startTime, endTime))
	assert(endTime - startTime > 1000)


