default:
	@echo targets:   build  bash run

build:
	docker build -t helloflask .

run:
	docker run -d -p 9001:80 helloflask
#	docker run -d --name helloFlaskContainer -p 9001:80 helloflask

bash:

ls:
	docker images | grep hello
