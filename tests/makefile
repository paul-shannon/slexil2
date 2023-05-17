default:
	@echo targets: test build

test:
	python -m unittest test_htmlInserter.py
	python -m unittest test_listTiers.py
	python -m unittest test_morphemeGloss.py
	python -m unittest test_infernoDemo.py
	python -m unittest test_infernoDemo_toHTML.py

install:
	(cd ..; make install)
