default:
	@echo venv
	@echo server
	@echo demo  - record and playback
	@echo publish

venv:
	@echo source /Users/paul/github/slexil2/py3105slexil/bin/activate

server:
	python -m http.server 9999 &

F = skunkWorksTest.html

demo:
	open http://localhost:9999/$(F)


publish:
	scp $(F) paulshannnon@pshannon.net:public_html/pshannon.net/misc/
	open https://pshannon.net/misc/$(F)



