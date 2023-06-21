default:
	@echo targets:  build bash run test view rm ls

venv:
	@echo source ../py3105/bin/activate

build:
	docker build -t helloflask .

run:
	docker run -d --name helloFlaskContainer -p 9001:80 helloflask

view:
	open http://localhost:9001

test:
	curl http://localhost:9001

rm:
	docker stop helloFlaskContainer
	docker rm helloFlaskContainer

bash:
	docker run -ti --rm  -p 9001:80 helloflask bash

ls:
	docker images | grep hello
