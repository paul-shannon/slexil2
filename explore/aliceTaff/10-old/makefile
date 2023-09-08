PROJECT_NUMBER = 10
EAF = 10DavidGeorge230503Slexil.eaf
MOVIE = DavidGeorge9-9-10.m4v

default:
	@echo targets:  venv html scp-media scp-html test-url

venv:
	@echo source /Users/paul/github/slexil2/py3105/bin/activate

html: 
	python ../../../utils/eaf2html.py \
               --eaf $(EAF) \
               --terms grammaticalTerms.txt \
               --tierGuide tierGuide.yaml \
               --projectDirectory ./ \
               --addFontSizeControls 
#               --verbose \
#               --startLine 2 \
#               --endLine 10


scp-media:
	scp $(MOVIE) pshannon@206.12.91.237:tmp/

scp-html:
	scp index.html pshannon@206.12.91.237:tmp/10.html

test-url:
	curl -X HEAD -I https://slexildata.artsrn.ualberta.ca/tlingit/$(MOVIE)
