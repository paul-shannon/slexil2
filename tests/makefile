default:
	@echo venv
	@echo all
	@echo exceptions
	@echo install
	@echo webPacker
#	@echo tierGuide
	@echo oldEaf
	@echo eaf
#	@echo learnTierGuide
	@echo ijalLine
	@echo text
	@echo morphemeGloss
	@echo listTiers
	@echo standardizeIjalTierTable
	@echo xmlFileUtils
	@echo ijalFromDict
	@echo inferTiers
	@echo inferTiersSFMT
#	@echo yamlParser
	@echo newYamlParser
	@echo grammaticalTermFormatter
#	@echo textFromYaml
	@echo yamlFromEAF
	@echo tieredLine
	@echo practiceLists
	@echo eafyaml
	@echo morphemeGlossAbbreviations  [mga]

practiceLists:
	python test_PracticeLists.py 

yamlTextCreator:

venv:
	@echo source /Users/paul/github/slexil2/py3119slexil/bin/activate


all: install \
     webPacker \
     tierGuide \
     eaf \
     learnTierGuide \
     ijalLine \
     text \
     morphemeGloss \
     listTiers \
     standardizeIjalTierTable \
     xmlFileUtils \
     ijalFromDict \
     sfmt \
     sfmtToWebPage

webPacker:
	python test_webPacker.py 

tierGuide:
	python test_tierGuide.py

oldEaf:
	python test_eafParser.py
	python test_eafParserInferno.py

eaf:
	python test_eafParser.py

learnTierGuide:
	python test_learnTierGuide.py

ijalLine:
	python test_IjalLine.py

text:
	python test_Text.py

morphemeGloss:
	python test_MorphemeGloss.py

listTiers:
	python test_listTiers.py

install:
	(cd ..; make install)

pipgit:
	(cd ..; make gitpip)

check:
	(cd ..; make check)

infernoDemo:
	python demoInferno.py
	open inferno.html

# BUG.eaf = ../testData/validButBreaksSlexil-small.eaf
EAF = ../testData/inferno/inferno-threeLines.eaf
TG = ../testData/inferno/tierGuide.yaml

tierNamingBug:
	python ../utils/validXML.py ../testData/EAFv3.0.xsd $(EAF)
	python ../utils/eaf2html.py --eaf $(EAF) --tierGuide $(TG) --pageTitle bug

standardizeIjalTierTable:
	python test_standardizeIjalTierTable.py

xmlFileUtils:
	python test_XmlFileUtils.py

yaml:  newYamlParser  textFromYaml


#yamlParser:
#	python test_yamlParser.py

newYamlParser:
	python test_NewYamlParser.py

yamlFromEAF:
	python test_yamlFromEAF.py

#textFromYaml:
#	python test_TextFromYaml.py

ijalFromDict:
	python test_IjalLineFromDict.py

inferTiersSFMT:
	python test_inferTierStructureFromSFMT.py

sfmtToWebPage:
	python test_sfmtToWebPage.py

inferTiers:
	python test_inferTierStructure.py

tieredLine:
	python test_TieredLine.py

yamlToTextApp:
	python test_yamlToTextApp.py

eafyaml:
	python test_eafParser-toYAML.py

grammaticalTermFormatter:
	python test_grammaticalTermFormatter.py

mga: morphemeGlossAbbreviations

morphemeGlossAbbreviations:
	python test_morphemeGlossAbbreviations.py

exceptions:
	python test_exceptions.py

sfmt:
	python test_SFMT.py

sfmtToText:
	python test_sfmtToText.py


crucial: exceptions \
         sfmt \
         tieredLine \
         eaf \
         morphemeGlossAbbreviations \
		   sfmtToWebPage
