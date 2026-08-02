default:
	@echo venv
	@echo server
	@echo view
	@echo run

venv:
	@echo source /Users/paul/github/slexil2/py3119slexil/bin/activate

PORT = 8883

server:
	python -m http.server $(PORT) &

view:
	open http://localhost:$(PORT)/demo.html

run:
	open http://localhost:$(PORT)/demo.html
