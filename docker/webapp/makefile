default:
	@echo --- shell targets:
	@echo venv pkgs run view
	@echo --- docker targets
	@echo build bash ls runDocker viewDocker

venv:
	@echo source ~/github/slexil2/docker/py3105/bin/activate

pkgs:
	pip install -r requirements.txt

run:
	python app/main.py

view:
	open http://localhost:8050


build:
	docker build -t pshannon/slexil2 .

runDocker:
	docker run -d --name slexil2Container -p 9004:80 pshannon/slexil2

viewDocker:
	open http://localhost:9004

test:
	curl http://localhost:9004

rm:
	- docker stop slexil2Container
	- docker rm slexil2Container

bash:
	docker run -ti --rm -p 9004:80 pshannon/slexil2 bash

ls:
	docker images | grep slexil

