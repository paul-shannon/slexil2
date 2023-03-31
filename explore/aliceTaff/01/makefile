PROJECT_NUMBER = 01
EAF = 01RuthNora230209AT.eaf


default:
	@echo targets:  venv http update-slexil-code html open-local mkdir testdir 
	@echo targets: publish open

venv:
	@echo be sure to run: source /Users/paul/github/slexil2/py3105/bin/activate

PORT = 8009

http:
	python -m http.server $(PORT) &

html: update-slexil-code
	python ../../../utils/eaf2html.py \
               --eaf $(EAF) \
               --terms grammaticalTerms.txt \
               --tierGuide tierGuide.yaml \
               --projectDirectory ./ \
               --quiet \
               --addFontSizeControls
#               --startLine 121 \
#               --endLine 126

update-slexil-code:
	cp -p ../slexil.* .


publish:
	scp index.html paulshannnon@pshannon.net:public_html/pshannon.net/tlingit-demos/$(PROJECT_NUMBER)/
	scp slexil.css paulshannnon@pshannon.net:public_html/pshannon.net/tlingit-demos/$(PROJECT_NUMBER)/
	scp slexil.js paulshannnon@pshannon.net:public_html/pshannon.net/tlingit-demos/$(PROJECT_NUMBER)/


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
