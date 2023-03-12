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
	sed -f insertCustomCode.sed ruth0.html  > ruth1.html
	cat ruth1.html | sed 's/<audio.*audio>//g' > ruth.html

view-local:
	open http://localhost:$(PORT)/ruth.html

publish-html:
	scp ruth.html paulshannnon@pshannon.net:public_html/pshannon.net/tlingit-demos/v2/
	scp *.css paulshannnon@pshannon.net:public_html/pshannon.net/tlingit-demos/v2/
	scp ijalUtils.js paulshannnon@pshannon.net:public_html/pshannon.net/tlingit-demos/v2/


publish-all:
	scp ruth.html paulshannnon@pshannon.net:public_html/pshannon.net/tlingit-demos/v2/
	scp ijal.css paulshannnon@pshannon.net:public_html/pshannon.net/tlingit-demos/v2/
	scp jquery-3.3.1.min.js paulshannnon@pshannon.net:public_html/pshannon.net/tlingit-demos/v2/
	scp ijalUtils.js paulshannnon@pshannon.net:public_html/pshannon.net/tlingit-demos/v2/
	scp audio/* paulshannnon@pshannon.net:public_html/pshannon.net/tlingit-demos/v2/audio

publish-video:
	scp 1RuthNora2Wide.m4v paulshannnon@pshannon.net:public_html/pshannon.net/tlingit-demos

publish-audio:
	scp audio/* paulshannnon@pshannon.net:public_html/pshannon.net/tlingit-demos/v2/audio

open:
	open https://pshannon.net/tlingit-demos/v2/ruth.html
