NAME = owlLivesThere

default:
	@echo targets:
	@echo  venv 
	@evho  y2h
	@echo  eaf
	@echo  html
	@echo  view
	@echo  publish
	@echo  viewRemote

venv:
	@echo source /Users/paul/github/slexil2/py3105slexil/bin/activate

eaf:
	python ~/github/yamlToEAF/toEAF.py $(NAME).yaml


html:
	python ../../../../utils/eaf2html.py  --eaf $(NAME).eaf \
                       --tierGuide tierGuide.yaml \
                       --terms grammaticalTerms.txt \
                       --pageTitle "Martha Lamont - Owl Lives There" \
                       --fontSizeControls \
                       --helpFile about.html \
                       --helpButtonLabel About
#                       --webpackLinksOnly



y2h:
	python ~/github/slexil2/utils/yaml2html.py \
        --yaml owlLivesThere.yaml \
        --pageTitle "Martha Lamont - Owl Lives There" \
        --helpButtonLabel About \
        --helpFile about.html

publish:
	scp index.html pshannon@206.12.95.4:www/lushootseed/marthaLamont/owlLivesThere/
	scp owlLivesThere-mono-8k.wav pshannon@206.12.95.4:www/lushootseed/marthaLamont/owlLivesThere/

view:
	open index.html

viewRemote:
	open https://slexildata.artsrn.ualberta.ca/lushootseed/marthaLamont/owlLivesThere
