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
	docker build -t pshannon/slexil .

runDocker:
	docker run -d --name slexilContainer -p 9003:80 pshannon/slexil

viewDocker:
	open http://localhost:9003

test:
	curl http://localhost:9003

rm:
	- docker stop slexilContainer
	- docker rm slexilContainer

bash:
	docker run -ti --rm -p 9003:80 pshannon/slexil bash

ls:
	docker images | grep slexil

