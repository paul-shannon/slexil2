default:
	@echo venv
	@echo assemble
	@echo main
	@echo run

venv:
	@echo source /Users/paul/github/slexil2/py3105slexil/bin/activate

assemble:
	m4 -P app.pre > app.py

run:
	python app.py

main:
	m4 -P app.pre > ../app/main.py
	@echo  check port number, should be 80



