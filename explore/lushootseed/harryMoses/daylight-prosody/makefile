NAME = howDaylightWasStolen


default:
	@echo targets:
	@echo  venv eaf http refresh-js html
	@echo  curl
	@echo  eaf
	@echo  html
	@echo  view
	@echo  publish
	@echo  viewRemote

venv:
	@echo source /Users/paul/github/slexil2/py3105slexil/bin/activate

PORT = 8009

curl:
	curl -I https://slexildata.artsrn.ualberta.ca/lushootseed/harryMoses/daylight/daylight-restoration_V03-22k-aLaw.wav

http:
	python -m http.server $(PORT) &

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
                       --helpButtonLabel About 
#                       --verbose \
#                       --webpackLinksOnly



tailor:
	sed -f insertCustomCode.sed index.html  > index0.html

refresh-js:
	cp -p ../../*.js .
	cp -p ../../slexil.css .



publish:
	scp index.html pshannon@206.12.95.4:www/lushootseed/harryMoses/daylight/
	scp kb.js pshannon@206.12.95.4:www/lushootseed/harryMoses/daylight/
	scp linguisticTerms.js pshannon@206.12.95.4:www/lushootseed/harryMoses/daylight/
	scp daylight-restoration_V03-22k-aLaw.wav pshannon@206.12.95.4:www/lushootseed/harryMoses/daylight/


view:
	open index.html

viewRemote:
	open https://slexildata.artsrn.ualberta.ca/lushootseed/harryMoses/daylight/

