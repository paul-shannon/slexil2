default:
	@echo venv
	@echo pkgs
	@echo install
	@echo run
	@echo run-minimal
	@echo dockerBuild
	@echo dockerBuild-noCache
	@echo dockerBash
	@echo dockerRun
	@echo dockerStop
	@echo dockerClean
	@echo dockerHelloBuild

venv:
	source ~/github/slexil2/py3105/bin/activate

pkgs:
	pip install -r requirements.txt

install:
	(cd ../..; make install)

run:
	python main.py

run-minimal:
	python main-minimal.py

dockerHelloBuild:
	docker build -t pshannon/slexil2:v236 -f Dockerfile-helloWorld .

dockerBuild:
	docker build -t pshannon/slexil2:v236 .

dockerBuild-noCache:
	docker build --rm --no-cache -t pshannon/slexil2:v236 .

dockerBash:
	docker run -ti --rm -p 10004:80 pshannon/slexil2:v236 bash

dockerRun:
	docker run -d --name slexil2Container -p 10004:80 pshannon/slexil2:v236

dockerStop:
	docker stop slexil2Container
	docker rm slexil2Container

dockerClean:
	docker rmi $$(docker images -f "dangling=true" -q)

