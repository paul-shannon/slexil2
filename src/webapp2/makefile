NAME = pshannon/slexilwebapp2
PORT = 8009
VERSION = 262

default:
	@echo venv
	@echo runNC
	@echo openNC
	@echo killNC
	@echo build
	@echo run
	@echo test
	@echo ps
	@echo start
	@echo bash
	@echo stop
	@echo logs
	@echo rm
	@echo open
	@echo checkAlberta


venv:
	@echo source /Users/paul/github/slexil2/py3105slexil/bin/activate

build:
	docker build -q -t $(NAME):$(VERSION) .

runNC:
	@echo change later restore port number
	python app/main.py &

openNC:
	open http://localhost:8001

killNC:
	kill `netstat | grep 8001 | awk '{print $2}'`

run:
	docker run -d --name $(NAME) -p $(PORT):80 $(NAME):$(VERSION)

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
	docker push $(NAME):$(VERSION)

checkAlberta:
	curl -L slexil.artsrn.ualberta.ca  | grep -i "<title>"
	curl -L slexiltest.artsrn.ualberta.ca  | grep -i "<title>"
