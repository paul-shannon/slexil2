include ../../../makefile-shared
BASEDIR=~/github/slexil2
LANGUAGE = tlingit
BASE = ravenAndHisUncle
SFMT.FILE = $(BASE).yaml
HELP_FILE = help.html
HTML.FILE = ravenAndHisUncle.html
VID = ravenAndHisUncle.wav
#VID = https://aklanguages.uas.alaska.edu/tlingit/breakRules-mono.1-3.wav
TITLE = "Yéil k̲a Du Kaak: Raven and His Uncle"
HOST = https://aklanguages.uas.alaska.edu
PORT =  12341

s2h:
	python $(BASEDIR)/utils/sfmt2html.py \
        --sfmt ravenAndHisUncle.yaml \
        --htmlFile ravenAndHisUncle.html \
        --kbFilename kb-raven.js \
        --pageTitle $(TITLE) \
        --helpButtonLabel About \
        --helpFile $(HELP_FILE) \
        --provideRecording 



