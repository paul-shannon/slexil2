NAME = howDaylightWasStolen
BASEDIR=~/github/slexil2

default:
	@echo targets:
	@echo  venv eaf http refresh-js html
	@echo  install
	@echo  curl
	@echo  eaf
	@echo  html
#	@echo  y2h    # yaml2html
	@echo  s2h    # yaml2html
	@echo  publish
	@echo  publish-audio
	@echo  viewRemote

venv:
	@echo source /Users/paul/github/slexil2/py3105slexil/bin/activate

PORT = 8009

curl:
	curl -I https://slexildata.artsrn.ualberta.ca/lushootseed/harryMoses/daylight/daylight-restoration_V03-22k-aLaw.wav

http:
	python -m http.server $(PORT) &

#y2h:
#	python $(BASEDIR)/utils/yaml2html.py \
#        --yaml daylight.yaml \
#        --tierGuide tierGuide.yaml \
#        --kbFilename kb.js \
#        --linguistics linguisticTerms.js \

s2h:
	python $(BASEDIR)/utils/sfmt2html.py \
        --sfmt daylight.yaml \
        --tierGuide tierGuide.yaml \
        --kbFilename kb.js \
        --pageTitle "Harry Moses - How Daylight Was Stolen" \
        --helpButtonLabel About \
        --helpFile about.html \
        --linguistics linguisticTerms.js


install:
	(cd ../../../..; make install)

bug:
	python ~/github/yamlToEAF/toEAF.py tiny.yaml

eaf:
	python ~/github/yamlToEAF/toEAF.py $(NAME).yaml


html:
	python ../../../../utils/eaf2html.py  --eaf $(NAME).eaf \
                       --tierGuide tierGuide.yaml \
                       --terms grammaticalTerms.txt \
                       --pageTitle "Harry Moses - How Daylight Was Stolen" \
                       --fontSizeControls \
                       --kbFilename kb.js \
                       --linguistics linguisticTerms.js \
                       --helpFile about.html \
                       --helpButtonLabel About \
                       --verbose \
                       --practiceFile practice.yaml 
#                       --webpackLinksOnly




tailor:
	sed -f insertCustomCode.sed index.html  > index0.html

refresh-js:
	cp -p ../../*.js .
	cp -p ../../slexil.css .



publish:
	scp daylight.html pshannon@206.12.95.4:www/lushootseed/harryMoses/daylight/index.html
	scp kb.js pshannon@206.12.95.4:www/lushootseed/harryMoses/daylight/
	scp linguisticTerms.js pshannon@206.12.95.4:www/lushootseed/harryMoses/daylight/

publish-audio:
	scp daylight-restoration_V03-22k-aLaw.wav pshannon@206.12.95.4:www/lushootseed/harryMoses/daylight/


view:
	open daylight.html

viewRemote:
	open https://slexildata.artsrn.ualberta.ca/lushootseed/harryMoses/daylight/

