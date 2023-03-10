PORT = 8123
default:
	@echo targets: venv http find.port eaf extractAudio html kb tailor view.local publish

venv:
	@echo be sure to run: source /Users/paul/github/slexil2/py3105/bin/activate

http:
	python3 -m http.server $(PORT) &

find.port:
	lsof -i -n -P | grep TCP | grep $(PORT)

eaf:
	python ~/github/slexil2/yamlToEAF/toEAF.py gettingLight.yaml 

extractAudio:
	python ~/github/slexil2/yamlToEAF/extractAudioPhrases.py \
                               ../daylight.wav \
                               gettingLight.eaf \
                               audio

html:
	python eaf2html.py 

tailor:
	sed -f insertCustomCode.sed daylight-verbs-0.html  > daylight-verbs.html

view-local:
	open http://localhost:$(PORT)/daylight-verbs.html


kb:
	m4 --quiet -P ../kb.pre > kb.pre2
	sed  s/COMMA/,/g kb.pre2 > kb.js

view.local:
	open http://localhost:8123/daylight-verbs.html

publish:
	scp * paulshannnon@pshannon.net:public_html/pshannon.net/slexil2/

view:
	open   https://pshannon.net/slexil2/

