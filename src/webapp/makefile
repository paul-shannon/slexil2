default:
	@echo venv
	@echo pkgs
	@echo run
	@echo run-minimal
	@echo dockerBuild
	@echo dockerBuild-noCache
	@echo dockerBash
	@echo dockerRun
	@echo dockerClean


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

dockerBuild-noCache:
	docker build --rm --no-cache -t pshannon/slexil2 .

dockerBash:
	docker run -ti --rm -p 10004:80 pshannon/slexil2 bash

dockerRun:
	docker run -d --name slexil2Container -p 10004:80 pshannon/slexil2

dockerStop:
	docker stop slexil2Container
	docker rm slexil2Container

dockerClean:
	docker rmi $$(docker images -f "dangling=true" -q)

