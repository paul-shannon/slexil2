# -*- tab-width: 3 -*-
import re
import sys, os

from slexil.tieredLine import TieredLine
from slexil.inferTierStructure import InferTierStructure
# from slexil.yamlParser import YamlParser

import pdb
import yaml
import yattag
import pandas as pd

pd.set_option('display.width', 1000)
pd.set_option('display.max_columns', None)
#----------------------------------------------------------------------------------------------------
def extractTieredLine(yamlTextFile, lineNumber):

    tierGuideFile = "/tmp/tierGuide.yaml"
    its = InferTierStructure(yamlTextFile)
    its.writeTierGuide(tierGuideFile)
    # tierGuide = its.getTiersList()

    its.writeTierGuide(tierGuideFile)

    x = yaml.load(open(yamlTextFile), Loader=yaml.FullLoader)
    expectedFields = ['title', 'narrator', 'textEntry', 'mediaFile', 'mimeType', 'lines']
    assert(list(x.keys()) == expectedFields)
    lines = x["lines"]# parser.getAllLines()

    return({"line": lines[lineNumber],
            "tierGuideFile": tierGuideFile})
    
#----------------------------------------------------------------------------------------------------
def test_ctor():

    print("--- test_ctor")

    yamlTextFile = "../testData/validYamlFiles/inferno-noAnalysisTiers.yaml"
    its = InferTierStructure(yamlTextFile)
    x = yaml.load(open(yamlTextFile), Loader=yaml.FullLoader)
    lines = x['lines']
    tierGuide = its.getTierGuide()
    tl = TieredLine(lines, 0, tierGuide, grammaticalTerms=[],
                            useTooltips=False, verbose=True)
    assert(type(tl).__name__ == 'TieredLine')

       #-----------------------------------------------------
       # be sure that the its held by TieredLine has the same
       # inferences as the one we created above
       #-----------------------------------------------------

    its2 = tl.getIts()
    assert(its2.getTierGuide() == its.getTierGuide())

#----------------------------------------------------------------------------------------------------
def test_infernoFirstLine():

    print("--- test_infernoFirstLine")

    yamlTextFile = "../testData/validYamlFiles/inferno-noAnalysisTiers.yaml"
    its = InferTierStructure(yamlTextFile)

    fullDoc = yaml.load(open(yamlTextFile), Loader=yaml.FullLoader)
    expected = ['title', 'narrator', 'textEntry', 'mediaFile', 'mimeType', 'lines']
    assert(list(fullDoc.keys()) == expected)

    lines = fullDoc['lines']
    tierGuide = its.getTierGuide()
    line = TieredLine(lines, 0, tierGuide, grammaticalTerms=[],
                      useTooltips=False, verbose=True)

    assert(line.getSpeechTierNameMap() == {'speech': 'italianSpeech'})
    assert(line.getGenericTierNameMap() == {'tier_1': 'soundsLike', 'tier_2': 'english', 'tier_3': 'speaker'})
    assert(line.getAnalysisTierNameMap() == {})

    expected = ['speech', 'tier_1', 'tier_2', 'tier_3']
    assert(list(line.getTierGuide().keys()) == expected)
    assert(line.getTierNames() == expected)
    
    expected = ['italianSpeech', 'soundsLike', 'english', 'speaker']
    assert(list(line.getTierGuide().values()) == expected)
    assert(line.getTierValues() == expected)

    assert(line.getStartTime() == 0)
    assert(line.getEndTime() == 2828)
    assert(line.getSpokenText() == "Nel mezzo del cammin di nostra vita")

#----------------------------------------------------------------------------------------------------
def test_toHTML_noAnalysisLines():
    
    print("--- test_toHTML_noAnalysisLines")

    yamlTextFile = "../testData/validYamlFiles/inferno-noAnalysisTiers.yaml"
    its = InferTierStructure(yamlTextFile)
    fullDoc = yaml.load(open(yamlTextFile), Loader=yaml.FullLoader)
    lines = fullDoc['lines']
    tierGuide = its.getTierGuide()


    #------------------------------------------------------------
    # the first line:
    #   - lineNumber: 1
    #     startTime: 0
    #     endTime: 2828
    #     italianSpeech: Nel mezzo del cammin di nostra vita
    #     soundsLike: nell metzo del kuh-mean dee nostruh veeta
    #     english: Midway upon the journey of our life
    #------------------------------------------------------------

    line = TieredLine(lines, 0, tierGuide, grammaticalTerms=[],
                      useTooltips=False, verbose=True)
    htmlDoc = yattag.Doc()
    s = line.toHTML(htmlDoc)
    html = htmlDoc.getvalue()
    expected = '<div class="line-content" id="1"><div class="line"><span class="speech-tier">Nel mezzo del cammin di nostra vita</span></div><div class="generic-tier">nell metzo del kuh-mean dee nostruh veeta</div><div class="generic-tier">Midway upon the journey of our life</div><div class="annotationDiv"></div></div>'
    assert(html == expected)

    #------------------------------------------------------------
    # the second line:
    #   - lineNumber: 2
    #     startTime: 3095
    #     endTime: 5500
    #     italianSpeech: mi ritrovai per una selva oscura
    #     soundsLike: me ritrovie per oona selva oscura
    #     english: I found myself within a forest dark
    #     speaker: Roberto Benigni
    #------------------------------------------------------------

    line = TieredLine(lines, 1, tierGuide, grammaticalTerms=[],
                      useTooltips=False, verbose=True)
    htmlDoc = yattag.Doc()
    s = line.toHTML(htmlDoc)
    html = htmlDoc.getvalue()
    expected = '<div class="line-content" id="2"><div class="line"><span class="speech-tier">mi ritrovai per una selva oscura</span></div><div class="generic-tier">me ritrovie per oona selva oscura</div><div class="generic-tier">I found myself within a forest dark</div><div class="generic-tier">Roberto Benigni</div><div class="annotationDiv"></div></div>'
    assert(html == expected)

    #------------------------------------------------------------
    # the fourth line, just 1 language-related tier
    #   - lineNumber: 52
    #     startTime: 5624
    #     endTime: 8033
    #     italianSpeech: ché la diritta via era smarrita.
    #------------------------------------------------------------

    line = TieredLine(lines, 3, tierGuide, grammaticalTerms=[],
                      useTooltips=False, verbose=True)
    htmlDoc = yattag.Doc()
    s = line.toHTML(htmlDoc)
    html = htmlDoc.getvalue()
    expected = '<div class="line-content" id="4"><div class="line"><span class="speech-tier">ché la diritta via era smarrita.</span></div><div class="annotationDiv"></div></div>'
    assert(html == expected)

#----------------------------------------------------------------------------------------------------
def test_toHTML_withAnalysisLines():
    
    print("--- test_toHTML_withAnalysisLines")

    yamlTextFile = "../testData/validYamlFiles/inferno-heterogeneousTiers.yaml"
    its = InferTierStructure(yamlTextFile)
    fullDoc = yaml.load(open(yamlTextFile), Loader=yaml.FullLoader)
    lines = fullDoc['lines']
    tierGuide = its.getTierGuide()

    line = TieredLine(lines, 0, tierGuide, grammaticalTerms=[],
                      useTooltips=False, verbose=True)
    htmlDoc = yattag.Doc()
    s = line.toHTML(htmlDoc)
    html = htmlDoc.getvalue()

    expected = '<div class="line-content" id="1"><div class="line"><span class="speech-tier">Nel mezzo del cammin di nostra vita</span></div><div class="generic-tier">nell metzo del kuh-mean dee nostruh veeta</div><div class="generic-tier">Midway upon the journey of our life</div><div class="morpheme-tier" style="grid-template-columns: 17ch 17ch 17ch 18ch 5ch 13ch 11ch ;"><div class="morpheme-cell">en=il</div><div class="morpheme-cell">mezz–o</div><div class="morpheme-cell">de=il</div><div class="morpheme-cell">cammin–Ø</div><div class="morpheme-cell">di</div><div class="morpheme-cell">nostr–a</div><div class="morpheme-cell">vit–a</div></div><div class="morpheme-tier" style="grid-template-columns: 17ch 17ch 17ch 18ch 5ch 13ch 11ch ;"><div class="morpheme-cell"><div class="morpheme-gloss">in=DEF:MASC:SG</div></div><div class="morpheme-cell"><div class="morpheme-gloss">middle-MASC:SG</div></div><div class="morpheme-cell"><div class="morpheme-gloss">of=DEF:MASC:SG</div></div><div class="morpheme-cell"><div class="morpheme-gloss">journey–MASC:SG</div></div><div class="morpheme-cell"><div class="morpheme-gloss">of</div></div><div class="morpheme-cell"><div class="morpheme-gloss">our-FEM:SG</div></div><div class="morpheme-cell"><div class="morpheme-gloss">life-FEM</div></div></div><div class="annotationDiv"></div></div>'
    assert(html == expected)


#----------------------------------------------------------------------------------------------------
def runTests():

   test_ctor()
   test_infernoFirstLine()
   test_toHTML_noAnalysisLines()
   test_toHTML_withAnalysisLines()
   # test_toHTML_withHtmlLines()
   
#----------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    runTests()
