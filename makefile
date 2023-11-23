default:
	@echo venv
	@echo install
	@echo install-via-setup
	@echo check
	@echo test
	@echo gitpip
	@echo wheel

venv:
	@echo source /Users/paul/github/slexil2/py3105slexil/bin/activate

install:
	pip install . --upgrade

install-via-setup:
	python setup.py install

wheel:
	pip wheel . --no-deps -w wheels

gitpip:
	pip install git+https://github.com/paul-shannon/slexilAsModuleAndPackage


check:
	cat ~/github/slexil2/py3105/lib/python3.10/site-packages/slexil/version.py
#	ls -lat ~/github/slexilAsModuleAndPackage/pySlexil/lib/python3.10/site-packages/slexil*
 
test:
	(cd tests; 	make test)
