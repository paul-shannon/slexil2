STORY = beckAndHess
YAML2EAF = ~/github/slexil2/yamlToEAF/toEAF.py

default:
	@echo targets: venv  eaf extractAudio html tailor open publish open-remote

venv:
	@echo be sure to run: source /Users/paul/github/slexil2/py3105/bin/activate



eaf:
	python ~/github/slexil2/yamlToEAF/toEAF.py $(STORY).yaml


html:
	python daylight-eaf2html.py 

tailor:
	sed -f insertCustomCode.sed $(STORY)0.html  > $(STORY).html

open:
	open $(STORY).html

extractAudio:
	python ~/github/slexil2/yamlToEAF/extractAudioPhrases.py \
                               daylight.wav \
                               $(STORY).eaf \
                               audio

STORY-DIR  = daylight-beckHess2007

publish-html:
	scp beckAndHess.html paulshannnon@pshannon.net:public_html/pshannon.net/$(STORY-DIR)/
	scp ijal.css paulshannnon@pshannon.net:public_html/pshannon.net/$(STORY-DIR)/
	scp ijalUtils.js paulshannnon@pshannon.net:public_html/pshannon.net/$(STORY-DIR)/


publish-all:
	scp beckAndHess.html paulshannnon@pshannon.net:public_html/pshannon.net/$(STORY-DIR)/
	scp ijal.css paulshannnon@pshannon.net:public_html/pshannon.net/$(STORY-DIR)/
	scp ijalUtils.js paulshannnon@pshannon.net:public_html/pshannon.net/$(STORY-DIR)/
	scp audio/* paulshannnon@pshannon.net:public_html/pshannon.net/$(STORY-DIR)/audio

publish-audio:
	scp audio/* paulshannnon@pshannon.net:public_html/pshannon.net/$(STORY-DIR)/audio

open-remote:
	open https://pshannon.net/$(STORY-DIR)/beckAndHess.html



