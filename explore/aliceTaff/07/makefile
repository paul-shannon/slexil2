PROJECT = 07
default:
	@echo targets:  venv http html tailor view-local mkdir testdir 
	@echo targets: publish-html publish-audio publish-video open

venv:
	@echo be sure to run: source /Users/paul/github/slexil2/py3105/bin/activate

PORT = 8009

http:
	python -m http.server $(PORT) &

html:
	python3 eafToHtml.py #7FlorenceRon230302AT.eaf FlorenceRon7-27-09.m4v $(PROJECT)

tailor:
	sed -f insertCustomCode.sed $(PROJECT)-0.html  > $(PROJECT)-1.html
	cat $(PROJECT)1.html | sed 's/<audio.*audio>//g' > $(PROJECT).html

view-local:
	open http://localhost:$(PORT)/$(PROJECT).html

publish-html:
	scp $(PROJECT).html paulshannnon@pshannon.net:public_html/pshannon.net/tlingit-demos/v2/
	scp *.css paulshannnon@pshannon.net:public_html/pshannon.net/tlingit-demos/v2/
	scp ijalUtils.js paulshannnon@pshannon.net:public_html/pshannon.net/tlingit-demos/v2/


publish-all:
	scp $(PROJECT).html paulshannnon@pshannon.net:public_html/pshannon.net/tlingit-demos/v2/
	scp ijal.css paulshannnon@pshannon.net:public_html/pshannon.net/tlingit-demos/v2/
	scp jquery-3.3.1.min.js paulshannnon@pshannon.net:public_html/pshannon.net/tlingit-demos/v2/
	scp ijalUtils.js paulshannnon@pshannon.net:public_html/pshannon.net/tlingit-demos/v2/
	scp audio/* paulshannnon@pshannon.net:public_html/pshannon.net/tlingit-demos/v2/audio

publish-video:
	scp 1$(PROJECT)Nora2Wide.m4v paulshannnon@pshannon.net:public_html/pshannon.net/tlingit-demos

publish-audio:
	scp audio/* paulshannnon@pshannon.net:public_html/pshannon.net/tlingit-demos/v2/audio

open:
	open https://pshannon.net/tlingit-demos/v2/$(PROJECT).html

mkdir:
	ssh paulshannnon@pshannon.net mkdir public_html/pshannon.net/tlingit-demos/$(PROJECT)

testdir:
	ssh paulshannnon@pshannon.net ls -l public_html/pshannon.net/tlingit-demos/$(PROJECT)
