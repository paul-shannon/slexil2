NAME = howDaylightWasStolen


default:
	@echo targets:
	@echo  venv eaf http refresh-js html
	@echo  eaf
	@echo  html
	@echo  view
	@echo  publish
	@echo  viewRemote

venv:
	@echo source /Users/paul/github/slexil2/py3105slexil/bin/activate

PORT = 8009

http:
	python -m http.server $(PORT) &

eaf:
	python ~/github/yamlToEAF/toEAF.py $(NAME).yaml

html.old: 
	python ~/github/slexil2/utils/eaf2html.py \
               --eaf $(NAME).eaf \
               --terms grammaticalTerms.txt \
               --tierGuide tierGuide.yaml \
               --projectDirectory ./ \
               --fontSizeControls \
               --kbFilename kb.js \
               --linguistics linguisticTerms.js \
               --helpFilename help.html \
               --helpButtonLabel  About \
               --pageTitle Daylight \
               --verbose \
               --startLine None \
               --endLine None \
               -webpackLinksOnly False
	            fixOverlappingTimeSegments=True)


html:
	python ../../../../utils/eaf2html.py  --eaf $(NAME).eaf \
                       --tierGuide tierGuide.yaml \
                       --terms grammaticalTerms.txt \
                       --pageTitle "Harry Moses - How Daylight Was Stolen" \
                       --fontSizeControls \
                       --kbFilename kb.js \
                       --linguistics linguistics.js \
                       --helpFile about.html \
                       --helpButtonLabel About \
                       --webpackLinksOnly



tailor:
	sed -f insertCustomCode.sed index.html  > index0.html

refresh-js:
	cp -p ../../*.js .
	cp -p ../../slexil.css .



publish:
	scp index.html pshannon@206.12.95.4:www/lushootseed/harryMoses/daylight/
	scp kb.js pshannon@206.12.95.4:www/lushootseed/harryMoses/daylight/
	scp linguisticTerms.js pshannon@206.12.95.4:www/lushootseed/harryMoses/daylight/

view:
	open index.html

