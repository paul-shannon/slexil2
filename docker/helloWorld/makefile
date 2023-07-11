default:
	@echo targets:  build bash run test view rm ls

venv:
	@echo source ../py3105/bin/activate

build:
	docker build -t pshannon/helloslexil .

run:
	docker run -d --name helloSlexilContainer -p 9001:80 pshannon/helloslexil

view:
	open http://localhost:9001

test:
	curl http://localhost:9001

rm:
	docker stop helloSlexilContainer
	docker rm helloSlexilContainer

bash:
	docker run -ti --rm  -p 9001:80 pshannon/helloslexil bash

ls:
	docker images | grep hello
