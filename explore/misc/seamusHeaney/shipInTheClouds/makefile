NAME = shipInTheClouds
YAML = $(NAME).yaml
EAF = $(NAME).eaf
HTML.FILE = $(NAME).html
MEDIA = seamusHeaneyListenings7-perdue-Kimble.wav

default:
	@echo valid
	@echo venv
	@echo curl
	@echo eaf
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
	curl -I https://slexildata.artsrn.ualberta.ca/misc/seamusHeaney/$(MEDIA)

eaf:
	python ~/github/yamlToEAF/toEAF.py $(YAML)

html:
	python ~/github/slexil2/utils/eaf2html.py  --eaf $(EAF) \
                       --tierGuide tierGuide.yaml \
                       --pageTitle "Lightenings vii" \
                       --helpFile about.html \
                       --helpButtonLabel About \
                       --verbose
#                       --toolTips
#			   --start 31 --end 33

publish:
	scp index.html pshannon@206.12.95.4:www/misc/seamusHeaney/$(HTML.FILE)
	scp seamusHeaneyListenings7-perdue-Kimble.wav pshannon@206.12.95.4:www/misc/seamusHeaney/


view:
	open index.html

viewRemote:
	open https://slexildata.artsrn.ualberta.ca/misc/seamusHeaney/$(HTML.FILE)
