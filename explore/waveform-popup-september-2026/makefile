default:
	@echo venv
	@echo server
	@echo pid
	@echo html

venv:
	@echo source /Users/paul/github/slexil2/py3119slexil/bin/activate

PORT = 9012

server:
	python -m http.server $(PORT) &

pid:
	lsof -i -n -P | grep $(PORT)

html:
	open http://localhost:$(PORT)/skeleton.html

