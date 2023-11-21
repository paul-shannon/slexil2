import xmlschema
import os, sys
if(len(sys.argv) != 3):
	print("usage: python validXML.py <xsd filename> <xml filename>")
	sys.exit(1)
	
baseDir = "/Users/paul/github/slexil2/testData"
schemaFile = sys.argv[1]
assert(os.path.isfile(schemaFile))
xml = sys.argv[2]
assert(os.path.isfile(xml))

result = xmlschema.validate(xml, schemaFile)
if(result == None):
	print("valid")
else:
	print(result)
