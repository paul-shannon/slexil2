default:
	@echo venv
	@echo inferno
	@echo inferno-broken

venv:
	@echo source ~/github/slexil2/py3105/bin/activate

inferno:
	python validXML.py ../testData/EAFv3.0.xsd \
                      ../testData/inferno/inferno-threeLines.eaf

inferno-broken:
	python validXML.py ../testData/EAFv3.0.xsd \
                      ../testData/inferno/inferno-threeLines-brokenTierTree.eaf

 
