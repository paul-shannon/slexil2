EAF = 4EthelAnita230503Slexil.eaf
MEDIA = 4EthelAnita.mov
HTML.FILE = 4EthelAnita.html

default:
	@echo movieCurl
	@echo valid
	@echo venv
	@echo html
	@echo view
	@echo publish
	@echo viewRemote

venv:
	@echo source /Users/paul/github/slexil2/py3105/bin/activate

valid:
	python ~/github/slexil2/utils/validXML.py $(EAF) 2>&1 | more

movieCurl:
	curl -I https://slexildata.artsrn.ualberta.ca/tlingit/$(MEDIA)

html:
	python ../../../utils/eaf2html.py  \
	                     --eaf $(EAF) \
                        --tierGuide tierGuide.yaml \
                        --helpFile ../help.html \
                        --helpButtonLabel "How To" \
                        --pageTitle "Tlingit Conversation #4" \
                        --fixOverlappingTimeSegments \
                        --fontSizeControls

view:
	open index.html

publish:
	scp index.html pshannon@206.12.95.4:www/tlingit/$(HTML.FILE)

viewRemote:
	open https://slexildata.artsrn.ualberta.ca/tlingit/$(HTML.FILE)
