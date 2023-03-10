default:
	@echo targets: all, morphemeGloss, ijalLine, fullText, extractAudio, displayInferno clean

all: morphemeGloss ijalLine fullText


morphemeGloss:
	python3 test_MorphemeGloss.py

ijalLine:
	python3 test_IjalLine.py

audioExtractor:
	python3 test_AudioExtractor.py
	python3 test_startStopTable.py
	python3 test_Audio_formats.py
	python3 test_startStopTable.py

fullText: 
	python3 test_Text.py

displayInferno:
	python3 test_Text.py display


# for now, local pshannon use only (14 nov 2021)
extractAudio:
	python3 ~/github/yamlToEAF/extractAudioPhrases.py \
                               ../testData/inferno/inferno-threeLines.wav \
                               ../testData/inferno/inferno-threeLines.eaf \
                               audio
	cp ../testData/inferno/inferno-threeLines.wav audio/


clean:
	- rm tmp*.html
