NAME = mycontainer
PORT = 8008

default:
	@echo build
	@echo run
	@echo test
	@echo ps
	@echo start
	@echo stop
	@echo logs
	@echo rm


build:
	docker build -q -t $(NAME) .

run:
	docker run -d --name $(NAME) -p $(PORT):80 $(NAME)

ps:
	docker ps -a   # running and stopped containers

start:
	docker start $(NAME)

stop:
	docker stop $(NAME)

rm:
	docker rm -f $(NAME)

test:
	curl http://localhost:$(PORT)
	@echo

logs:
	docker logs $(NAME)
