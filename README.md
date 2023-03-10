# slexil2

This repo is a work in progress, a modest refactoring
of the core original
[SLEXIL](https://github.com/davidjamesbeck/slexil) software, which was a collaborative
effort between me and linguist Davd Beck.  I have undertaken this
refactoing to remind myself of sound coding and project structuring practices in
Python, after several years in which I have work primarily in <b><i>R</i></b>.
I will be adding more revisions and additions soon.

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



