include ../../makefile-shared
BASEDIR=~/github/slexil2
LANGUAGE = lushootseed
BASE =  starChild-susieSampsonPeter
SFMT.FILE =  starChild.yaml
HTML.FILE = $(BASE).html
HELP_FILE = help.html
VID = candidate-01.wav
TITLE = "Star Child - Susie Sampson Peter"
PORT =  12340

s2hl:
	python $(BASEDIR)/utils/sfmt2html.py \
        --sfmt $(SFMT.FILE) \
        --htmlFile $(BASE).html \
        --pageTitle $(TITLE) \
        --helpButtonLabel "How To" \
        --helpFile $(HELP_FILE) \
        --provideRecording 



#        --kbFilename kb-raven-daylight.js \
#         --verbose \


