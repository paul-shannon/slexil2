NAME = owlLivesThere

default:
	@echo targets:
	@echo  venv 
	@echo  y2h
	@echo  eaf
	@echo  s2h
	@echo  html
	@echo  view
	@echo  publish
	@echo  viewRemote

venv:
	@echo source /Users/paul/github/slexil2/py3119slexil/bin/activate

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

s2h:
	python ~/github/slexil2/utils/sfmt2html.py \
        --sfmt owlLivesThere.yaml \
        --htmlFile owlLivesThere.html \
        --pageTitle "Martha Lamont - Owl Lives There" \
        --helpButtonLabel About \
        --helpFile about.html


publish:
	scp owlLivesThere.html pshannon@134.87.10.153:www/lushootseed/marthaLamont/owlLivesThere/
	scp owlLivesThere-mono-8k.wav pshannon@134.87.10.153:www/lushootseed/marthaLamont/owlLivesThere/

view:
	open owlLivesThere.html

viewRemote:
	open https://slexildata.artsrn.ualberta.ca/lushootseed/marthaLamont/owlLivesThere
