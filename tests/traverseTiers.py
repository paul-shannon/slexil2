from lxml import etree
import pdb
eafFiles = open("../testData/eafFileList.txt").read().split('\n')
if(eafFiles[-1] == ""):
	del eafFiles[-1]

xmlFilename = eafFiles[0]
doc = etree.parse(xmlFilename)

# find a time aligned tier.  trace its children
rowNumber = 1
x = doc.findall('TIER/ANNOTATION/ALIGNABLE_ANNOTATION')[rowNumber]
x.attrib["ANNOTATION_ID"]

visited = set()
def dfs(visited, doc, tierID):
	if(tierID not in visited):
		print(tierID)
		visited.add(tierID)
		pattern = "TIER/ANNOTATION/REF_ANNOTATION[@ANNOTATION_REF='%s']" % tierID
		kidElements = doc.findall(pattern)
		kids = [kid.attrib["ANNOTATION_ID"] for kid in kidElements]
		for kid in kids:
			dfs(visited, doc, kid)
	

pattern = "TIER/ANNOTATION/REF_ANNOTATION[@ANNOTATION_REF='%s']" % alignedID
