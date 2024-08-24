PROJECT = grammar
EAF = $(PROJECT).eaf
HTML.FILE = hessAndHilbert.html
BASEDIR=~/github/slexil2

default:
	@echo valid
	@echo venv
	@echo curl
	@echo yaml2html
	@echo eaf
	@echo html
	@echo css      # read local slexil.css, for experimentation
	@echo publish  # all
	@echo publish-text  # just html and kb.js
	@echo view
	@echo viewRemote

venv:
	@echo source /Users/paul/github/slexil2/py3105slexil/bin/activate

valid:
	python ~/github/slexil2/utils/validXML.py $(EAF) 2>&1 | more


yaml2html:
	python $(BASEDIR)/utils/yaml2html.py \
        --yaml grammar.yaml \
        --tierGuide tierGuide.yaml \
        --kbFilename kb.js \
        --pageTitle "Lushootseed Grammar" \
        --helpButtonLabel About \
        --helpFile about.html

eaf:
	python ~/github/yamlToEAF/toEAF.py  $(PROJECT).yaml 

html:
	python ../../../utils/eaf2html.py  --eaf $(EAF) \
                       --tierGuide tierGuide.yaml \
                       --pageTitle "Lushootseed Grammar" \
                       --helpFile about.html \
                       --helpButtonLabel About \
                       --kbFilename kb.js \
#                      --webpackLinksOnly \
                       --verbose
#                       --toolTips
#			   --start 31 --end 33

css:
	cat index.html | sed s,https://slexilData.artsrn.ualberta.ca/includes/slexil.css,slexil.css, > index2.html
	cat index2.html | sed s,https://slexilData.artsrn.ualberta.ca/includes/slexil.js,slexil.js, > index3.html

publish:
	scp index.html pshannon@206.12.95.4:www/lushootseed/$(PROJECT)/$(HTML.FILE)
	scp kb.js pshannon@206.12.95.4:www/lushootseed/$(PROJECT)/
	scp *.jpg pshannon@206.12.95.4:www/lushootseed/$(PROJECT)/
	scp volume1.wav pshannon@206.12.95.4:www/lushootseed/$(PROJECT)/

publish-text:
	scp index.html pshannon@206.12.95.4:www/lushootseed/$(PROJECT)/$(HTML.FILE)
	scp kb.js pshannon@206.12.95.4:www/lushootseed/$(PROJECT)/

view:
	open index.html

viewRemote:
	open https://slexildata.artsrn.ualberta.ca/lushootseed/$(PROJECT)/$(HTML.FILE)
