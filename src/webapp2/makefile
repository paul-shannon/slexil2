IMAGE = pshannon/slexilwebapp2
NAME = slexilwebapp2
PORT = 9002
VERSION = 262

default:
	@echo venv
	@echo assemble
	@echo runNoDocker
	@echo openNoDocker
	@echo killNoDocker
	@echo setDockerPlatform
	@echo build
	@echo run
	@echo push
	@echo test
	@echo ps
	@echo start
	@echo bash
	@echo stop
	@echo logs
	@echo clean
	@echo rm
	@echo open
	@echo checkAlberta


venv:
	@echo source /Users/paul/github/slexil2/py3105slexil/bin/activate

assemble:
	(cd parts; make assemble)
	cp parts/app.py main.py
	cp parts/app.py app/main.py

setDockerPlatform:
	@echo export DOCKER_DEFAULT_PLATFORM=linux/amd64

build:
	docker build -q -t $(IMAGE) .

runNoDocker:
	@echo no-docker version needs port other than 80
	python main.py

openNoDocker:
	open http://localhost:$(PORT)

killNoDocker:
	kill `netstat | grep $(PORT) | awk '{print $$2}'`

run:
	docker run --rm --name $(NAME) -p $(PORT):80 $(IMAGE)

ps:
	docker ps -a   # running and stopped containers

start:
	docker start $(NAME)

bash:
	docker exec -it $(NAME) bash

stop:
	docker stop $(NAME)

rm:
	docker rm -f $(NAME)

test:
	curl http://localhost:$(PORT)
	@echo

logs:
	docker logs $(NAME)

open:
	open http://localhost:$(PORT)

clean:
	docker rmi $$(docker images -f "dangling=true" -q)

push:
	docker push $(IMAGE)

checkAlberta:
	curl -L slexil.artsrn.ualberta.ca  | grep -i "<title>"
	curl -L slexiltest.artsrn.ualberta.ca  | grep -i "<title>"
