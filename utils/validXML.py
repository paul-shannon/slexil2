import xmlschema
import os, sys
if(len(sys.argv) != 2):
	print("usage: python validXML.py <eaf filename>")
	sys.exit(1)
	
baseDir = "/Users/paul/github/slexil2/testData"
schemaFile = os.path.join(baseDir, "EAFv3.0.xsd")
os.path.isfile(schemaFile)
eaf = sys.argv[1]

result = xmlschema.validate(eaf, schemaFile)
if(result == None):
	print("valid")
else:
	print(result)
