NAME = soboleffRamos

default:
	@echo targets:
	@echo   venv validateXML eaf http refresh-js html
	@echo   tailor open-local
	@echo   mkdir testdir 
	@echo   publish open
	@echo   check

check:
	ls -lat ~/github/slexil2/py3105/lib/python3.10/site-packages/slexil*


venv:
	@echo source /Users/paul/github/slexil2/py3105/bin/activate

PORT = 8009

eaf:
	python ~/github/yamlToEAF/toEAF.py $(NAME).yaml

validateXML:
	python validate.py

html: 
	python ~/github/slexil2/utils/eaf2html.py \
               --eaf $(NAME).eaf \
               --terms grammaticalTerms.txt \
               --tierGuide tierGuide.yaml \
               --projectDirectory ./ \
               --verbose \
               --addFontSizeControls
#               --kb kb.js \
#               --linguistics linguistics.js

#               --startLine 121 \
#               --endLine 126



publish:
	scp index.html pshannon@206.12.95.4:www/tlingit/54.html


publish-all:
	scp index.html paulshannnon@pshannon.net:public_html/pshannon.net/tlingit-demos/$(PROJECT_NUMBER)/
	scp slexil.css paulshannnon@pshannon.net:public_html/pshannon.net/tlingit-demos/$(PROJECT_NUMBER)/
	scp slexil.js paulshannnon@pshannon.net:public_html/pshannon.net/tlingit-demos/$(PROJECT_NUMBER)/

open-local:
	open index.html

open:
	open https://pshannon.net/tlingit-demos/$(PROJECT_NUMBER)/index.html

mkdir:
	ssh paulshannnon@pshannon.net mkdir public_html/pshannon.net/tlingit-demos/$(PROJECT_NUMBER)

testdir:
	ssh paulshannnon@pshannon.net ls -l public_html/pshannon.net/tlingit-demos/$(PROJECT_NUMBER)
