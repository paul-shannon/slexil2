EAF = inferno-threeLines.eaf
HTML.FILE = inferno.html

default:
	@echo mediaTest
	@echo valid
	@echo venv
	@echo eaf
	@echo html
	@echo publish
	@echo view
	@echo viewRemote

venv:
	@echo source /Users/paul/github/slexil2/py3105/bin/activate

valid:
	python ~/github/slexil2/utils/validXML.py $(EAF) 2>&1 | more

mediaTest:
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
                       --webpackLinksOnly \
                       --fontSizeControls
#                       --verbose
#			   --start 31 --end 33

publish:
	scp index.html pshannon@206.12.95.4:www/misc/$(HTML.FILE)

view:
	open index.html

viewRemote:
	open https://slexildata.artsrn.ualberta.ca/misc/$(HTML.FILE)
