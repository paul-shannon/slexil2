default:
	@echo venv
	@echo install
	@echo inferno
	@echo inferno-broken
	@echo eafs-all
	@echo eafs-all
	@echo clean
	@echo tiny  - just 2 eafs
	@echo try    - many eafs, then divide into goot, broken, needsWork
	@echo broken - many eafs, found to be broken

venv:
	@echo source ~/github/slexil2/py3105slexil/bin/activate

clean:
	- rm testResults/*

install:
	(cd ..; pip install . --upgrade)

inferno:
	python validXML.py ../testData/EAFv3.0.xsd \
                      ../testData/inferno/inferno-threeLines.eaf

inferno-broken:
	python validXML.py ../testData/EAFv3.0.xsd \
                      ../testData/inferno/inferno-threeLines-brokenTierTree.eaf

eafs-all:
	bash run-dbeck-188.sh  >> log.txt 2>&1

try:
	python eaf2yaml2html.py try.txt  >> log.txt 2>&1

broken:
	python eaf2yaml2html.py broken.txt  >> broken.log 2>&1

tiny:
	python eaf2yaml2html.py try2.txt  >> log.txt 2>&1
