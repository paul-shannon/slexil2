default:
	@echo targets: venv, morphemeGloss, ijalLine, fullText, 
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

fullText: 
	python test_Text.py

displayInferno:
	python test_Text.py display


# for now, local pshannon use only (14 nov 2021)
extractAudio:
	python ~/github/yamlToEAF/extractAudioPhrases.py \
                               ../testData/inferno/inferno-threeLines.wav \
                               ../testData/inferno/inferno-threeLines.eaf \
                               audio
	cp ../testData/inferno/inferno-threeLines.wav audio/


clean:
	- rm tmp*.html
