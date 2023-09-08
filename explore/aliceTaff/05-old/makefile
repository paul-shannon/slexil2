EAF = 5ArchieGeorge230503Slexil.eaf
MEDIA = ArchieGeorge5All.wav
HTML.FILE = 5ArchieGeorge.html

default:
	@echo movieCurl
	@echo valid
	@echo venv
	@echo html
	@echo publish
	@echo viewRemote

venv:
	@echo source /Users/paul/github/slexil2/py3105/bin/activate

valid:
	python ~/github/slexil2/utils/validXML.py $(EAF) 2>&1 | more

movieCurl:
	curl -I https://slexildata.artsrn.ualberta.ca/tlingit/$(MEDIA)

html:
	python toHTML.py


publish:
	scp index.html pshannon@206.12.95.4:www/tlingit/$(HTML.FILE)

viewRemote:
	open https://slexildata.artsrn.ualberta.ca/tlingit/$(HTML.FILE)
