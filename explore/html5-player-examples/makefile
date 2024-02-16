#WAV = owlLivesThere-mono-16bit.wav
# WAV = owlLivesThere-mono-8k.wav
WAV = owlLivesThere-min-aLaw.wav
# WAV = daylight-restoration_V03.wav

default:
	@echo pubHtml
	@echo pubAudio
	@echo open
	@echo openLocal

pubHtml:
	scp safariAudioBug.html pshannon@206.12.95.4:www/bugs/index.html

pubAudio:
	scp $(WAV)  pshannon@206.12.95.4:www/bugs

open:
	open https://slexildata.artsrn.ualberta.ca/bugs

openLocal:
	open safariAudioBug.html
