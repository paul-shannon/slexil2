default:
	@echo targets: venv dev test install

venv:
	@echo source ~/github/slexil2/py3105/bin/activate

dev:
	python -m unittest test_eafParser.py

test:
	python -m unittest test_webPacker.py 
	python test_eafParser.py
	python test_IjalLine.py
	python test_Text.py
	python -m unittest test_morphemeGloss.py
	python -m unittest test_listTiers.py
#	python -m unittest test_infernoDemo.py
#	python -m unittest test_infernoDemo_toHTML.py

install:
	(cd ..; make install)
