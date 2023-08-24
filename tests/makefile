default:
	@echo targets: venv all install
	@echo webPacker
	@echo eafParser
	@echo ijalLine
	@echo text
	@echo morphemeGloss
	@echo listTiers

venv:
	@echo source ~/github/slexil2/py3105/bin/activate

dev:
	python -m unittest test_eafParser.py

all: webPacker eafParser ijalLine text morphemeGloss

webPacker:
	python -m unittest test_webPacker.py 

eafParser:
	python test_eafParser.py

ijalLine:
	python test_IjalLine.py

text:
	python test_Text.py

morphemeGloss:

	python -m unittest test_MorphemeGloss.py

listTiers:
	python -m unittest test_listTiers.py

#	python -m unittest test_infernoDemo.py
#	python -m unittest test_infernoDemo_toHTML.py

install:
	(cd ..; make install)

pipgit:
	(cd ..; make gitpip)

check:
	(cd ..; make check)

infernoDemo:
	python demoInferno.py
	open inferno.html
