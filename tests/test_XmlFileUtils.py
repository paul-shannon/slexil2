import base64
import os
import pdb
import pandas as pd
import magic
from slexil.xmlFileUtils import XmlFileUtils
#--------------------------------------------------------------------------------
# from
# https://stackoverflow.com/questions/66368326/plotly-dash-how-to-reproduce-content-output-of-dcc-upload-i-e-base64-encod
#
# dcc.Upload widget returns filename, contents and date.
# in this function we create, from plain text, the odd "contents" beast
# returned by dcc.Upload
# 
# contents is a base64 encoded string that contains the files contents
# [...] Property accept (string; optional): Allow specific types of
# files. See https://github.com/okonet/attr-accept for more information.
# Keep in mind that mime type determination is not reliable across
# platforms. CSV files, for example, are reported as text/plain
# under macOS but as application/vnd.ms-excel under Windows. In
# some cases there might not be a mime type set at all.

def createBase64EncodedStringFromEAFfile(fullPath):

   with open(fullPath, "rb") as file:
      decoded = file.read()
   content_bytes = base64.b64encode(decoded)
   content_string = content_bytes.decode("utf-8")
   mime = magic.Magic(mime=True)
   mime_type = mime.from_file(fullPath)
   content_type = "".join(["data:", mime_type, ";base64"])
   contents = "".join([content_type, ",", content_string])
   return(contents)

#--------------------------------------------------------------------------------
def test_ctor():

   print("--- test_ctor")
   fullPath = "../testData/inferno/inferno-threeLines.eaf"
   contents = createBase64EncodedStringFromEAFfile(fullPath)
   xmlFileUtils = XmlFileUtils(fullPath, "tmp", contents, verbose=True)
   
#--------------------------------------------------------------------------------
def test_saveBytesToFile():

   print("--- test_saveBytesToFile")

   fullPath = "../testData/inferno/inferno-threeLines.eaf"
   contents = createBase64EncodedStringFromEAFfile(fullPath)
   projectDirectory = "tmp"
   reconstitutedFilename = os.path.join(projectDirectory,
                                        os.path.basename(fullPath))
   if(os.path.exists(reconstitutedFilename)):
      print("   (removing pre-existing %s)" % reconstitutedFilename)
      os.remove(reconstitutedFilename)

   utils = XmlFileUtils(fullPath, projectDirectory, contents, verbose=True)
   utils.saveBytesToFile()
   localFile = utils.getLocalFilename()
   assert(localFile == reconstitutedFilename)
   assert(os.path.exists(reconstitutedFilename))

   filesizeOld = os.path.getsize(fullPath)
   filesizeNew = os.path.getsize(reconstitutedFilename)
   assert(filesizeNew == filesizeOld)
   
#--------------------------------------------------------------------------------
def test_validateXML():

   print("--- test_validateXML")

   fullPath = "../testData/inferno/inferno-threeLines.eaf"
   contents = createBase64EncodedStringFromEAFfile(fullPath)
   projectDirectory = "tmp"
   utils = XmlFileUtils(fullPath, projectDirectory, contents, verbose=True)
   localFile = utils.saveBytesToFile()
   assert(localFile == 'tmp/inferno-threeLines.eaf')

   result = utils.validElanXML()
   assert(result["valid"] == True)
   assert(result["details"] == None)

     #--------------------------------------------------------
     # now some ill-formed files.  first, this python script
     #--------------------------------------------------------
   fullPath = "test_xmlFileUtils.py" 
   contents = createBase64EncodedStringFromEAFfile(fullPath)
   projectDirectory = "tmp"
   utils = XmlFileUtils(fullPath, projectDirectory, contents, verbose=True)
   utils.saveBytesToFile()

   result = utils.validElanXML()
   expectedDetails = "invalid xml file test_xmlFileUtils.py : syntax error: line 1, column 0"
   assert(result["valid"] == False)
   assert(result["details"] == expectedDetails)

     #----------------------------------------------------------
     # a random xml file, no relation to the EAFv3.0.xsd schema
     #----------------------------------------------------------
   fullPath = "../testData/invalidEafFiles/randomBad.xml"
   print("    %s" % fullPath)
   contents = createBase64EncodedStringFromEAFfile(fullPath)
   projectDirectory = "tmp"
   utils = XmlFileUtils(fullPath, projectDirectory, contents, verbose=True)
   utils.saveBytesToFile()
   result = utils.validElanXML()
   assert(result["valid"] == False)
     # exception details includes memory address after this substring
     # don't check past this point
   expectedDetailsBeginsWith = 'invalid xml file randomBad.xml : failed validating <Element \'customers\''
   assert(result["details"].find(expectedDetailsBeginsWith) >= 0)

     #----------------------------------------------------------
     # one misspelled tag in an otherwise valid document
     #----------------------------------------------------------
   fullPath = "../testData/invalidEafFiles/inferno-misspelledTag.eaf"
   print("    %s" % fullPath)
   contents = createBase64EncodedStringFromEAFfile(fullPath)
   projectDirectory = "tmp"
   utils = XmlFileUtils(fullPath, projectDirectory, contents, verbose=True)
   utils.saveBytesToFile()
   result = utils.validElanXML()
   assert(result["valid"] == False)
      # test for a bunch of expected substrings: awkward to
      # eliminate the memory reference, awkward to test against
      # use the full long string
   x = result["details"]
   assert(len(x) > 3000)
   assert(x.find("invalid xml file inferno-misspelledTag.eaf") >= 0)
   assert(x.find("failed validating <Element \'ANNOTATION_DOCUMENT\'") >= 0)
   assert(x.find("Reason: Unexpected child with tag \'TIME_ORDERxxx\'") >= 0)

     #----------------------------------------------------------
     # the eaf schema requirest that all tiers have a linguistic
     # type. and type names can be used, but ours are often:
     #    default_lt
     #    morpheme
     #    morpheme-gloss
     #    translation
     # in this test, the LINGUISTIC_TYPE_ID should be "translation"
     # but I have upper-cased the leading letter:  Translation
     #----------------------------------------------------------
   fullPath = "../testData/invalidEafFiles/inferno-misnamedTierType.eaf"
   print("    %s" % fullPath)
   contents = createBase64EncodedStringFromEAFfile(fullPath)
   projectDirectory = "tmp"
   utils = XmlFileUtils(fullPath, projectDirectory, contents, verbose=True)
   utils.saveBytesToFile()
   result = utils.validElanXML()
   assert(result["valid"] == False)
   x = result["details"]
   assert(x.find("invalid xml file inferno-misnamedTierType.eaf") >= 0)
   expected = "Reason: value (\'translation\',) not found for XsdKey"
   assert(x.find(expected) >= 0)

     #----------------------------------------------------------
     # eaf tiers are linked via parent-child relations
     # we often have 4 tiers, where the first is a time-aligned
     # speech tier.  in this intentionally flawed file, the
     # morphemes tier is the first child of the italianSpeech tier
     # but gives its PARENT_REF as "italianSpEEch".
     #----------------------------------------------------------

   fullPath = "../testData/invalidEafFiles/inferno-misnamedParentRef.eaf"
   print("    %s" % fullPath)
   contents = createBase64EncodedStringFromEAFfile(fullPath)
   projectDirectory = "tmp"
   utils = XmlFileUtils(fullPath, projectDirectory, contents, verbose=True)
   utils.saveBytesToFile()
   result = utils.validElanXML()
   assert(result["valid"] == False)
   x = result["details"]
   assert(x.find("invalid xml file inferno-misnamedParentRef.eaf") >= 0)
   assert(x.find("Reason: value (\'italianSpEEch\',) not found") >= 0)
   
#--------------------------------------------------------------------------------
def runTests():

    test_ctor()
    test_saveBytesToFile()
    test_validateXML()

#--------------------------------------------------------------------------------
if __name__ == "__main__":
    runTests()

