import re
import sys
import tempfile

sys.path.append("../slexil")


from ijalLine import *
import importlib
import os
import pdb
import yaml
import pandas as pd
from text import *

#----------------------------------------------------------------------------------------------------
pd.set_option('display.width', 1000)
#----------------------------------------------------------------------------------------------------
def runTests():

    test_infernoReadAllLines()
    test_inferno_TimeCodes()
    test_inferno_line_1()
    test_extractAudioFileName()
    test_toHTML()

#----------------------------------------------------------------------------------------------------
def test_infernoReadAllLines():

    print("--- test_infernoReadAllLines")

    filename = "../testData/inferno/inferno-threeLines.eaf"
    xmlDoc = etree.parse(filename)
    lineCount = len(xmlDoc.findall("TIER/ANNOTATION/ALIGNABLE_ANNOTATION"))  # 9
    assert(lineCount==3)

    for lineNumber in range(lineCount):
        rootElement = xmlDoc.findall("TIER/ANNOTATION/ALIGNABLE_ANNOTATION")[lineNumber]
        allElements = findChildren(xmlDoc, rootElement)
        tmpTbl = buildTable(xmlDoc, allElements)
        assert(tmpTbl.shape == (4,13))

    tierGuideFile = "../testData/inferno/tierGuide.yaml"
    with open(tierGuideFile, 'r') as f:
        tierGuide = yaml.safe_load(f)
    assert(len(tierGuide) == 6)
    
    lines = []
    grammaticalTerms = ["hab", "past"]
    for i in range(lineCount):
        line = IjalLine(xmlDoc, i, tierGuide, grammaticalTerms)
        line.parse()
        lines.append(line)

    assert(len(lines) == 3)        

#----------------------------------------------------------------------------------------------------
def test_inferno_line_1():

    print("--- test_inferno_line_1")

    filename = "../testData/inferno/inferno-threeLines.eaf"
    xmlDoc = etree.parse(filename)
    tierGuideFile = "../testData/inferno/tierGuide.yaml"
    with open(tierGuideFile, 'r') as f:
        tierGuide = yaml.safe_load(f)
    grammaticalTerms = ["hab", "past"]
    line = IjalLine(xmlDoc, 0, tierGuide, grammaticalTerms)
    line.parse()

    assert(line.getTierCount() == 4)
    assert(isinstance(line.getTable(), pd.DataFrame))
    assert(line.getStartTime() == 0)
    assert(line.getEndTime() == 3093)
    assert(line.getSpokenText() == 'Nel mezzo del cammin di nostra vita')
    assert(line.getTranslation() == "‘Midway upon the journey of our life’")

    assert(line.extractMorphemes() == ['en=il', 'mezz–o', 'de=il', 'cammin–Ø', 'di', 'nostr–a', 'vit–a'])
    assert(line.extractMorphemeGlosses() ==
           ['in=DEF:MASC:SG', 'middle–MASC:SG', 'of=DEF:MASC:SG', 'journey–MASC:SG', 'of', 'our–FEM:SG', 'life–FEM'])

    line.calculateMorphemeSpacing()
    assert(line.getMorphemeSpacing() == [15, 15, 15, 16, 3, 11, 9])


#----------------------------------------------------------------------------------------------------
def test_toHTML(displayPage=False):

    print("--- test_toHTML")

    filename = "../testData/inferno/inferno-threeLines.eaf"
    xmlDoc = etree.parse(filename)
    tierGuideFile = "../testData/inferno/tierGuide.yaml"
    with open(tierGuideFile, 'r') as f:
        tierGuide = yaml.safe_load(f)
    grammaticalTerms = ["hab", "past"]
    line = IjalLine(xmlDoc, 0, tierGuide, grammaticalTerms)
    line.parse()

    htmlDoc = Doc()
    htmlDoc.asis('<!DOCTYPE html>')
    with htmlDoc.tag('html', lang="en"):
        with htmlDoc.tag('head'):
            htmlDoc.asis('<link rel="stylesheet" href="ijal.css">')
            with htmlDoc.tag('body'):
                line.toHTML(htmlDoc)

    htmlText = htmlDoc.getvalue()
    assert(len(re.findall('class="speech-tier"', htmlText)) == 1)
    assert(len(re.findall('class="morpheme-tier"', htmlText)) == 2)
    assert(len(re.findall('class="freeTranslation-tier"', htmlText)) == 1)
    assert(len(re.findall('class="morpheme-cell"', htmlText)) == 14)

    expected = '<div class="freeTranslation-tier">‘Midway upon the journey of our life’</div>'
    assert(len(re.findall(expected, htmlText)) == 1)

    if(displayPage):
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".html", dir=".")
        try:
            tmp.write(bytes(htmlText, "utf-8"))
            tmp.close()
        finally:
            os.system("open %s" % tmp.name)


#----------------------------------------------------------------------------------------------------
def test_inferno_TimeCodes():

    print("--- test_inferno_TimeCodes")

    filename = "../testData/inferno/inferno-threeLines.eaf"
    doc = etree.parse(filename)
    tierGuideFile = "../testData/inferno/tierGuide.yaml"
    with open(tierGuideFile, 'r') as f:
        tierGuide = yaml.safe_load(f)

    x3 = IjalLine(doc, 1, tierGuide)
    x3.parse()
    tbl = x3.getTable()
    assert(x3.getStartTime() == 3093)
    assert(x3.getEndTime() == 5624)

#----------------------------------------------------------------------------------------------------
def test_extractAudioFileName():

    print("--- test_extractAudioFileName")

    eaf_filename = "../testData/inferno/inferno-threeLines.eaf"
    assert(os.path.exists(eaf_filename))
    xmlDoc = etree.parse(eaf_filename)
    mediaDescriptors = xmlDoc.findall("HEADER/MEDIA_DESCRIPTOR")
    assert(len(mediaDescriptors) == 1)
    soundFileElement = mediaDescriptors[0]
    soundFileURI = soundFileElement.attrib["RELATIVE_MEDIA_URL"]
      # strip off the protocol
    soundFileName = soundFileURI.replace("file://./", "")
    directory = os.path.dirname(os.path.abspath(eaf_filename))
    fullPath = os.path.join(directory, soundFileName)
      # print("fullPath: %s" % fullPath)
    try:
        assert(os.path.exists(fullPath))
    except AssertionError as e:
        raise Exception(fullPath) from e


#----------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    runTests()
