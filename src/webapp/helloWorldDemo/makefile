default:
	@echo build
	@echo run
	@echo ps
	@echo bashIn
	@echo logs
	@echo curl
	@echo stop

build:
	docker build -t pshannon/hellodemo .

run:
	docker run -d --name helloDemoContainer -p 1002:80 pshannon/hellodemo

ps:
	docker ps

bashIn:
	docker exec -it helloDemoContainer bash

logs:
	docker logs helloDemoContainer

stop:
	docker stop helloDemoContainer
	docker rm helloDemoContainer

curl:
	curl http://localhost:1002


