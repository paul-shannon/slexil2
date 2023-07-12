VERSION = v239
PORT = 1003

default:
	@echo venv
	@echo pkgs
	@echo install
	@echo run
	@echo run-minimal
	@echo build
	@echo build-noCache
	@echo push
	@echo bash
	@echo bashIn
	@echo run
	@echo stop
	@echo clean
	@echo logs

venv:
	source ~/github/slexil2/py3105/bin/activate

pkgs:
	pip install -r requirements.txt

install:
	(cd ../..; make install)

build:
	docker build -t pshannon/slexil2:$(VERSION) .

build-noCache:
	docker build --rm --no-cache -t pshannon/slexil2:$(VERSION) .

bash:
	docker run -ti --rm -p $(PORT):80 pshannon/slexil2:$(VERSION) bash

bashIn:
	docker exec -it slexil2Container bash

run:
	docker run -d --name slexil2Container -p $(PORT):80 pshannon/slexil2:$(VERSION)

curl:
	curl http://localhost:$(PORT)

stop:
	docker stop slexil2Container
	docker rm slexil2Container

clean:
	docker rmi $$(docker images -f "dangling=true" -q)

push:
	docker push pshannon/slexil2:$(VERSION)

logs:
	docker logs slexil2Container
