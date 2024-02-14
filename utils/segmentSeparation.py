from xml.etree import ElementTree as etree

eafFile = 
class TestInfernoStructure(unittest.TestCase):

	def test_inferno(self):
		print("--- test_inferno")

		eafFile = os.path.join(dataDir, "inferno-threeLines.eaf")
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


