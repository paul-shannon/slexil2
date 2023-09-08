EAF = 56RuthMarsha230607Slexil.eaf
HTML.FILE = 56RuthMarsha.html

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
	curl -I https://slexildata.artsrn.ualberta.ca/tlingit/1RuthNora2Wide.m4v

html:
	python ../toHTML.py  --eaf $(EAF) \
                           --tierGuide tierGuide.yaml
#			   --start 31 --end 33

publish:
	scp index.html pshannon@206.12.95.4:www/tlingit/$(HTML.FILE)

viewRemote:
	open https://slexildata.artsrn.ualberta.ca/tlingit/$(HTML.FILE)
