default:
	@echo testCode
	@echo testCodeDebug
	@echo venv
	@echo server
	@echo html

venv:
	@echo source /Users/paul/github/slexil2/py3119slexil/bin/activate

PORT = 9876

server:
	python -m http.server $(PORT) &

html:
	open http://localhost:$(PORT)/demoRWC.html

testCode:
	node --test

testCodeDebug:
	node inspect --test

