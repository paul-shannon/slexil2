HTML.FILE = taoteching.html

default:
	@echo venv
	@echo s2h
	@echo view
	@echo publish
	@echo viewRemote

venv:
	@echo source /Users/paul/github/slexil2/py3105slexil/bin/activate

s2h:
	python ~/github/slexil2/utils/sfmt2html.py \
        --sfmt taoteching.yaml \
        --htmlFile $(HTML.FILE) \
        --kbFilename kb.js \
        --grammaticalTerms none \
        --pageTitle "Dao De Jing" 
#         --verbose \

publish:
	scp $(HTML.FILE) pshannon@206.12.95.4:www/misc/
	scp kb.js pshannon@206.12.95.4:www/misc/
	scp daodeching-8.wav pshannon@206.12.95.4:www/misc/

view:
	open taoteching.html

viewRemote:
	open https://slexildata.artsrn.ualberta.ca/misc/$(HTML.FILE)
