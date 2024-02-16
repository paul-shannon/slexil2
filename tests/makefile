default:
	@echo targets: venv all install
	@echo webPacker
	@echo tierGuide
	@echo eafParser
	@echo ijalLine
	@echo text
	@echo morphemeGloss
	@echo listTiers
	@echo tierNamingBug
	@echo standardizeIjalTierTable

venv:
	@echo source /Users/paul/github/slexil2/py3105slexil/bin/activate

dev:
	python -m unittest test_eafParser.py

all: webPacker eafParser ijalLine text morphemeGloss standardizeIjalTierTable

webPacker:
	python -m unittest test_webPacker.py 

tierGuide:
	python test_tierGuide.py

eafParser:
	python test_eafParser.py

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
