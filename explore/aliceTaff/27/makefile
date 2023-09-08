EAF = 27LorraineVincent230714Slexil.eaf
HTML.FILE = 27LorraineVincent.html
VID = 27LorraineVincent.m4v
TITLE = "Tlingit Conversation \#27"

default:
	@echo movieCurl
	@echo valid
	@echo venv
	@echo html
	@echo publish
	@echo view
	@echo viewRemote

venv:
	@echo source /Users/paul/github/slexil2/py3105/bin/activate

movieCurl:
	curl -I https://slexildata.artsrn.ualberta.ca/tlingit/$(VID)

html:
	python ../../../utils/eaf2html.py  \
	                     --eaf $(EAF) \
                        --tierGuide tierGuide.yaml \
                        --helpFile ../help.html \
                        --helpButtonLabel "How To" \
                        --pageTitle $(TITLE) \
                        --fixOverlappingTimeSegments \
	                     --fontSizeControls

publish:
	scp index.html pshannon@206.12.95.4:www/tlingit/$(HTML.FILE)

view:
	open index.html

viewRemote:
	open https://slexildata.artsrn.ualberta.ca/tlingit/$(HTML.FILE)

