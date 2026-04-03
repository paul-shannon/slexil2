default:
	@echo venv
	@echo server
	@echo pid
	@echo htmls

PORT = 5007

venv:
	@echo source /Users/paul/github/slexil2/py3119slexil/bin/activate

server:
	python -m http.server $(PORT) &

pid:
	lsof -i -n -P | grep $(PORT)

htmls:
	open http://127.0.0.1:$(PORT)



