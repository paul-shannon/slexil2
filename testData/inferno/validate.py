import xmlschema
import os
baseDir = "/Users/paul/github/slexil2/testData"
schemaFile = os.path.join(baseDir, "EAFv3.0.xsd")
os.path.isfile(schemaFile)
result = xmlschema.validate("inferno-threeLines.eaf", schemaFile)
print(result is None)

