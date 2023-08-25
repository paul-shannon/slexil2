NAME = howDaylightWasStolen


default:
	@echo targets:
	@echo   venv eaf http refresh-js html
	@echo   tailor open-local
	@echo   mkdir testdir 
	@echo   publish open

venv:
	@echo source /Users/paul/github/slexil2/py3105/bin/activate

PORT = 8009

http:
	python -m http.server $(PORT) &

eaf:
	python ~/github/yamlToEAF/toEAF.py $(NAME).yaml

html: 
	python ~/github/slexil2/utils/eaf2html.py \
               --eaf $(NAME).eaf \
               --terms grammaticalTerms.txt \
               --tierGuide tierGuide.yaml \
               --projectDirectory ./ \
               --addFontSizeControls \
               --kb kb.js \
               --linguistics linguisticTerms.js \
               --helpFile help.html \
               --helpButtonLabel  About \
               --pageTitle Daylight
#               --verbose 
#               --startLine 121 \
#               --endLine 126

tailor:
	sed -f insertCustomCode.sed index.html  > index0.html

refresh-js:
	cp -p ../../*.js .
	cp -p ../../slexil.css .



publish:
	scp index.html pshannon@206.12.95.4:www/lushootseed/harryMoses/daylight/
	scp kb.js pshannon@206.12.95.4:www/lushootseed/harryMoses/daylight/
	scp linguisticTerms.js pshannon@206.12.95.4:www/lushootseed/harryMoses/daylight/

open-local:
	open index.html

open:
	open https://pshannon.net/tlingit-demos/$(PROJECT_NUMBER)/index.html

mkdir:
	ssh paulshannnon@pshannon.net mkdir public_html/pshannon.net/tlingit-demos/$(PROJECT_NUMBER)

testdir:
	ssh paulshannnon@pshannon.net ls -l public_html/pshannon.net/tlingit-demos/$(PROJECT_NUMBER)
