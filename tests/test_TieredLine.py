# -*- tab-width: 3 -*-
import re
import sys, os

from slexil.sfmt import *
from slexil.tieredLine import TieredLine
#from slexil.inferTierStructure import InferTierStructure

from slexil.morphemeGlossAbbreviations import MorphemeGlossAbbreviations

import pdb
#import yaml
import yattag
import pandas as pd

pd.set_option('display.width', 1000)
pd.set_option('display.max_columns', None)

mga = MorphemeGlossAbbreviations()

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

    f  = "../testData/validEafYamlFiles/inferno-noAnalysisTiers.yaml"

    sfmt = SFMT(f)
    lines = sfmt.getTieredLines()
    assert(len(lines) == 3)

    tierGuide = sfmt.getTierGuide()
    tl = TieredLine(sfmt, lines, lineNumber=0, tierNumber=1,
                    tierGuide=tierGuide,
                    grammaticalTerms=mga.getAll(),
                    useTooltips=False, verbose=False)
    assert(type(tl).__name__ == 'TieredLine')
    tierMap = tl.getTierMap()
    expected =  {'speech': 'italianSpeech',
                 'tier_1': 'soundsLike',
                 'tier_2': 'english',
                 'tier_3': 'speaker'}
    assert(tierMap == expected)
    assert(sfmt.getGenericTierNameMap() == {'tier_1': 'soundsLike',
                                            'tier_2': 'english',
                                            'tier_3': 'speaker'})

    assert(sfmt.getSpeechTierNameMap() == {'speech': 'italianSpeech'})
    assert(sfmt.getAnalysisTierNameMap() == {})

    htmlDoc = yattag.Doc()
    tl.toHTML(htmlDoc)
    html = htmlDoc.getvalue()
    expected = '<div class="line-content" id="1"><div class="line"><span class="tier speech-tier" name="italianSpeech">Nel mezzo del cammin di nostra vita</span></div><div class="tier soundsLike-tier" name="soundsLike">nell metzo del kuh-mean dee nostruh veeta</div><div class="tier generic-tier" name="english">Midway upon the journey of our life</div><div class="annotationDiv"></div></div>'
    assert(html == expected)

    pdb.set_trace()

#----------------------------------------------------------------------------------------------------
def test_infernoFirstLine():

    print("--- test_infernoFirstLine")

    yamlTextFile = "../testData/validEafYamlFiles/inferno-noAnalysisTiers.yaml"
    its = InferTierStructure(yamlTextFile)

    fullDoc = yaml.load(open(yamlTextFile), Loader=yaml.FullLoader)
    expected = ['title', 'narrator', 'textEntry', 'mediaFile', 'mimeType', 'lines']
    assert(list(fullDoc.keys()) == expected)

    lines = fullDoc['lines']
    tierGuide = its.getTierGuide()
    line = TieredLine(lines, lineNumber=0, tierNumber=1,
                      tierGuide=tierGuide, grammaticalTerms=[],
                      useTooltips=False, verbose=False)

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

    yamlTextFile = "../testData/validEafYamlFiles/inferno-noAnalysisTiers.yaml"
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

    line = TieredLine(lines, lineNumber=0, tierNumber=1, tierGuide=tierGuide,
                      grammaticalTerms=[],
                      useTooltips=False, verbose=False)
    htmlDoc = yattag.Doc()
    s = line.toHTML(htmlDoc)
    html = htmlDoc.getvalue()
    expected = '<div class="line-content" id="1"><div class="line"><span class="tier speech-tier" name="italianSpeech">Nel mezzo del cammin di nostra vita</span></div><div class="tier soundsLike-tier" name="soundsLike">nell metzo del kuh-mean dee nostruh veeta</div><div class="tier generic-tier" name="english">Midway upon the journey of our life</div><div class="annotationDiv"></div></div>'
    assert(html == expected)

#----------------------------------------------------------------------------------------------------
def test_toHTML_withAnalysisLines():
    

    print("--- test_toHTML_withAnalysisLines")

    #grammaticalTerms = mga.getAll()

    yamlTextFile = "../testData/validEafYamlFiles/inferno-heterogeneousTiers.yaml"
    its = InferTierStructure(yamlTextFile)
    fullDoc = yaml.load(open(yamlTextFile), Loader=yaml.FullLoader)
    lines = fullDoc['lines']
    tierGuide = its.getTierGuide()

      # inferno line 1 (aka tier 2) has these morpheme glosses
      # [I:DAT,found–1SG:INDEF:REM:PAST,for,INDEF:FEM:SG,forest-FEM,dark–FEM:SG]
      # the leading I is (not) a grammatical gloss, but the actual first person
      # singular pronoun.  So a good test here is that all of the capitalized
      # terms are converted to lower case, tagged for class so they can be styled
      # as sm-cap - which requires that they be lower case.  and that the
      # I remains capitalized
    line = TieredLine(lines, lineNumber=1,   # the second line
                      tierNumber=1,
                      tierGuide=its.getTierGuide(),
                      grammaticalTerms=mga.getAll(),
                      useTooltips=False, verbose=False)
    htmlDoc = yattag.Doc()
    s = line.toHTML(htmlDoc)
    html = htmlDoc.getvalue()

    expected = '<div class="line-content" id="1"><div class="line"><span class="tier speech-tier" name="italianSpeech">mi ritrovai per una selva oscura</span></div><div class="tier morpheme-tier" style="grid-template-columns: 8ch 27ch 6ch 15ch 13ch 14ch ;" name="morphemes"><div class="morpheme-cell">mi</div><div class="morpheme-cell">ritrov–ai</div><div class="morpheme-cell">per</div><div class="morpheme-cell">una</div><div class="morpheme-cell">selv–a</div><div class="morpheme-cell">oscur–a</div></div><div class="tier morpheme-tier" style="grid-template-columns: 8ch 27ch 6ch 15ch 13ch 14ch ;" name="morpheme-gloss"><div class="morpheme-cell">I:<span class=\'grammatical-term\'>dat</span></div><div class="morpheme-cell">found–<span class=\'grammatical-term\'>1sg</span>:<span class=\'grammatical-term\'>indef</span>:<span class=\'grammatical-term\'>rem</span>:<span class=\'grammatical-term\'>past</span></div><div class="morpheme-cell">for</div><div class="morpheme-cell"><span class=\'grammatical-term\'>indef</span>:<span class=\'grammatical-term\'>fem</span>:<span class=\'grammatical-term\'>sg</span></div><div class="morpheme-cell">forest-<span class=\'grammatical-term\'>fem</span></div><div class="morpheme-cell">dark–<span class=\'grammatical-term\'>fem</span>:<span class=\'grammatical-term\'>sg</span></div></div><div class="tier soundsLike-tier" name="soundsLike">me ritrovie per oona selva oscura</div><div class="tier generic-tier" name="english">I found myself within a forest dark</div><div class="annotationDiv"></div></div>'
    assert(html == expected)

      # check a morpheme:
    expected = '<div class="tier morpheme-tier" style="grid-template-columns: 8ch 27ch 6ch 15ch 13ch 14ch ;" name="morphemes"><div class="morpheme-cell">mi</div>'
    assert(expected in html)

#----------------------------------------------------------------------------------------------------
def test_toHTML_withAnalysisLines_oneMorphemeOnly():
    
    print("--- test_toHTML_withAnalysisLines_oneMorphemeOnly")

    yamlTextFile = "../testData/validEafYamlFiles/daylight-line6-only.yaml"
    its = InferTierStructure(yamlTextFile)
    fullDoc = yaml.load(open(yamlTextFile), Loader=yaml.FullLoader)
    lines = fullDoc['lines']
    tierGuide = its.getTierGuide()

    line = TieredLine(lines, lineNumber=0,   # the second line
                      tierNumber=1,
                      tierGuide=its.getTierGuide(),
                      grammaticalTerms=mga.getAll(),
                      useTooltips=False, verbose=False)
    htmlDoc = yattag.Doc()
    s = line.toHTML(htmlDoc)
    html = htmlDoc.getvalue()

    assert(html.find('<div class="morpheme-cell">tu=c̓agʷa–t–sut=əxʷ</div>') > 0)
    assert(html.find("<span class='grammatical-term'>past</span>=washed–<span class='grammatical-term'>ics</span>–<span class='grammatical-term'>refl</span>=now</div>") > 0)


#----------------------------------------------------------------------------------------------------
def runTests():

   test_ctor()
   sys.exit(0)
   
   test_infernoFirstLine()
   test_toHTML_withAnalysisLines()
   test_toHTML_withAnalysisLines_oneMorphemeOnly()
   test_toHTML_noAnalysisLines()
   
#----------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    runTests()
