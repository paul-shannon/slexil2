default:
	@echo targets:  venv http html tailor view-local publish-html publish-audio publish-video open

venv:
	@echo be sure to run: source /Users/paul/github/slexil2/py3105/bin/activate

PORT = 8009
http:
	python -m http.server $(PORT) &

html:
	python3 ruth-eaf2html.py 

tailor:
	sed -f insertCustomCode.sed ruth0.html  > ruth.html

view-local:
	open http://localhost:$(PORT)/ruth.html

publish-html:
	scp ruth.html paulshannnon@pshannon.net:public_html/pshannon.net/tlingit-demos/
	scp ijal.css paulshannnon@pshannon.net:public_html/pshannon.net/tlingit-demos/
	scp ijalUtils.js paulshannnon@pshannon.net:public_html/pshannon.net/tlingit-demos/


publish-all:
	scp ruth.html paulshannnon@pshannon.net:public_html/pshannon.net/tlingit-demos/
	scp ijal.css paulshannnon@pshannon.net:public_html/pshannon.net/tlingit-demos/
	scp jquery-3.3.1.min.js paulshannnon@pshannon.net:public_html/pshannon.net/tlingit-demos/
	scp ijalUtils.js paulshannnon@pshannon.net:public_html/pshannon.net/tlingit-demos/
	scp audio/* paulshannnon@pshannon.net:public_html/pshannon.net/tlingit-demos/audio

publish-video:
	scp 1RuthNora2Wide.m4v paulshannnon@pshannon.net:public_html/pshannon.net/tlingit-demos

publish-audio:
	scp audio/* paulshannnon@pshannon.net:public_html/pshannon.net/tlingit-demos/audio

open:
	open https://pshannon.net/tlingit-demos/ruth.html
