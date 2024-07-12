BASEDIR = ~/github/slexil2
default:
	@echo venv
	@echo yaml2html

venv:
	@echo source /Users/paul/github/slexil2/py3105slexil/bin/activate

yaml2html:
	python $(BASEDIR)/utils/yaml2html.py \
        --yaml $(BASEDIR)/testData/validYamlFiles/inferno.yaml \
        --tierGuide $(BASEDIR)/testData/validYamlFiles/infernoTierGuide.yaml \
        --terms $(BASEDIR)/testData/validYamlFiles/infernoTerms.txt \
        --kbFilename $(BASEDIR)/testData/validYamlFiles/inferno-kb.js \
        --fontSizeControls
	open fromYaml.html
