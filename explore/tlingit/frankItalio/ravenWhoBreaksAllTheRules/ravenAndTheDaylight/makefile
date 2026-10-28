include ../../../makefile-shared
BASEDIR=~/github/slexil2
LANGUAGE = tlingit
BASE = ravenAndTheDaylight
SFMT.FILE = $(BASE).yaml
HELP_FILE = help.html
HTML.FILE = $(BASE).html
VID = ravenAndTheDaylight.wav
TITLE = "Yéil ḵa Ḵei.á: Raven and the Daylight"
HOST = https://aklanguages.uas.alaska.edu
PORT =  12342

s2hv:
	python $(BASEDIR)/utils/sfmt2html.py \
        --sfmt $(BASE).yaml \
        --htmlFile $(BASE).html \
        --pageTitle $(TITLE) \
        --verbose \
        --helpButtonLabel About \
        --helpFile $(HELP_FILE) \
        --kbFilename kb-raven-daylight.js \
        --provideRecording 


publish-kb:
	scp kb-raven-daylight.js ptshannon@10.194.218.48:tlingit/



