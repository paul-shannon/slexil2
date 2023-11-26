NAME = ladyLouse


default:
	@echo targets:
	@echo  venv eaf http refresh-js html
	@echo  eaf
	@echo  html
	@echo  css
	@echo  view
	@echo  publish
	@echo  viewRemote

venv:
	@echo source /Users/paul/github/slexil2/py3105slexil/bin/activate

eaf:
	python ~/github/yamlToEAF/toEAF.py $(NAME).yaml


html:
	python ../../../utils/eaf2html.py  --eaf $(NAME).eaf \
                       --tierGuide tierGuide.yaml \
                       --terms grammaticalTerms.txt \
                       --pageTitle "Lady Louse" \
                       --fontSizeControls \
                       --helpFile about.html \
                       --helpButtonLabel About \
                       --webpackLinksOnly
css:
	cat index.html | sed s,https://slexilData.artsrn.ualberta.ca/includes/slexil.css,slexil.css, > index2.html
	cat index2.html | sed s,https://slexilData.artsrn.ualberta.ca/includes/slexil.js,slexil.js, > index3.html



publish:
	scp *.html pshannon@206.12.95.4:www/lushootseed/ladyLouse/

view:
	open index.html

viewRemote:
	open https://slexildata.artsrn.ualberta.ca/lushootseed/ladyLouse/index.html


