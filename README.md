# slexil2

## sləxil: Software Linking ELAN XML to Illuminated Language ##

The name of this software builds upon the Lushootseed word for
daylight, <b><i>sləxil</b></i>, the focus of the origin story told by
Sauk-Suittale elder, Harry Moses: "How Daylight Was Stolen". Both Beck
(professionally) and Shannon (informally) have spent much time on this
story.

I am grateful to David for his patience over the years guiding me
through the intracies of this beautiful language, into the inner secrets of
ELAN XML, and as we knocked our heads against, and eventually
solved, many thorny parsing problems.

Our software is documented in the journal *Language Documentation and Conservation*
[here](https://scholarspace.manoa.hawaii.edu/bitstream/10125/24948/beck_shannon.pdf).
The main **SLEXIL** github repository
[here](https://github.com/davidjamesbeck/slexil).

## Background

Field linguists often transcribe and annotate stories using a complex and
flexible XML format called
[ELAN](https://en.wikipedia.org/wiki/ELAN_software).  slexil
transforms that xml, and accompanying audio, into a modestly
interactive webpage.  We use the first three lines of Dante's Inferno,
read by Roberto Benigni, to test and demonstrate the software.  The
live result can be seen and heard at [pshannon.net](https://pshannon.net/inferno/).

The source EAF XML looks like this:

![alt tag](https://github.com/paul-shannon/slexil2/blob/main/docs/inferno-eaf.png)


## Quick Start

### Install slexil

- You need a recent Python 3 installation.  I currently (May 2023) use
  version 3.10.5.
  
- This shell command will install slexil:

<pre>
pip install update git+https://github.com/paul-shannon/slexil2
</pre>
   
### Get short and simple examples files

- create and enter a temporary test directory
- if you have cloned this github repo, data files and script are in *demos/* directory.
- otherwise, you can download the three files you need like this:
    - curl -O https://raw.githubusercontent.com/paul-shannon/slexil2/main/testData/inferno/inferno-threeLines.eaf
    - curl -O https://raw.githubusercontent.com/paul-shannon/slexil2/main/testData/inferno/grammaticalTerms.txt
    - curl -O https://raw.githubusercontent.com/paul-shannon/slexil2/main/testData/inferno/tierGuide.yaml

Note that the audio for this small project is hosted independently, at a url written
into the eaf file.

### Generate an interactive HTML web page with a simple Python script

Here is the full text of the Python code.  The file is *demos/infernoDemo.py*

<pre>
from slexil.text import Text
from yattag import indent

elanXmlFilename = "inferno-threeLines.eaf"
tierGuideFile = "tierGuide.yaml"
grammaticalTermsFile = "grammaticalTerms.txt"
projectDirectory = "./"
fontSizeControls = False
startLine = None
endLine = None
kbFilename = None
linguisticsFilename = None

text = Text(elanXmlFilename,
			grammaticalTermsFile=grammaticalTermsFile,
			tierGuideFile=tierGuideFile,
			projectDirectory=projectDirectory,
			verbose=False,
			fontSizeControls = fontSizeControls,
			startLine = startLine,
			endLine = endLine,
			kbFilename = kbFilename,
			linguisticsFilename = linguisticsFilename)

htmlText = text.toHTML() 
filename = "inferno.html"
f = open(filename, "w")
f.write(indent(htmlText))
print("wrote %s" % filename)
</pre>

  

