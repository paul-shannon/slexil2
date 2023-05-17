from slexil import ijalLine as ijalLine
from slexil import text as text 

#import re
#import sys

#sys.path.append("../src/slexil")
#import audioExtractor
#from ijalLine import *
#import importlib
#import os
#import pdb
#import yaml
import pandas as pd
# import pickle
from text import *

# ----------------------------------------------------------------------------------------------------
pd.set_option('display.width', 1000)


# ----------------------------------------------------------------------------------------------------
def runTests():
    test_buildTable()
    test_getStartStopTimes()
    test_loco_line_3()    # each morpheme and gloss are separate xml tier elements
    test_extractAudio()   # only works when LARGE AYAMT files is present
    test_loco_toHTML(False, sampleOfLinesOnly=True)
    test_AYAMT_line_6() # morphemes and glosses are each packed into in a single tab-delimited tier element
    test_AYAMT_toHTML(False)
    test_featherSnake_toHTML(False)
    test_Jagpossum_TimeCodes() #this file is weird, it appears to have no alignable annotation types
    test_inferno_TimeCodes()
    test_Ghost_TimeCodes()
    test_aktzini_TimeCodes() #this file is weird, it appears to have no alignable annotation types
    test_praying_toHTML(displayPage=False)
    test_inferno()
    test_Jagpossum(displayPage=False)
    test_infernoDeep()
    test_aktzini_toHTML()



# ----------------------------------------------------------------------------------------------------
def test_infernoDeep():
    print("--- test_infernoDeep")

    filename = "../testTextPyData/Inferno/infernoDeep.eaf"
    xmlDoc = etree.parse(filename)
    lineCount = len(xmlDoc.findall("TIER/ANNOTATION/ALIGNABLE_ANNOTATION"))  # 9
    # print(lineCount)

    for lineNumber in range(lineCount):
        rootElement = xmlDoc.findall("TIER/ANNOTATION/ALIGNABLE_ANNOTATION")[lineNumber]
        allElements = findChildren(xmlDoc, rootElement)
        tmpTbl = buildTable(xmlDoc, allElements)
        # print("---- line %d" % lineNumber)
        # print(tmpTbl)

    tierGuideFile = "../testTextPyData/Inferno/tierGuide.yaml"
    with open(tierGuideFile, 'r') as f:
        tierGuide = yaml.safe_load(f)

    lines = []
    grammaticalTerms = ["hab", "past"]
    for i in range(lineCount):
        line = IjalLine(xmlDoc, i, tierGuide, grammaticalTerms)


# ----------------------------------------------------------------------------------------------------
def test_inferno():
    print("--- test_inferno")

    filename = "../testTextPyData/Inferno/inferno-threeLines.eaf"
    xmlDoc = etree.parse(filename)
    lineCount = len(xmlDoc.findall("TIER/ANNOTATION/ALIGNABLE_ANNOTATION"))  # 9
    # print(lineCount)

    for lineNumber in range(lineCount):
        rootElement = xmlDoc.findall("TIER/ANNOTATION/ALIGNABLE_ANNOTATION")[lineNumber]
        allElements = findChildren(xmlDoc, rootElement)
        tmpTbl = buildTable(xmlDoc, allElements)
        # print("---- line %d" % lineNumber)
        # print(tmpTbl)

    tierGuideFile = "../testTextPyData/Inferno/tierGuide.yaml"
    with open(tierGuideFile, 'r') as f:
        tierGuide = yaml.safe_load(f)

    lines = []
    grammaticalTerms = ["hab", "past"]
    for i in range(lineCount):
        line = IjalLine(xmlDoc, i, tierGuide, grammaticalTerms)


# ----------------------------------------------------------------------------------------------------
def test_Jagpossum(displayPage):
    print("--- test_Jagpossum")

    filename = "../testTextPyData/Jagpossum/Jagpossum.eaf"
    xmlDoc = etree.parse(filename)
    lineCount = len(xmlDoc.findall("TIER/ANNOTATION/ALIGNABLE_ANNOTATION"))  # 9
    # print(lineCount)

    for lineNumber in range(lineCount):
        rootElement = xmlDoc.findall("TIER/ANNOTATION/ALIGNABLE_ANNOTATION")[lineNumber]
        allElements = findChildren(xmlDoc, rootElement)
        tmpTbl = buildTable(xmlDoc, allElements)
        # print("---- line %d" % lineNumber)
        # print(tmpTbl)

    tierGuideFile = "../testTextPyData/Jagpossum/tierGuide.yaml"
    with open(tierGuideFile, 'r') as f:
        tierGuide = yaml.safe_load(f)

    lines = []
    grammaticalTerms = ["hab", "past"]
    for i in range(lineCount):
        line = IjalLine(xmlDoc, i, tierGuide, grammaticalTerms)
    # print(line.tblRaw)

    if (displayPage):
        audioFilename = "../testTextPyData/Jagpossum/Jagpossum.wav"
        grammaticalTermsFile = "../testTextPyData/Jagpossum/abbreviations.txt"
        projectDirectory = "../testTextPyData/Jagpossum"
        text = Text(filename,
                    audioFilename,
                    grammaticalTermsFile,
                    tierGuideFile,
                    projectDirectory)

        htmlText = text.toHTML()

        filename = "../testTextPyData/Jagpossum/Jagpossum.html"
        f = open(filename, "w")
        f.write(indent(htmlText))
        f.close()
        os.system("open %s" % filename)


# ----------------------------------------------------------------------------------------------------
def test_praying_toHTML(displayPage=False):
    print("--- test_praying_toHTML")

    filename = "../testData/praying/praying.eaf"
    xmlDoc = etree.parse(filename)
    lineCount = len(xmlDoc.findall("TIER/ANNOTATION/ALIGNABLE_ANNOTATION"))  # 9
    # print(lineCount)

    for lineNumber in range(lineCount):
        rootElement = xmlDoc.findall("TIER/ANNOTATION/ALIGNABLE_ANNOTATION")[lineNumber]
        allElements = findChildren(xmlDoc, rootElement)
        tmpTbl = buildTable(xmlDoc, allElements)
        # print("---- line %d" % lineNumber)
        # print(tmpTbl)

    tierGuideFile = "../testData/praying/tierGuide.yaml"
    with open(tierGuideFile, 'r') as f:
        tierGuide = yaml.safe_load(f)

    lines = []
    grammaticalTerms = ["hab", "past"]
    for i in range(lineCount):
        line = IjalLine(xmlDoc, i, tierGuide, grammaticalTerms)
        if (line.tierCount < 4):
            print("skipping line %d, tierCount %d" % (i, line.tierCount))
        else:
            line.parse()
            lines.append(line)

    # print("parsed %d/%d complete lines" % (len(lines), lineCount))

    htmlDoc = Doc()

    htmlDoc.asis('<!DOCTYPE html>')
    with htmlDoc.tag('html', lang="en"):
        with htmlDoc.tag('head'):
            htmlDoc.asis('<meta charset="UTF-8">')
            htmlDoc.asis('<link rel="stylesheet" href="ijal.css">')
            htmlDoc.asis('<script src="ijalUtils.js"></script>')
            with htmlDoc.tag('body'):
                for line in lines:
                    line.toHTML(htmlDoc)

    htmlText = htmlDoc.getvalue()

    if (displayPage):
        filename = "tmp.html"
        f = open(filename, "w")
        f.write(indent(htmlText))
        f.close()
        os.system("open %s" % filename)


# ----------------------------------------------------------------------------------------------------
def test_aktzini_TimeCodes():
    print("--- test_aktzini_TimeCodes")

    filename = "../testData/aktzini/18-06-03Aktzini-GA.eaf"
    doc = etree.parse(filename)
    tierGuideFile = "../testData/aktzini/tierGuide.yaml"
    with open(tierGuideFile, 'r') as f:
        tierGuide = yaml.safe_load(f)

    x3 = IjalLine(doc, 1, tierGuide)
    x3.parse()
    tbl = x3.getTable()
    startTime = x3.getStartTime()
    endTime = x3.getEndTime()
    print(startTime, endTime)


# ----------------------------------------------------------------------------------------------------
def test_Ghost_TimeCodes():
    print("--- test_Ghost_TimeCodes")

    filename = "../testTextPyData/GhostInWagon/GhostInWagon.eaf"
    doc = etree.parse(filename)
    tierGuideFile = "../testTextPyData/GhostInWagon/tierGuide.yaml"
    with open(tierGuideFile, 'r') as f:
        tierGuide = yaml.safe_load(f)

    x3 = IjalLine(doc, 1, tierGuide)
    x3.parse()
    tbl = x3.getTable()
    startTime = x3.getStartTime()
    endTime = x3.getEndTime()
    print(startTime, endTime)


# ----------------------------------------------------------------------------------------------------
def test_inferno_TimeCodes():
    print("--- test_inferno_TimeCodes")

    filename = "../testTextPyData/Inferno/inferno-threeLines.eaf"
    doc = etree.parse(filename)
    tierGuideFile = "../testTextPyData/Inferno/tierGuide.yaml"
    with open(tierGuideFile, 'r') as f:
        tierGuide = yaml.safe_load(f)

    x3 = IjalLine(doc, 1, tierGuide)
    x3.parse()
    tbl = x3.getTable()
    startTime = x3.getStartTime()
    endTime = x3.getEndTime()
    print(startTime, endTime)


# ----------------------------------------------------------------------------------------------------
def test_Jagpossum_TimeCodes():
    print("--- test_Jagpossum_TimeCodes")

    filename = "../testTextPyData/Jagpossum/Jagpossum.eaf"
    doc = etree.parse(filename)
    tierGuideFile = "../testTextPyData/Jagpossum/tierGuide.yaml"
    with open(tierGuideFile, 'r') as f:
        tierGuide = yaml.safe_load(f)

    x3 = IjalLine(doc, 1, tierGuide)
    x3.parse()
    tbl = x3.getTable()
    startTime = x3.getStartTime()
    endTime = x3.getEndTime()
    print(startTime, endTime)
    # assert (startTime == 8850.0)
    # assert (endTime == 10570.0)


# ----------------------------------------------------------------------------------------------------
def test_buildTable():
    print("--- test_buildTable")

    filename = "../testData/loco/loco.eaf"
    doc = etree.parse(filename)
    tierGuideFile = "../testData/loco/tierGuide.yaml"
    with open(tierGuideFile, 'r') as f:
        tierGuide = yaml.safe_load(f)

    x3 = IjalLine(doc, 3, tierGuide, '1')
    x3.parse()
    tbl = x3.getTable()
    assert (tbl.shape == (10, 14))
    assert (tbl.columns.tolist() == ['ANNOTATION_ID', 'LINGUISTIC_TYPE_REF', 'START', 'END',
                                     'TEXT', 'ANNOTATION_REF', 'TIME_SLOT_REF1', 'TIME_SLOT_REF2',
                                     'PARENT_REF', 'TIER_ID', 'TEXT_LENGTH', 'HAS_TABS', 'HAS_SPACES',
                                     'category'])

    assert (tbl['category'].tolist() == ['speech', 'translation', 'morpheme', 'morphemeGloss',
                                         'morpheme', 'morphemeGloss', 'morpheme', 'morphemeGloss',
                                         'morpheme', 'morphemeGloss'])

    assert (tbl['ANNOTATION_ID'].tolist() == ['a26', 'a969', 'a20533', 'a22390', 'a20534', 'a22391',
                                              'a20535', 'a22392', 'a20536', 'a22393'])

    assert (tbl['TIER_ID'].tolist() == ['Orthographic represntation', 'English translation', 'morpheme', 'gloss',
                                        'morpheme', 'gloss', 'morpheme', 'gloss', 'morpheme', 'gloss'])

    # first element is empty, confusingly parsed out of xml as math.nan.  don't test for it - too peculiar
    assert (tbl['ANNOTATION_REF'].tolist()[1:] == ['a26', 'a12134', 'a12134', 'a12135', 'a12135', 'a12136',
                                                   'a12136', 'a12137', 'a12137'])


# ----------------------------------------------------------------------------------------------------
def test_getStartStopTimes():
    print("--- test_getStartStopTimes")

    filename = "../testData/loco/loco.eaf"
    doc = etree.parse(filename)
    tierGuideFile = "../testData/loco/tierGuide.yaml"
    with open(tierGuideFile, 'r') as f:
        tierGuide = yaml.safe_load(f)

    x3 = IjalLine(doc, 3, tierGuide)  # ,audioData='a,b,c')
    x3.parse()
    tbl = x3.getTable()
    startTime = x3.getStartTime()
    endTime = x3.getEndTime()
    assert (startTime == 8850.0)
    assert (endTime == 10570.0)


# ----------------------------------------------------------------------------------------------------
def test_loco_line_3():
    """
      used for early exploration and development of the IjalLine class
    """
    print("--- test_loco_line_3")

    filename = "../testData/loco/loco.eaf"
    doc = etree.parse(filename)
    tierGuideFile = "../testData/loco/tierGuide.yaml"
    with open(tierGuideFile, 'r') as f:
        tierGuide = yaml.safe_load(f)

    grammaticalTerms = ['fem', 'poss', 'indf']
    x3 = IjalLine(doc, 3, tierGuide, grammaticalTerms)
    x3.parse()

    assert (x3.speechRow == 0)
    assert (x3.translationRow == 1)
    assert (x3.morphemeRows == [2, 4, 6, 8])
    assert (x3.morphemeGlossRows == [3, 5, 7, 9])

    assert (x3.getSpokenText() == 'th@s@, @b@ h@y@r@ k@b@.')
    try:
        assert (x3.getTranslation() == "‘[@] ch@ld, @ w@m@n @s w@ll.’")
    except AssertionError as e:
        raise Exception(x3.getTranslation()) from e
    assert (x3.getMorphemes() == ['tʰ–ɨs@', '@b@', 'h@j@r@', 'k@b@'])
    assert (x3.getMorphemeGlosses() == ['3F@M.P@SS–ch@ld', '@NDF', 'w@m@n', 't@@'])
    assert (x3.getMorphemeSpacing() == [16, 5, 7, 5])  # word width + 1


# ----------------------------------------------------------------------------------------------------
def test_extractAudio():
    print("--- test_extractAudio")
    filename = "../testData/AYAMT/AYAMT.eaf"
    assert (os.path.exists(filename))
    xmlDoc = etree.parse(filename)
    mediaDescriptors = xmlDoc.findall("HEADER/MEDIA_DESCRIPTOR")
    assert (len(mediaDescriptors) == 1)
    soundFileElement = mediaDescriptors[0]
    soundFileURI = soundFileElement.attrib["RELATIVE_MEDIA_URL"]
    directory = os.path.dirname(os.path.abspath(filename))
    fullPath = os.path.join(directory, soundFileURI)
    print("fullPath: %s" % fullPath)
    try:
        assert (os.path.exists(fullPath))
    except AssertionError as e:
        raise Exception(fullPath) from e


# ----------------------------------------------------------------------------------------------------
def test_loco_toHTML(displayPage=False, sampleOfLinesOnly=True):
    print("--- test_loco_toHTML")

    filename = "../testData/loco/loco.eaf"
    xmlDoc = etree.parse(filename)
    lineCount = len(xmlDoc.findall("TIER/ANNOTATION/ALIGNABLE_ANNOTATION"))  # 41

    tierGuideFile = "../testData/loco/tierGuide.yaml"
    with open(tierGuideFile, 'r') as f:
        tierGuide = yaml.safe_load(f)

    lines = []

    if (sampleOfLinesOnly):
        maxLines = 10
    else:
        maxLines = lineCount

    grammarTerms = ["hab", "past"]
    for i in range(maxLines):
        line = IjalLine(xmlDoc, i, tierGuide, grammarTerms)
        if (line.tierCount < 4):
            print("skipping line %d, tierCount %d" % (i, line.tierCount))
        else:
            # print("parsing line %d" % i)
            line.parse()
            lines.append(line)

    # print("parsed %d/%d complete lines" % (len(lines), lineCount))

    htmlDoc = Doc()

    htmlDoc.asis('<!DOCTYPE html>')
    with htmlDoc.tag('html', lang="en"):
        with htmlDoc.tag('head'):
            htmlDoc.asis('<meta charset="UTF-8">')
            htmlDoc.asis('<link rel="stylesheet" href="ijal.css">')
            htmlDoc.asis('<script src="ijalUtils.js"></script>')
            with htmlDoc.tag('body'):
                for line in lines:
                    line.toHTML(htmlDoc)

    htmlText = htmlDoc.getvalue()
    # displayPage = True
    if (displayPage):
        filename = "tmp.html"
        f = open(filename, "w")
        f.write(indent(htmlText))
        f.close()
        os.system("open %s" % filename)


# ----------------------------------------------------------------------------------------------------
def test_AYAMT_line_6():
    """
      used for early exploration and development of the IjalLine class
    """
    print("--- test_AYAMT_line_6")

    filename = "../testData/AYAMT/AYAMT.eaf"
    doc = etree.parse(filename)

    tierGuideFile = "../testData/AYAMT/tierGuide.yaml"
    with open(tierGuideFile, 'r') as f:
        tierGuide = yaml.safe_load(f)

    grammaticalTermsFile = "../testData/AYAMT/grammaticalTerms.txt"
    grammaticalTerms = open(grammaticalTermsFile).read().split("\n")
    assert ("M@@TH" in grammaticalTerms)

    x6 = IjalLine(doc, 6, tierGuide, grammaticalTerms)
    x6.parse()

    assert (x6.speechRow == 0)
    assert (x6.translationRow == 2)
    assert (x6.morphemeRows == [1])
    assert (x6.morphemeGlossRows == [3])

    assert (x6.getSpokenText() == 'K@ j@jn m@kp@t. M@knd@j mb@ʹ @@ m@knhw@j m@j.')
    assert (x6.getTranslation() == '‘H@ l@ft. H@ w@nt l@@k@ng f@r s@m@@n@ wh@ c@@ld sh@@t l@@d@r.’')
    try:
        assert (x6.getMorphemes() == ['q@@', 'h@M', 'm@k=p@t', 'm@k=nǝh', 'm@ʔ', 'ʔ@ː', 'm@k=ŋ•w@h', 'm@s'])
    except AssertionError as e:
        raise Exception(x6.getMorphemes()) from e
    assert (x6.getMorphemeGlosses() == ['th@t', 'th@r@', 'CMP=@x@t', 'CMP=g@', 'D@ST', 'wh@', 'CMP=M@@TH•cry', 'm@r@'])
    assert (x6.getMorphemeSpacing() == [5, 6, 9, 8, 5, 4, 14, 5])  # word width + 1

    htmlDoc = Doc()
    x6.toHTML(htmlDoc)
    htmlText = htmlDoc.getvalue()
    assert (htmlText.count("grammatical-term") == 5)
    # print(indent(htmlText))


# ----------------------------------------------------------------------------------------------------
def test_AYAMT_line_0():
    """
      neither morphemes nor glosses in this line: just spanish and english
    """
    print("--- test_AYAMT_line_0")

    filename = "../testData/AYAMT/AYAMT.eaf"
    doc = etree.parse(filename)

    tierGuideFile = "../testData/AYAMT/tierGuide.yaml"
    with open(tierGuideFile, 'r') as f:
        tierGuide = yaml.safe_load(f)

    x0 = IjalLine(doc, 0, tierGuide)
    x0.parse()

    assert (x0.speechRow == 0)
    assert (x0.translationRow == 1)
    assert (x0.morphemeRows == [])
    assert (x0.morphemeGlossRows == [])

    assert (x0.getSpokenText() == 'Por ejemplo el, como se llama, el mono,')
    assert (x0.getTranslation() == '‘For example it, what do you call it, the monkey,’')
    assert (x0.getMorphemes() == [])
    assert (x0.getMorphemeGlosses() == [])
    assert (x0.getMorphemeSpacing() == [])


# ----------------------------------------------------------------------------------------------------
def test_AYAMT_toHTML(displayPage=False):
    print("--- test_AYAMT_toHTML")

    filename = "../testData/AYAMT/AYAMT.eaf"
    grammaticalTermFile = "../testData/AYAMT/grammaticalTerms.txt"
    with open(grammaticalTermFile, 'r') as f:
        grammaticalTerms = f.read().split('\n')
    xmlDoc = etree.parse(filename)
    lineCount = len(xmlDoc.findall("TIER/ANNOTATION/ALIGNABLE_ANNOTATION"))  # 41

    tierGuideFile = "../testData/AYAMT/tierGuide.yaml"
    with open(tierGuideFile, 'r') as f:
        tierGuide = yaml.safe_load(f)

    lines = []
    for i in range(lineCount):
        line = IjalLine(xmlDoc, i, tierGuide, grammaticalTerms)
        # if(line.tierCount < 4):
        #    print("skipping line %d, tierCount %d" %(i, line.tierCount))
        # else:
        line.parse()
        lines.append(line)

    # print("parsed %d/%d complete lines" % (len(lines), lineCount))

    htmlDoc = Doc()

    htmlDoc.asis('<!DOCTYPE html>')
    with htmlDoc.tag('html', lang="en"):
        with htmlDoc.tag('head'):
            htmlDoc.asis('<meta charset="UTF-8">')
            htmlDoc.asis('<link rel="stylesheet" href="ijal.css">')
            htmlDoc.asis('<script src="ijalUtils.js"></script>')
            with htmlDoc.tag('body'):
                for line in lines:
                    line.toHTML(htmlDoc)

    htmlText = htmlDoc.getvalue()

    if (displayPage):
        filename = "tmp.html"
        f = open(filename, "w")
        f.write(indent(htmlText))
        f.close()
        os.system("open %s" % filename)


# ----------------------------------------------------------------------------------------------------
def test_aktzini_toHTML(displayPage=False):
    print("--- test_aktzini_toHTML")

    filename = "../testData/aktzini/18-06-03Aktzini-GA.eaf"
    xmlDoc = etree.parse(filename)
    lineCount = len(xmlDoc.findall("TIER/ANNOTATION/ALIGNABLE_ANNOTATION"))  # 16
    tierGuideFile = "../testData/aktzini/tierGuide.yaml"
    grammaticalTerms = "../testData/aktzini/grammaticalTerms.txt"

    with open(tierGuideFile, 'r') as f:
        tierGuide = yaml.safe_load(f)
    lineNumber = 0
    for lineNumber in range(lineCount):
        rootElement = xmlDoc.findall("TIER/ANNOTATION/ALIGNABLE_ANNOTATION")[lineNumber]
        allElements = findChildren(xmlDoc, rootElement)
        tmpTbl = buildTable(xmlDoc, allElements)
        print("---- line %d" % lineNumber)
        # print(tmpTbl)
    for i in range(lineCount):
        line = IjalLine(xmlDoc, i, tierGuide, grammaticalTerms)
    # print(line.tblRaw)
        # every line has exactly two tiers: "Line"  "L3Gloss"


# ----------------------------------------------------------------------------------------------------
def test_featherSnake_toHTML(displayPage=False):
    print("--- test_featherSnake_toHTML")

    filename = "../testData/featherSnake/featherSnake.eaf"
    xmlDoc = etree.parse(filename)
    lineCount = len(xmlDoc.findall("TIER/ANNOTATION/ALIGNABLE_ANNOTATION"))  # 15
    # print(lineCount)

    for lineNumber in range(lineCount):
        rootElement = xmlDoc.findall("TIER/ANNOTATION/ALIGNABLE_ANNOTATION")[lineNumber]
        allElements = findChildren(xmlDoc, rootElement)
        tmpTbl = buildTable(xmlDoc, allElements)
        # print("---- line %d" % lineNumber)
        # print(tmpTbl)

    tierGuideFile = "../testData/featherSnake/tierGuide.yaml"
    with open(tierGuideFile, 'r') as f:
        tierGuide = yaml.safe_load(f)

    lines = []
    grammaticalTerms = ["hab", "past"]
    for i in range(lineCount):
        line = IjalLine(xmlDoc, i, tierGuide, grammaticalTerms)
        if (line.tierCount < 4):
            print("skipping line %d, tierCount %d" % (i, line.tierCount))
        else:
            line.parse()
            lines.append(line)

    # print("parsed %d/%d complete lines" % (len(lines), lineCount))

    htmlDoc = Doc()

    htmlDoc.asis('<!DOCTYPE html>')
    with htmlDoc.tag('html', lang="en"):
        with htmlDoc.tag('head'):
            htmlDoc.asis('<meta charset="UTF-8">')
            htmlDoc.asis('<link rel="stylesheet" href="ijal.css">')
            htmlDoc.asis('<script src="ijalUtils.js"></script>')
            with htmlDoc.tag('body'):
                for line in lines:
                    line.toHTML(htmlDoc)

    htmlText = htmlDoc.getvalue()

    if (displayPage):
        filename = "tmp.html"
        f = open(filename, "w")
        f.write(indent(htmlText))
        f.close()
        os.system("open %s" % filename)


# ----------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    runTests()
