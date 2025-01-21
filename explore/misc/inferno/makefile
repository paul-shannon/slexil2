EAF = inferno-threeLines.eaf
HTML.FILE = inferno.html

default:
	@echo valid
	@echo venv
	@echo curl
	@echo eaf
	@echo y2h
	@echo html
	@echo css      # read local slexil.css, for experimentation
	@echo publish
	@echo view
	@echo viewRemote

venv:
	@echo source /Users/paul/github/slexil2/py3105slexil/bin/activate

valid:
	python ~/github/slexil2/utils/validXML.py $(EAF) 2>&1 | more

curl:
	curl -I https://slexildata.artsrn.ualberta.ca/misc/inferno-threeLines.wav

eaf:
	python ~/github/yamlToEAF/toEAF.py  inferno-threeLines.yaml 

html:
	python ../../../utils/eaf2html.py  --eaf $(EAF) \
                       --tierGuide tierGuide.yaml \
                       --terms grammaticalTerms.txt \
                       --pageTitle "Dante's Inferno" \
                       --helpFile about.html \
                       --helpButtonLabel About \
                       --kbFilename kb.js \
                       --linguistics linguisticTerms.js \
                       --practice
#                       --webpackLinksOnly \
                       --verbose
#                       --toolTips
#			   --start 31 --end 33

css:
	cat index.html | sed s,https://slexilData.artsrn.ualberta.ca/includes/slexil.css,slexil.css, > index2.html
	cat index2.html | sed s,https://slexilData.artsrn.ualberta.ca/includes/slexil.js,slexil.js, > index3.html


y2h:
	python ~/github/slexil2/utils/yaml2html.py \
        --yaml inferno-threeLines.yaml \
        --pageTitle "Inferno" \
        --helpButtonLabel About \
        --helpFile about.html

y2h-mp3:
	python ~/github/slexil2/utils/yaml2html.py \
        --yaml inferno-mp3.yaml \
        --pageTitle "Inferno mp3" \
        --helpButtonLabel About \
        --helpFile about.html

y2h-ogg:
	python ~/github/slexil2/utils/yaml2html.py \
        --yaml inferno-ogg.yaml \
        --pageTitle "Inferno ogg" \
        --helpButtonLabel About \
        --helpFile about.html


publish:
	scp index.html pshannon@206.12.95.4:www/misc/$(HTML.FILE)

view:
	open index.html

viewRemote:
	open https://slexildata.artsrn.ualberta.ca/misc/$(HTML.FILE)


