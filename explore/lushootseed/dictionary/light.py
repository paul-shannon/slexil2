from lxml import etree
import xmltodict
import pprint
pp = pprint.PrettyPrinter(indent=2)

    #-------------------------------
    # get the ləx̌ entry using xpath
    #-------------------------------
xmlFilename = "LushDict.xml"
ns = {"tei": "http://www.tei-c.org/ns/1.0",
      "re": "http://exslt.org/regular-expressions"}
tree = etree.parse(xmlFilename)
target = 'ləx̌'

  # get the entry grandparent where the entry/form/orth text exactly matches the target

query = "tei:text/tei:body/tei:entry/tei:form/tei:orth[text()='%s']/parent::*/parent::*" % target
targetEntry = tree.xpath(query, namespaces=ns)[0]

targetText = etree.tostring(targetEntry)
targetObject = xmltodict.parse(targetText)
pp.pprint(targetObject)

    #------------------------------------
    # get the ləx̌ entry using xmltodict
    #------------------------------------
xmlFilename = "LushDict.xml"
text = open(xmlFilename).read()
obj = xmltodict.parse(text)
obj["TEI"]["text"]["body"]["entry"][0]["form"]["orth"]   # 'ʔa:'


