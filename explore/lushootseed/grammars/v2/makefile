PROJECT = grammar
EAF = $(PROJECT).eaf
HTML.FILE = hessAndHilbert2.html
BASEDIR=~/github/slexil2

default:
	@echo valid
	@echo venv
	@echo curl
	@echo server
	@echo s2h
	@echo eaf
	@echo html
	@echo css      # read local slexil.css, for experimentation
	@echo publish  # all text
	@echo publish-audio # the wav file
	@echo updateLocal [s2h view]
	@echo updateRemote
	@echo view
	@echo viewRemote
	@echo testyaml

venv:
	@echo source /Users/paul/github/slexil2/py3119slexil/bin/activate

valid:
	python ~/github/slexil2/utils/validXML.py $(EAF) 2>&1 | more

server:
	python -m http.server 8008


s2h:
	python $(BASEDIR)/utils/sfmt2html.py \
        --sfmt grammar2.yaml \
        --htmlFile $(HTML.FILE) \
        --kbFilename kb2.js \
        --pageTitle "Lushootseed Grammar 2" \
        --helpButtonLabel About \
        --helpFile about.html \
        --linguistics linguisticTerms2.js
#        --verbose

updateLocal: s2h view
updateRemote: s2h publish viewRemote

curl:
	curlyhead https://slexildata.artsrn.ualberta.ca/lushootseed/grammar/volume2.wav


# css:
# 	cat index.html | sed s,https://slexilData.artsrn.ualberta.ca/includes/slexil.css,slexil.css, > index2.html
# 	cat index2.html | sed s,https://slexilData.artsrn.ualberta.ca/includes/slexil.js,slexil.js, > index3.html
# 
publish:
	rsync -a $(HTML.FILE) pshannon@206.12.95.4:www/lushootseed/$(PROJECT)/$(HTML.FILE)
	rsync -a kb2.js pshannon@206.12.95.4:www/lushootseed/$(PROJECT)/
	rsync -a  linguisticTerms2.js pshannon@206.12.95.4:www/lushootseed/$(PROJECT)/
	rsync -a *.png pshannon@206.12.95.4:www/lushootseed/$(PROJECT)/

publish-audio:
	rsync -a  volume2.wav pshannon@206.12.95.4:www/lushootseed/$(PROJECT)/

view:
	open $(HTML.FILE)

viewRemote:
	open https://slexildata.artsrn.ualberta.ca/lushootseed/$(PROJECT)/$(HTML.FILE)

