default:
	@echo venv
	@echo pkgs
	@echo run
	@echo run-minimal
	@echo dockerBuild
	@echo dockerBash
	@echo dockerRun


venv:
	source ~/github/slexil2/py3105/bin/activate

pkgs:
	pip install -r requirements.txt

run:
	python main.py

run-minimal:
	python main-minimal.py

dockerBuild:
	docker build -t pshannon/slexil2 .

dockerBash:
	docker run -ti --rm -p 9004:80 pshannon/slexil2 bash

dockerRun:
	docker run -d --name slexil2Container -p 10004:8008 pshannon/slexil2

