# -*- tab-width: 3 -*-
import pdb
import os, sys
import yaml
from slexil.inferTierStructure import InferTierStructure
from time import time
from pathlib import Path
path = Path(".")
#---------------------------------------------------------------------------------------------------
def test_fileConstructor():

    print("--- test_fileConstructor")

    f = "../testData/validYamlFiles/inferno-heterogeneousTiers.yaml"
    its = InferTierStructure(f)
    assert(type(its).__name__ == 'InferTierStructure')

#----------------------------------------------------------------------------------------------------
def test_parsedLinesConstructor():

    print("--- test_parsedLinesConstructor")

    f = "../testData/validYamlFiles/inferno-heterogeneousTiers.yaml"
    x = yaml.load(open(f), Loader=yaml.FullLoader)
    lines = x['lines']

    its = InferTierStructure(lines)
    assert(type(its).__name__ == 'InferTierStructure')

    tierNames = its.getAllTierNames()
    assert(len(tierNames) == 6)
    assert('italianSpeech' in tierNames)

    assert(len(its.getAllLines()) == 3)
    assert(len(its.getTieredLines()) == 3)
    assert(len(its.getHtmlLines()) == 0)
    
#----------------------------------------------------------------------------------------------------
def test_linesConstructor():

    print("--- test_linesConstructor")

    f = "../testData/validYamlFiles/inferno-heterogeneousTiers.yaml"
    yp = YamlParser(f)
    lines = yp.getRawLines()  # all lines within the "lines" yaml field

    its = InferTierStructure(lines)
    assert(type(its).__name__ == 'InferTierStructure')

    tl = its.getAllTierNames()
    assert(len(tl) == 3)
    assert('italianSpeech' in tl[0])

#----------------------------------------------------------------------------------------------------
def test_getAllTierNames():

    print("--- test_getAllTierNames")

    f = "../testData/validYamlFiles/inferno-heterogeneousTiers.yaml"
    its = InferTierStructure(f)
    x = its.getAllTierNames()
    expected = ['italianSpeech', 'soundsLike', 'morphemes',
                'morpheme-gloss', 'english', 'speaker']
    assert(x == expected)

#----------------------------------------------------------------------------------------------------
def test_identifyAnalysisTiers():

    print("--- test_identifyAnalysisTiers")

    f = "../testData/validYamlFiles/inferno-heterogeneousTiers.yaml"
    its = InferTierStructure(f)
    #its.identifyAnalysisTiers()
    analysisTiers = list(its.getAnalysisTierNameMap().values())
    assert(analysisTiers == ['morphemes', 'morpheme-gloss'])

#----------------------------------------------------------------------------------------------------
# some conditions to satisfy:
#
#   - no analysis tiers included
#
#   - order of the generic tiers should follow that found in lines with
#     the most tiers.  alice taff's tlingit conversation has speaker initials
#     in the firest mostly documentary line, with the translation tier not
#     appearing until line 3.
#     
def test_getGenericTiers_inProperOrder():

    print("--- test_getGenericTiersInProperOrder")

    f = "../testData/validYamlFiles/61.yaml"
    its = InferTierStructure(f)
    tiers = its.getGenericTierNameMap()
       # make sure that Speaker initials comes last

    assert(tiers == {'tier_1': 'translation', 'tier_2': 'Speaker initials'})
    assert(list(tiers.values()) == ['translation', 'Speaker initials'])

    f = "../testData/validYamlFiles/inferno-heterogeneousTiers.yaml"
    its = InferTierStructure(f)
    tiers = its.getGenericTierNameMap()
    assert(tiers == {'tier_1': 'soundsLike', 'tier_2': 'english', 'tier_3': 'speaker'})
    assert(list(tiers.values()) == ['soundsLike', 'english', 'speaker'])

#----------------------------------------------------------------------------------------------------
def test_getSpeechTier():

    print("--- test_getSpeechTier")

    f = "../testData/validYamlFiles/inferno-heterogeneousTiers.yaml"
    its = InferTierStructure(f)
    
    stMap = its.getSpeechTierNameMap()
    assert(stMap == {'speech': 'italianSpeech'})
       # here's how to get the tier names and values
    assert(list(stMap.keys()) == ['speech'])
    assert(list(stMap.values()) == ['italianSpeech'])

#----------------------------------------------------------------------------------------------------
def test_getGenericTiers():

    print("--- test_getGenericTiers")

    f = "../testData/validYamlFiles/inferno-heterogeneousTiers.yaml"
    its = InferTierStructure(f)
    gtMap = its.getGenericTierNameMap()
    assert(gtMap == {'tier_1': 'soundsLike', 'tier_2': 'english', 'tier_3': 'speaker'})

       # here's how to get the tier names and values
    assert(list(gtMap.keys()) == ['tier_1', 'tier_2', 'tier_3'])
    assert(list(gtMap.values()) == ['soundsLike', 'english', 'speaker'])

#----------------------------------------------------------------------------------------------------
def test_getAnalysisTiers():

    print("--- test_getAnalysis")

    f = "../testData/validYamlFiles/inferno-heterogeneousTiers.yaml"
    its = InferTierStructure(f)
    atMap = its.getAnalysisTierNameMap()


#----------------------------------------------------------------------------------------------------
def test_recognizeAbsentAnalysisTiers():

    print("--- test_recognizeAbsentAnalysisTiers")

    f = "../testData/validYamlFiles/inferno-noAnalysisTiers.yaml"
    its = InferTierStructure(f)
    assert(its.getAllTierNames() == ['italianSpeech', 'soundsLike', 'english', 'speaker'])
    assert(its.getGenericTierNameMap() ==
           {'tier_1': 'soundsLike', 'tier_2': 'english', 'tier_3': 'speaker'})
    assert(its.getAnalysisTierNameMap() == {})

#----------------------------------------------------------------------------------------------------
def test_writeTierGuide():

    print("--- test_writeTierGuide")

    f = "../testData/validYamlFiles/inferno-heterogeneousTiers.yaml"
    its = InferTierStructure(f)
    yamlFile = "/tmp/tierGuide.yaml"
    its.writeTierGuide(yamlFile)
    x = yaml.load(open(yamlFile), Loader=yaml.FullLoader)
    assert(x['speech'] == 'italianSpeech')
    assert(x['tier_1'] == 'soundsLike')
    assert(x['analysis_1'] == 'morphemes')
    assert(x['analysis_2'] == 'morpheme-gloss')
    assert(x['tier_2'] == 'english')
    assert(x['tier_3'] == 'speaker')

#----------------------------------------------------------------------------------------------------
def test_getTierGuide():

    print("--- test_getTierGuide")

    f = "../testData/validYamlFiles/inferno-heterogeneousTiers.yaml"
    its = InferTierStructure(f)
    tg = its.getTierGuide()
    assert(list(tg.keys()) ==
           ['speech', 'tier_1', 'analysis_1', 'analysis_2', 'tier_2', 'tier_3'])
    assert(tg["speech"] == "italianSpeech")
    assert(tg['tier_1'] == "soundsLike")
    assert(tg['analysis_1'] == "morphemes")
    assert(tg['analysis_2'] == "morpheme-gloss")
    assert(tg['tier_2'] == "english")
    assert(tg['tier_3'] == "speaker")

#----------------------------------------------------------------------------------------------------
def test_getTierGuide():

    print("--- test_getTierGuide")

    f = "../testData/validYamlFiles/inferno-heterogeneousTiers.yaml"
    its = InferTierStructure(f)
    tg = its.getTierGuide()
    assert(list(tg.keys()) ==
           ['speech', 'tier_1', 'analysis_1', 'analysis_2', 'tier_2', 'tier_3'])
    assert(tg["speech"] == "italianSpeech")
    assert(tg['tier_1'] == "soundsLike")
    assert(tg['analysis_1'] == "morphemes")
    assert(tg['analysis_2'] == "morpheme-gloss")
    assert(tg['tier_2'] == "english")
    assert(tg['tier_3'] == "speaker")

#----------------------------------------------------------------------------------------------------
def test_getTierGuide_yamlHasSomeHtmlLines():

    print("--- test_getTierGuide_yamlHasSomeHtmlLines")

    f = "../testData/validYamlFiles/inferno-withHtmlLines.yaml"
    its = InferTierStructure(f)
    tg = its.getTierGuide()
    assert(list(tg.keys()) == ['speech', 'analysis_1', 'analysis_2', 'tier_1'])
    assert(tg["speech"] == "italianSpeech")
    assert(tg['analysis_1'] == "morphemes")
    assert(tg['analysis_2'] == "morpheme-gloss")
    assert(tg['tier_1'] == "english")

    assert(len(its.getAllLines()) == 9)
    assert(len(its.getTieredLines()) == 3)
    assert(len(its.getHtmlLines()) == 6)
    
#----------------------------------------------------------------------------------------------------
def runTests():

  test_fileConstructor()
  test_parsedLinesConstructor()
  test_getAllTierNames()
  test_identifyAnalysisTiers()
  test_getSpeechTier()
  test_getGenericTiers()
  test_getGenericTiers_inProperOrder()
  test_getAnalysisTiers()
  test_getTierGuide_yamlHasSomeHtmlLines()
  test_getTierGuide()
  test_writeTierGuide()
  test_recognizeAbsentAnalysisTiers()

#---------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    runTests()
