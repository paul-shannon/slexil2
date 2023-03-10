default:
	@echo publish-html, publish-all, open-local, open-remote, byte-range-test, header

publish-html:
	scp *.html paulshannnon@pshannon.net:public_html/pshannon.net/tests/

publish-all:
	scp * paulshannnon@pshannon.net:public_html/pshannon.net/tests/

open-local:
	open playSegment.html


open-remote:
	open https://pshannon.net/tests/playSegment.html

byte-range-test:
	curl --range 0-99 https://pshannon.net/tests/1RuthNora2Wide.m4v -o junk
	curl -L -H --range 0-99 https://pshannon.net/tests/1RuthNora2Wide.m4v -o junk
header:
	curl -X HEAD -i https://pshannon.net/tests/1RuthNora2Wide.m4v
