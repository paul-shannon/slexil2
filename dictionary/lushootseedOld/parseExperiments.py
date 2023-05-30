from xml.etree import ElementTree as etree
xmlFilename = "LushDict.xml"
doc = etree.parse(xmlFilename)
root = doc.getroot()
len(root) # 2
for child in root:
    print(child.tag, child.attrib)
# {http://www.tei-c.org/ns/1.0}teiHeader {}
# {http://www.tei-c.org/ns/1.0}text {}

ns = {"tei": "http://www.tei-c.org/ns/1.0"}
text = root.findall("tei:text", ns)
text = root.findall("tei:text", ns)[0]
body = text.findall("tei:body", ns)[0]
len(body.findall("tei:entry", ns)) # 3599
entries = body.findall("tei:entry", ns)
len(entries)

entries = root.findall("tei:text/tei:body/tei:entry", ns)
len(entries)  # 3599
e = entries[3000]
len(e)
dir(e)
e.tag  # '{http://www.tei-c.org/ns/1.0}entry'

for child in e:
   print(child.tag, child.attrib)

[elem.tag for elem in e.iter()]
#   ['{http://www.tei-c.org/ns/1.0}entry',
#    '{http://www.tei-c.org/ns/1.0}form',
     '{http://www.tei-c.org/ns/1.0}orth',
#    '{http://www.tei-c.org/ns/1.0}ref']

for orth in e.iter('orth'):
	print(orth.attrib)

len(root.findall("text/body/entry")) # 0
len(root.findall("tei:text/tei:body/tei:entry", ns))  # 3599
len(root.findall("tei:text/tei:body/tei:entry/tei:form", ns))  # 8512
len(root.findall("tei:text/tei:body/tei:entry/tei:form/tei:orth", ns))  # 3599

  # orth instance 480, 1-based <form type="subst"><orth>   s^biáw </orth>

e = root.findall("tei:text/tei:body/tei:entry/tei:form/tei:orth", ns)[473]
e.text   # '   s^biáw '

e = root.findall("tei:text/tei:body/tei:entry", ns)[473]

for child in e.findall("tei:form"):
   print(child.tag, child.attrib, child.text)


orths = root.findall("tei:text/tei:body/tei:entry/tei:form/tei:orth", ns)

orthText =  [orth.text for orth in orths]
len(orthText)  # 3599
orthText[1:5]  # ['   ʔa: ', '   ʔa ', '   ʔaʔ ', '   ʔáʔəgʷàləb ']

[x for x in orthText[1:5] if '   ʔa ' in x]
# ['   ʔa ']
[x for x in orthText[1:5] if 'ʔa' in x]
# ['   ʔa: ', '   ʔa ', '   ʔaʔ ']

#------- try some xpath
len(doc.xpath("//*/entry"))

from lxml import etree
xmlFilename = "LushDict.xml"
tree = etree.parse(xmlFilename)
ns = {"tei": "http://www.tei-c.org/ns/1.0"}
r = tree.xpath("tei:text/tei:body/tei:entry/tei:form/tei:orth", namespaces=ns)
len(r) # 3599
r[473].text
#'   s^biáw '
tree.xpath("tei:text/tei:body/tei:entry/tei:form/tei:orth[text()=='   s^biáw ']"), namespaces=ns)
coyote = tree.xpath("//*[contains(text(), 's^biáw ')]")[0]
print(coyote.tag)
coyoteFormParent = tree.xpath("//*[contains(text(), 's^biáw ')]/./..")[0]
coyoteFormParent.getchildren()
# [<Element {http://www.tei-c.org/ns/1.0}orth at 0x1009e4e00>,
# <Element {http://www.tei-c.org/ns/1.0}gloss at 0x100a160c0>,
# <Element {http://www.tei-c.org/ns/1.0}gloss at 0x100a15f40>,
# <Element {http://www.tei-c.org/ns/1.0}bibl at 0x100a16100>,
# <Element {http://www.tei-c.org/ns/1.0}gloss at 0x100a16140>,
# <Element {http://www.tei-c.org/ns/1.0}gramGrp at 0x100a16200>]

# from this xml
# <entry>
#   <form type="subst">
#     <orth>   s^biáw </orth>
#     <gloss type="cat">   ns </gloss>
#     <gloss type="shape">   CVVC </gloss>
#     <bibl type="Hess">   35.6</bibl>
#     <gloss type="zoo">   *coyote </gloss>
#     <gramGrp>
#        <usg>   gʷa bəs^biaw tiʔəʔ ləcu(t)^cut. </usg>
#        <gloss>   But it was Coyote who was talking. <note type="cnslt">ML 14.227</note> </gloss>
#      </gramGrp>
#     </form>


print(coyoteFormParent).tag
for child in coyoteFormParent:
	print(child.tag)
	attributes = child.attrib.keys()
	for attr in attributes:
		print("%s: %s" % (attr, child.attrib[attr]))
	print(child.text)


#---------- now try to get all the forms in the entry. two for coyote

coyoteFormParent = tree.xpath("//*[contains(text(), 's^biáw ')]/./../../form")
coyoteFormParent = tree.xpath("//*[contains(text(), 's^biáw ')]/./../../form")
coyoteFormParent = tree.xpath("//*[contains(text(), 's^biáw ')]/./../..")

for kid in coyoteFormParent[0]:
	print(kid.tag)
	print(kid.text)
	for child in kid:
		print(child.tag)
		attributes = child.attrib.keys()
		for attr in attributes:
			print("%s: %s" % (attr, child.attrib[attr]))
		print(child.text)
	
	
