import os
import unittest
from slexil.text import Text
from yattag import indent

#----------------------------------------------------------------------------------------------------
packageRoot = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dataDir = os.path.join(packageRoot, "data", "infernoDemo")
projectDir = os.path.join(packageRoot, "tests", "tmp")
#----------------------------------------------------------------------------------------------------
def createText():
	elanXmlFilename =      os.path.join(dataDir, "inferno-threeLines.eaf")
	projectDirectory =     projectDir
	tierGuideFile =        os.path.join(dataDir, "tierGuide.yaml")
	grammaticalTermsFile = os.path.join(dataDir, "grammaticalTerms.txt")
	fontSizeControls = False
	startLine = None
	endLine = None
	kbFilename = None
	linguisticsFilename = None

	text = Text(elanXmlFilename,
				grammaticalTermsFile=grammaticalTermsFile,
				tierGuideFile=tierGuideFile,
				projectDirectory=projectDirectory,
				verbose=True,
				fontSizeControls = fontSizeControls,
				startLine = startLine,
				endLine = endLine,
				kbFilename = kbFilename,
				linguisticsFilename = linguisticsFilename)
	
	return(text)

#-------------------------------------------------------------------------------------
class TestInfernoDemo_toHTML(unittest.TestCase):

	def test_constructor(self):
		print("--- test_constructor")
		text = createText()
		assert(text.validInputs())
		tbl = text.getTierSummary()
		assert(tbl.shape == (6,3))
		assert(list(tbl['key']) == ['morpheme', 'morphemeGloss', 'morphemePacking', 'speech', 'transcription2', 'translation'])
		assert(list(tbl['value']) == ['morphemes', 'morphemeGloss', 'lines', 'italianSpeech', '', 'english'])
		assert(list(tbl['count']) == [3, 3, 3, 3, 0, 0])

	def test_toHTML(self):
		print("--- test_toHTML")
		text = createText()
		text.getLineAsTable(1)
		htmlText = text.toHTML()
		filename = "inferno.html"
		f = open(filename, "w")
		f.write(indent(htmlText))
		f.close()
