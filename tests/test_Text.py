import re
import sys, os

#from slexil.ijalLine import IjalLine
#from slexil.eafParser import EafParser
from slexil.text import Text

import pdb
import yaml
import yattag
import pandas as pd

pd.set_option('display.width', 1000)
pd.set_option('display.max_columns', None)
#--------------------------------------------------------------------------------
def runTests():

	test_inferno_speechOnly()
	test_inferno_speechAndTranslation()
	test_inferno_speechTranslationMorphemes()
	test_inferno_speechTranslationMorphemesAndGloss()

#--------------------------------------------------------------------------------
def test_inferno_speechOnly():

	print("--- text_inferno_speechOnly")

	tierGuide = {"speech": "italianSpeech"}
	with open("tmp.yaml", "w") as outfile:
		yaml.dump(tierGuide, outfile)
	packageRoot = os.path.dirname(os.path.dirname(os.path.abspath("explore_text-inferno.py")))
	dataDir = os.path.join(packageRoot, "testData", "inferno")
	projectDir = os.path.join(packageRoot, "tests", "tmp")

	elanXmlFilename =      os.path.join(dataDir, "inferno-threeLines.eaf")
	projectDirectory =     projectDir
	tierGuideFile =        "tmp.yaml"
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
		    verbose=False,
		    fontSizeControls = fontSizeControls,
		    startLine = startLine,
		    endLine = endLine,
		    kbFilename = kbFilename,
		    linguisticsFilename = linguisticsFilename,
                    pageTitle = "inferno",
		    helpFilename = None,
		    helpButtonLabel = None,
                    fixOverlappingTimeSegments=True)

	# print(text.getTierSummary())
	htmlText = text.toHTML()
	htmlText_indented = yattag.indent(htmlText)

	   # 3 lines of speech, one jquery pattern
	pattern = re.compile('speech-tier"')
	assert(len(pattern.findall(htmlText)) == 4)

	   # should be no other tiers
	pattern = re.compile('-tier">')
	assert(len(pattern.findall(htmlText)) == 3)
	
	filename = "speechOnly-index.html"
	f = open(filename, "wb")
	f.write(bytes(htmlText_indented, "utf-8"))
	f.close()
	print("    wrote %s" % f.name)

#--------------------------------------------------------------------------------
def test_inferno_speechAndTranslation():

	print("--- text_inferno_speechAndTranslation")

	tierGuide = {"speech": "italianSpeech",
	             "translation": "english"}
	with open("tmp.yaml", "w") as outfile:
		yaml.dump(tierGuide, outfile)
	packageRoot = os.path.dirname(os.path.dirname(os.path.abspath("explore_text-inferno.py")))
	dataDir = os.path.join(packageRoot, "testData", "inferno")
	projectDir = os.path.join(packageRoot, "tests", "tmp")

	elanXmlFilename =      os.path.join(dataDir, "inferno-threeLines.eaf")
	projectDirectory =     projectDir
	tierGuideFile =        "tmp.yaml"
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
		    verbose=False,
		    fontSizeControls = fontSizeControls,
		    startLine = startLine,
		    endLine = endLine,
		    kbFilename = kbFilename,
		    linguisticsFilename = linguisticsFilename,
                    pageTitle = "inferno",
		    helpFilename = None,
		    helpButtonLabel = None,
                    fixOverlappingTimeSegments=True)

	# print(text.getTierSummary())
	htmlText = text.toHTML()
	htmlText_indented = yattag.indent(htmlText)

	   # 3 speech tiers
	pattern = re.compile('speech-tier">')
	assert(len(pattern.findall(htmlText)) == 3)

	   # 3 translation tiers
	pattern = re.compile('freeTranslation-tier">')
	assert(len(pattern.findall(htmlText)) == 3)
	
	   # should be no other tiers
	pattern = re.compile('-tier">')
	assert(len(pattern.findall(htmlText)) == 6)

	filename = "speechAndTranslation.html"
	f = open(filename, "wb")
	f.write(bytes(htmlText_indented, "utf-8"))
	f.close()
	print("    wrote %s" % f.name)

#--------------------------------------------------------------------------------
def test_inferno_speechTranslationMorphemes():

	print("--- text_inferno_speechTranslationMorphemes")

	tierGuide = {"speech": "italianSpeech",
	             "translation": "english",
	             "morpheme": "morphemes"}
	
	with open("tmp.yaml", "w") as outfile:
		yaml.dump(tierGuide, outfile)
	packageRoot = os.path.dirname(os.path.dirname(os.path.abspath("explore_text-inferno.py")))
	dataDir = os.path.join(packageRoot, "testData", "inferno")
	projectDir = os.path.join(packageRoot, "tests", "tmp")

	elanXmlFilename =      os.path.join(dataDir, "inferno-threeLines.eaf")
	projectDirectory =     projectDir
	tierGuideFile =        "tmp.yaml"
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
		    verbose=False,
		    fontSizeControls = fontSizeControls,
		    startLine = startLine,
                    pageTitle = "inferno",
		    helpFilename = None,
		    helpButtonLabel = None,
		    endLine = endLine,
		    kbFilename = kbFilename,
		    linguisticsFilename = linguisticsFilename,
                    fixOverlappingTimeSegments=True)

	# print(text.getTierSummary())
	htmlText = text.toHTML()
	htmlText_indented = yattag.indent(htmlText)

	   # 3 speech tiers, but avoid two ".speech-tier" strings
	pattern = re.compile('"speech-tier"')
	assert(len(pattern.findall(htmlText)) == 3)

	   # 3 translation tiers
	pattern = re.compile('"freeTranslation-tier"')
	assert(len(pattern.findall(htmlText)) == 3)
	
	   # 3 translation tiers
	pattern = re.compile('"morpheme-tier"')
	assert(len(pattern.findall(htmlText)) == 3)
	
	filename = "speechTranslationMorphemes.html"
	f = open(filename, "wb")
	f.write(bytes(htmlText_indented, "utf-8"))
	f.close()
	print("    wrote %s" % f.name)

#--------------------------------------------------------------------------------
def test_inferno_speechTranslationMorphemesAndGloss():

	print("--- text_inferno_speechTranslationMorphemesAndGloss")

	tierGuide = {"speech": "italianSpeech",
	             "translation": "english",
	             "morpheme": "morphemes",
				 "morphemeGloss": "morpheme-gloss"}
	
	with open("tmp.yaml", "w") as outfile:
		yaml.dump(tierGuide, outfile)
	packageRoot = os.path.dirname(os.path.dirname(os.path.abspath("explore_text-inferno.py")))
	dataDir = os.path.join(packageRoot, "testData", "inferno")
	projectDir = os.path.join(packageRoot, "tests", "tmp")

	elanXmlFilename =      os.path.join(dataDir, "inferno-threeLines.eaf")
	projectDirectory =     projectDir
	tierGuideFile =        "tmp.yaml"
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
		    verbose=False,
		    fontSizeControls = fontSizeControls,
		    startLine = startLine,
		    endLine = endLine,
		    kbFilename = kbFilename,
		    linguisticsFilename = linguisticsFilename,
                    pageTitle = "inferno",
		    helpFilename = None,
		    helpButtonLabel = None,
                    fixOverlappingTimeSegments=True)

	# print(text.getTierSummary())
	htmlText = text.toHTML()
	htmlText_indented = yattag.indent(htmlText)

	   # 3 speech tiers
	pattern = re.compile('"speech-tier">')
	assert(len(pattern.findall(htmlText)) == 3)

	   # 3 translation tiers
	pattern = re.compile('"freeTranslation-tier"')
	assert(len(pattern.findall(htmlText)) == 3)
	
	   # 3 morpheme tiers, 3 morphemeGloss tiers
	pattern = re.compile('"morpheme-tier"')
	assert(len(pattern.findall(htmlText)) == 6)
	
	filename = "speechTranslationMorphemesAndGloss.html"
	f = open(filename, "wb")
	f.write(bytes(htmlText_indented, "utf-8"))
	f.close()
	print("    wrote %s" % f.name)

#--------------------------------------------------------------------------------
if __name__ == '__main__':
    runTests()
