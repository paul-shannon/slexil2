default:
	@echo targets: venv install install-via-setup check test gitpip

venv:
	@echo source ~/github/slexil2/py3105/bin/activate

install:
	pip install . --upgrade

install-via-setup:
	python setup.py install

gitpip:
	pip install git+https://github.com/paul-shannon/slexilAsModuleAndPackage


check:
	cat ~/github/slexil2/py3105/lib/python3.10/site-packages/slexil/version.py
#	ls -lat ~/github/slexilAsModuleAndPackage/pySlexil/lib/python3.10/site-packages/slexil*
 
test:
	(cd tests; 	make test)
