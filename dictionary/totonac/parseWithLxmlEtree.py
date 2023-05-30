from lxml import etree
xmlFilename = "unt-formatted.xml"
tree = etree.parse(xmlFilename)
root = tree.getroot()
print("root child count: %d" % len(root.getchildren()))  # 35910

#root = objectify.Element("root")
#b = objectify.SubElement(root, "b")
lexemes = tree.xpath("//FieldBook/Lex")
print("lexeme count: %d" % len(lexemes))

texts = tree.xpath("//FieldBook/Text")
print("text count: %d" % len(texts)) 

dsets = tree.xpath("//FieldBook/Dset")
len(dsets)  # 224

exs = tree.xpath("//FieldBook/Ex")
len(exs)  # 15399

speakers = tree.xpath("//FieldBook/Speaker")
print("speaker count: %d" % len(speakers))

rschrs = tree.xpath("//FieldBook/Rschr")
print("researcher count: %d" % len(rschrs))  # 10

abbreviations = tree.xpath("//FieldBook/Abbreviations")
len(abbreviations)  # 1

abbrs = tree.xpath("//FieldBook/Abbreviations/Abbr")
len(abbrs)  # 86

medias = tree.xpath("//FieldBook/Media")
len(medias)  # 10592 ?

orthographys = tree.xpath("//FieldBook/Orthography")
print("orthography count: %d" % len(orthographys))  # 1

# FieldBook apparently has many optional, and some required attributes:

#  <xsd:attribute name="Dbase" type="xsd:string" use="required"/>
# <xsd:attribute name="Language" type="xsd:string" use="required"/>
# <xsd:attribute name="Family" type="xsd:string" use="optional"/>
# <xsd:attribute name="Population" type="xsd:string" use="optional"/>
# <xsd:attribute name="Location" type="xsd:string" use="optional"/>
# <xsd:attribute name="ISO" type="xsd:string" use="optional"/>
# <xsd:attribute name="Font" type="xsd:anyURI" use="optional"/>
# <xsd:attribute name="L1Choice" type="xsd:language" use="required"/>
# <xsd:attribute name="L2Choice" type="xsd:language" use="optional"/>
# <xsd:attribute name="LastCard" type="xsd:IDREF" use="required"/>
# <xsd:attribute name="LastLex" type="xsd:IDREF" use="required"/>
# <xsd:attribute name="LastEx" type="xsd:IDREF" use="required"/>
# <xsd:attribute name="LastText" type="xsd:IDREF" use="required"/>
# <xsd:attribute name="LastDset" type="xsd:IDREF" use="required"/>
# <xsd:attribute name="LastSpeaker" type="xsd:IDREF" use="optional"/>
# <xsd:attribute name="LastRschr" type="xsd:IDREF" use="optional"/>
# <xsd:attribute name="DefaultSpeaker" type="xsd:IDREF" use="optional"/>
# <xsd:attribute name="DefaultRschr" type="xsd:IDREF" use="optional"/>
# <xsd:attribute name="MediaFolder" type="xsd:string" use="optional"/>
# <xsd:attribute name="lAuto" type="xsd:string" use="required"/>
# <xsd:attribute name="eParse" type="xsd:string" use="required"/>
# <xsd:attribute name="Orth" type="xsd:string" use="optional"/>
# <xsd:attribute name="SortKey" type="xsd:string" use="optional"/>
# <xsd:attribute name="Tiers" type="xsd:string" use="optional"/>
# <xsd:attribute name="noText" type="xsd:string" use="optional"/>
# <xsd:attribute name="noEG" type="xsd:string" use="optional"/>
# <xsd:attribute name="noDefaultSort" type="xsd:string" use="optional"/>


lexemes[0].getchildren()
lexeme = lexemes[0]
tags = [kid.tag for kid in lexeme.getchildren()]
print(tags)
# ['Orth', 'POS', 'IPA', 'PhKy', 'Def', 'Comments']

start = 200
end = 300
i = start
for lexeme in lexemes[start:end]:
	print("--- lexeme %3d" % i)
	i = i + 1
	tags = [kid.tag for kid in lexeme.getchildren()]
	uniqueTags = {}
	for tag in tags:
		uniqueTags[tag] = 1
	tags = list(uniqueTags.keys())
	for tag in tags:
	   elements = lexeme.xpath(tag)
	   for element in elements:
		   if(tag == "Def"):
			   print("    Def:")
			   #defSubElements = lexeme.xpath("Def")[0].getchildren()
			   defSubElements = element.getchildren()
			   #pdb.set_trace()
			   for subElement in defSubElements:
				   subTag = subElement.tag
				   print("       %s: %s" %(subTag, subElement.text))
		   else:
			   print("    %s: %s" % (tag, element.text))

