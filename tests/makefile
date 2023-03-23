default:
	@echo targets: venv, morphemeGloss, ijalLine, text, textDisplay
	@echo targets: audioExtractor, displayInferno clean

venv:
	@echo be sure to run: source /Users/paul/github/slexil2/py3105/bin/activate

all: morphemeGloss ijalLine fullText


eafParser:
	python test_EAFParser.py

morphemeGloss:
	python test_MorphemeGloss.py

ijalLine:
	python test_IjalLine.py

audioExtractor:
	python test_AudioExtractor.py

text: 
	python test_Text.py

textDisplay:
	python test_Text.py display



clean:
	- rm tmp*.html
