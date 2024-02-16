default:
	@echo venv
	@echo view
	@echo publish
	@echo viewRemote
	@echo menu
	@echo openMenu

venv:
	@echo source /Users/paul/github/slexil2/py3105slexil/bin/activate


publish:
	scp $(HTML) paulshannnon@pshannon.net:public_html/pshannon.net/demos/layout/index.html
	scp *.js paulshannnon@pshannon.net:public_html/pshannon.net/demos/layout/
	scp *.css paulshannnon@pshannon.net:public_html/pshannon.net/demos/layout/

viewRemote:
	open https://pshannon.net/demos/layout/

view:
	open $(HTML)

menu:
	python test_DropDownMenu.py

openMenu:
	open test_DropDownMenu.html
