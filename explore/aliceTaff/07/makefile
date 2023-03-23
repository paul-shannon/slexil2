PROJECT_NUMBER = 07
PROJECT_NAME = florence


default:
	@echo targets:  venv http html view-local mkdir testdir 
	@echo targets: publish-html open

venv:
	@echo be sure to run: source /Users/paul/github/slexil2/py3105/bin/activate

PORT = 8009

http:
	python -m http.server $(PORT) &

html:
	python3 eafToHtml.py #7FlorenceRon230302AT.eaf FlorenceRon7-27-09.m4v $(PROJECT)

publish-html:
	scp $(PROJECT_NAME).html paulshannnon@pshannon.net:public_html/pshannon.net/tlingit-demos/$(PROJECT_NUMBER)/
	scp slexil.css paulshannnon@pshannon.net:public_html/pshannon.net/tlingit-demos/$(PROJECT_NUMBER)/
	scp slexil.js paulshannnon@pshannon.net:public_html/pshannon.net/tlingit-demos/$(PROJECT_NUMBER)/


publish-all:
	scp $(PROJECT_NAME).html paulshannnon@pshannon.net:public_html/pshannon.net/tlingit-demos/$(PROJECT_NUMBER)/
	scp slexil.css paulshannnon@pshannon.net:public_html/pshannon.net/tlingit-demos/$(PROJECT_NUMBER)/
	scp slexil.js paulshannnon@pshannon.net:public_html/pshannon.net/tlingit-demos/$(PROJECT_NUMBER)/


open:
	open https://pshannon.net/tlingit-demos/$(PROJECT_NUMBER)/$(PROJECT_NAME).html

mkdir:
	ssh paulshannnon@pshannon.net mkdir public_html/pshannon.net/tlingit-demos/$(PROJECT_NUMBER)

testdir:
	ssh paulshannnon@pshannon.net ls -l public_html/pshannon.net/tlingit-demos/$(PROJECT_NUMBER)
