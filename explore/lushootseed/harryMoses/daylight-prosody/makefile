
NAME = howDaylightWasStolen
BASEDIR=~/github/slexil2

PORT = 8765

default:
	@echo targets:
	@echo venv
	@echo server
	@echo pid
	@echo  venv eaf http refresh-js html
	@echo  install
	@echo  curl
	@echo  eaf
	@echo  html
	@echo  s2h    # yaml2html
	@echo  inject 
	@echo  view
	@echo  view-pshannon
	@echo  updateLocal [s2h, inject]
	@echo  update [s2h, inject, publish-alberta, viewRemote]
	@echo  publish-alberta
	@echo  publish-audio
	@echo  publish-pshannon
	@echo  viewRemote

venv:
	@echo source /Users/paul/github/slexil2/py3119slexil/bin/activate

server:
	python -m http.server $(PORT) &

pid:
	lsof -i -n -P | grep $(PORT)


curl:
	curl -I https://slexildata.artsrn.ualberta.ca/lushootseed/harryMoses/daylight/daylight-restoration_V03-22k-aLaw.wav


#y2h:
#	python $(BASEDIR)/utils/yaml2html.py \
#        --yaml daylight.yaml \
#        --tierGuide tierGuide.yaml \
#        --kbFilename kb.js \
#        --linguistics linguisticTerms.js \

s2h:
	python $(BASEDIR)/utils/sfmt2html.py \
        --sfmt daylight.yaml \
        --htmlFile daylight.html \
        --kbFilename kb.js \
        --pageTitle "Harry Moses - How Daylight Was Stolen" \
        --helpButtonLabel About \
        --helpFile aboutNew.html \
        --provideRecording \
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




inject:
	sed -f insertCustomCode.sed daylight.html  > daylight2.html

refresh-js:
	cp -p ../../*.js .
	cp -p ../../slexil.css .

DEST2=pshannon@134.87.10.153:www/lushootseed/harryMoses/daylight/

publish-alberta:
	rsync -a daylight2.html $(DEST2)/index.html
	rsync -a kb.js $(DEST2)
	rsync -a linguisticTerms.js $(DEST2)
	rsync -a docs/taxonomy.html $(DEST2)docs/
	rsync -a *.jpeg $(DEST2)

publish-audio:
	scp daylight-24k.wav pshannon@134.87.10.153:www/lushootseed/harryMoses/daylight/
#	scp daylight-restoration_V03-22k-aLaw.wav pshannon@134.87.10.153:www/lushootseed/harryMoses/daylight/

DEST=paulshannnon@pshannon.net:public_html/pshannon.net/daylight
publish-pshannon:
	rsync -a daylight2.html $(DEST)/index.html
	rsync -a kb.js $(DEST)
	rsync -a linguisticTerms.js $(DEST)
	rsync -a daylight-restoration_V03-22k-aLaw.wav $(DEST)
	rsync -a docs/taxonomy.html paulshannnon@pshannon.net:public_html/pshannon.net/docs/
	rsync -a *.jpeg $(DEST)

updateLocal: s2h inject 

update: s2h inject publish-alberta viewRemote


view:
	open http://localhost:$(PORT)/daylight2.html

viewRemote:
	open https://slexildata.artsrn.ualberta.ca/lushootseed/harryMoses/daylight/

view-pshannon:
	open https://pshannon.net/daylight

