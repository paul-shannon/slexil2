default:
	@echo venv
	@echo all
	@echo install
	@echo webPacker
	@echo tierGuide
	@echo eaf
	@echo learnTierGuide
	@echo ijalLine
	@echo text
	@echo morphemeGloss
	@echo listTiers
	@echo standardizeIjalTierTable
	@echo xmlFileUtils
	@echo ijalFromDict
	@echo yamlParser
	@echo textFromYaml

yamlTextCreator:

venv:
	@echo source /Users/paul/github/slexil2/py3105slexil/bin/activate


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
     yamlParser \
     textFromYaml

webPacker:
	python -m unittest test_webPacker.py 

tierGuide:
	python test_tierGuide.py

eaf:
	python test_eafParser.py
	python test_eafParserInferno.py

learnTierGuide:
	python test_learnTierGuide.py

ijalLine:
	python test_IjalLine.py

text:
	python test_Text.py

morphemeGloss:

	python -m unittest test_MorphemeGloss.py

listTiers:
	python -m unittest test_listTiers.py

#	python -m unittest test_infernoDemo.py
#	python -m unittest test_infernoDemo_toHTML.py

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

yaml:  yamlParser  textFromYaml

yamlParser:
	python test_yamlParser.py

textFromYaml:
	python test_TextFromYaml.py

ijalFromDict:
	python test_IjalLineFromDict.py

