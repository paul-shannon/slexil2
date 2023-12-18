HTML = 7-videoPlayer.html
HTML = 8-audioPlayer.html

default:
	@echo view
	@echo publish
	@echo viewRemote


publish:
	scp $(HTML) paulshannnon@pshannon.net:public_html/pshannon.net/demos/layout/index.html
	scp slexilNew.* paulshannnon@pshannon.net:public_html/pshannon.net/demos/layout/

viewRemote:
	open https://pshannon.net/demos/layout/

view:
	open $(HTML)
