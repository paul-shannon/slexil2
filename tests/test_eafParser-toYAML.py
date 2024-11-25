# -*- tab-width: 3 -*-
import yaml
import pdb
import os, sys
from slexil.eafParser import EafParser
import xmlschema
from xml.etree import ElementTree as etree
from time import time
import pandas as pd
import numpy as np
pd.set_option('display.width', 1000)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
from pathlib import Path
path = Path(".")
from xmlschema.validators.exceptions import XMLSchemaValidationError;

eafFiles = open("../testData/eafFileList.txt").read().split('\n')
if(eafFiles[-1] == ""):
    del eafFiles[-1]
print("eaf file count: %d" % len(eafFiles))

#---------------------------------------------------------------------------------------------------
# depth first traversal of nested lists, the structure of a project's tiers
#def dfs(lst):
#   result = []
#   for item in lst:
#       if isinstance(item, list):
#           dfs(item)
#       else:
#           print(item)

def dfs(lst):
    result = []
    for item in lst:
        if isinstance(item, list):
            result.extend(dfs(item))
        else:
            result.append(item)
    return result

def test_dfs():
   print("--- test_dfs")
   nested_list = [1, [2, 3], [4, [5, 6]]]
   assert(dfs(nested_list) == [1,2,3,4,5,6])

#---------------------------------------------------------------------------------------------------
def test_getHeader():

    print("--- test_getHeader")
    f = "../testData/validEafFiles/inferno-threeLines.eaf"
    p = EafParser(f, verbose=False, fixOverlappingTimeSegments=False)
    p.run()
    header = p.getYAMLHeader("inferno", "roberto begnini", "paul shannon")
    assert(header == ['title: inferno',
                      'narrator: roberto begnini',
                      'textEntry: paul shannon',
                      'mediaFile: https://slexildata.artsrn.ualberta.ca/misc/inferno-threeLines.wav',
                      'mimeType: audio/x-wav',
                      ''])

#---------------------------------------------------------------------------------------------------
def test_getLine():

    print("--- test_getLine")

    f = "../testData/validEafFiles/inferno-threeLines.eaf"
    p = EafParser(f, verbose=False, fixOverlappingTimeSegments=False)
    p.run()

    tbl = p.getLineTable(0)
    line = p.lineToYAML(tbl,0)
    assert(line == ['  - lineNumber: 0',
                    '    startTime: 3095',
                    '    endTime: 5500',
                    '    italianSpeech: mi ritrovai per una selva oscura',
                    '    morphemes: [mi,ritrov–ai,per,una,selv–a,oscur–a]',
                    '    morpheme-gloss: [I:DAT,found–1SG:INDEF:REM:PAST,for,INDEF:FEM:SG,forest-FEM,dark–FEM:SG]',
                    '    english: I found myself within a forest dark'])

#---------------------------------------------------------------------------------------------------
def test_getTierStructure():

    print("--- test_getTierStructure")

    f = "../testData/validEafFiles/inferno-threeLines.eaf"
    p = EafParser(f, verbose=False, fixOverlappingTimeSegments=False)
    p.run()
    tbl = p.getTierTable()
    timeAlignedTiers = list(tbl[tbl["TIME_ALIGNABLE"] == "true"]["TIER_ID"])
    assert(timeAlignedTiers == ['italianSpeech'])
    p.depthFirstTierTraversal("a2")
    assert(p.getTimeAlignedTiers() == ["italianSpeech"])
    kids = p.getTimeAlignedTierChildren("italianSpeech")
    assert(kids == ['morphemes', 'morpheme-gloss', 'english'])

#---------------------------------------------------------------------------------------------------
def test_getAll():

    print("--- test_getAll")

    f = "../testData/validEafFiles/inferno-threeLines.eaf"
    p = EafParser(f, verbose=False, fixOverlappingTimeSegments=False)
    p.run()

    x = p.toYAML("inferno", "roberto benigni", "paul shannon")
    assert(len(x) == 31)
    assert(x == ['title: inferno',
                 'narrator: roberto benigni',
                 'textEntry: paul shannon',
                 'mediaFile: https://slexildata.artsrn.ualberta.ca/misc/inferno-threeLines.wav',
                 'mimeType: audio/x-wav',
                 '',
                 'lines:',
                 '  - lineNumber: 1',
                 '    startTime: 0',
                 '    endTime: 2828',
                 '    italianSpeech: Nel mezzo del cammin di nostra vita',
                 '    morphemes: [en=il,mezz–o,de=il,cammin–Ø,di,nostr–a,vit–a]',
                 '    morpheme-gloss: [in=DEF:MASC:SG,middle-MASC:SG,of=DEF:MASC:SG,journey–MASC:SG,of,our-FEM:SG,life-FEM]',
                 '    english: Midway upon the journey of our life',
                 '',
                 '  - lineNumber: 2',
                 '    startTime: 3095',
                 '    endTime: 5500',
                 '    italianSpeech: mi ritrovai per una selva oscura',
                 '    morphemes: [mi,ritrov–ai,per,una,selv–a,oscur–a]',
                 '    morpheme-gloss: [I:DAT,found–1SG:INDEF:REM:PAST,for,INDEF:FEM:SG,forest-FEM,dark–FEM:SG]',
                 '    english: I found myself within a forest dark',
                 '',
                 '  - lineNumber: 3',
                 '    startTime: 5624',
                 '    endTime: 8033',
                 '    italianSpeech: ché la diritta via era smarrita.',
                 '    morphemes: [ché,la,diritt–a,vi–a,era,smarr–it–a]',
                 '    morpheme-gloss: [that,def:FEM:SG,straight-FEM:SG,path-FEM,be:3SG:IMPF,lose–PARTIC–FEM:SG]',
                 '    english: For the straightforward pathway had been lost.', ''])

#---------------------------------------------------------------------------------------------------
def test_aliceTaff_1():

    print("--- test_aliceTaff-1")

    f = "../explore/aliceTaff/dontWearRed/Don_tWearRed240419.eaf"
    p = EafParser(f, verbose=False, fixOverlappingTimeSegments=False)
    p.run()
    tbl = p.getTierTable()
    assert(tbl.shape == (2, 7))
    tierNames = list(tbl["TIER_ID"])
    assert(tierNames == ['utterance', 'translation'])
    yaml = p.toYAML("title", "speaker", "transcriber")
    assert(yaml == ['title: title',
                    'narrator: speaker',
                    'textEntry: transcriber',
                    'mediaFile: https://slexildata.artsrn.ualberta.ca/tlingit/Don_tWearRed.MOV',
                    'mimeType: video/quicktime',
                    '',
                    'lines:',
                    '  - lineNumber: 1',
                    '    startTime: 1070',
                    '    endTime: 3318', "    utterance: Go xitr'itodał tux,", "    translation: When we're going to go (for berries)",
                    '',
                    '  - lineNumber: 2',
                    '    startTime: 7070',
                    '    endTime: 12047', "    utterance: sitoʼ, «Dithiqirz ndliyuxliyo'.»",
                    '    translation: My father, "Red"',
                    '',
                    '  - lineNumber: 3',
                    '    startTime: 13129',
                    '    endTime: 15169', "    utterance: dina iłne tsʼi xiyan'.",
                    '    translation: he told us only.',
                    '',
                    '  - lineNumber: 4',
                    '    startTime: 15610',
                    '    endTime: 19300',
                    '    utterance: Ngo getiy viginalnek xiy in iy.',
                    '    translation: Well it (bear) really likes it (red).',
                    '',
                    '  - lineNumber: 5',
                    '    startTime: 19450',
                    '    endTime: 21368',
                    '    utterance: (di)na iłne.',
                    '    translation: he told us.', ''])
    p.writeYAML(yaml, "dontWearRead.yaml")

#---------------------------------------------------------------------------------------------------
# 10 time-aligned tiers, each with IPA, free translation tiers, and
# the analysis tiers are way too many, 17 pairs for line 15 for example
# these -could- be recognized and transformed to one pair of tiers,
# each a list of morphemes and their glosses.  but this may be a rare edge case
# not yet obviously worth handling.
def test_nestedTiers_useless():

    print("--- test_nestedTiers_useless")

      
    f = "../testData/validEafFiles/featherSnake.eaf"
    p = EafParser(f, verbose=False, fixOverlappingTimeSegments=False)
    p.run()
    tbl = p.getTierTable()
    pdb.set_trace()

#---------------------------------------------------------------------------------------------------
def test_nataliaComplex():

    print("--- test_nataliaComplex")

    f = "../testData/validEafFiles/natalia-yekwana.eaf"
    p = EafParser(f, verbose=False, fixOverlappingTimeSegments=False)
    p.run()
    tbl = p.getTierTable()

    tierNames = list(tbl["TIER_ID"])
    assert(tierNames == ['ref@FcM',   'ref@Anl', 'id@FcM',  'to@FcM',  'ft@FcM',
                         'iu@FcM',    'nq@FcM',  'nt@FcM',  'to@Anl',  'ft@Anl',
                         'iu@Anl',    'nt@Anl',  'ot@FcM',  'ot@Anl',  'ft-en@FcM',
                         'ft-en@Anl', 'tx@FcM',  'tx@Anl',  'mot@FcM', 'mb@FcM',
                         'ge@FcM',    'ps@FcM',  'mot@Anl', 'mb@Anl',  'ge@Anl',
                         'ps@Anl',    'tag@Anl', 'tag@FcM'])

    timeAlignedTiers = list(tbl[tbl["TIME_ALIGNABLE"] == "true"]["TIER_ID"])
    assert(timeAlignedTiers == ['ref@FcM', 'ref@Anl'])

    allParentTiers = list(tbl[tbl["TIME_ALIGNABLE"] == "false"]["PARENT_REF"])
    allParentTiers = list(sorted(set(allParentTiers), key=allParentTiers.index))
    for parentTier in allParentTiers:
        directKids = list(tbl[tbl["PARENT_REF"] == parentTier]["TIER_ID"])
        print("  parent %s  kids %d: %s" % (parentTier, len(directKids),
                                            " ".join(directKids)))

   #   parent ref@FcM direct kids 10, 4 sub-kids:
   #      id@FcM
   #      to@FcM
   #      ft@FcM
   #      iu@FcM
   #      nq@FcM
   #      nt@FcM
   #      ot@FcM
   #      ft-en@FcM
   #      tx@FcM - mot@FcM - mb@FcM -[ge@FcM ps@FcM]
   #      tag@FcM
   #                                       
   #   parent ref@Anl  kids 8, 4 sub-kids
   #      to@Anl
   #      ft@Anl
   #      iu@Anl
   #      nt@Anl
   #      ot@Anl
   #      ft-en@Anl
   #      tx@Anl - mot@An1 - mb@Anl - [ge@Anl ps@Anl]
   #      tag@Anl
    x0 = ["ref@FcM","id@FcM", "to@FcM", "ft@FcM", "iu@FcM", "nq@FcM",
          "nt@FcM", "ot@FcM", "ft-en@FcM",
          ["tx@FcM", "mot@FcM", ["mb@FcM", "ge@FcM", "ps@FcM"]],
          "tag@Fcm"]
    x1 = [1,2,3,4,5,6,7,8,9,[10, 11, [12, 13, 14]],16]

    fcmDirectKids = list(tbl[tbl["PARENT_REF"] == "ref@FcM"]["TIER_ID"])
    anlDirectKids = list(tbl[tbl["PARENT_REF"] == "ref@Anl"]["TIER_ID"])

    assert(fcmDirectKids == ['id@FcM', 'to@FcM', 'ft@FcM', 'iu@FcM', 'nq@FcM',
                            'nt@FcM', 'ot@FcM', 'ft-en@FcM', 'tx@FcM', 'tag@FcM'])
    assert(anlDirectKids == ['to@Anl', 'ft@Anl', 'iu@Anl', 'nt@Anl', 'ot@Anl',
                            'ft-en@Anl', 'tx@Anl', 'tag@Anl'])


    x = p.toYAML("Yek09", "FcM, An1", "Natalia Caceres")
    assert(tierNames == ['ref@FcM',   'ref@Anl', 'id@FcM',  'to@FcM',  'ft@FcM',
                         'iu@FcM',    'nq@FcM',  'nt@FcM',  'to@Anl',  'ft@Anl',
                         'iu@Anl',    'nt@Anl',  'ot@FcM',  'ot@Anl',  'ft-en@FcM',
                         'ft-en@Anl', 'tx@FcM',  'tx@Anl',  'mot@FcM', 'mb@FcM',
                         'ge@FcM',    'ps@FcM',  'mot@Anl', 'mb@Anl',  'ge@Anl',
                         'ps@Anl',    'tag@Anl', 'tag@FcM'])

    assert(p.getTimeAlignedTiers() == ['ref@FcM', 'ref@Anl'])
    kids0 = p.getTimeAlignedTierChildren('ref@FcM')
    assert(kids0 == ['to@FcM', 'ft@FcM', 'iu@FcM', 'ot@FcM', 'ft-en@FcM',
                     'tx@FcM', 'mot@FcM', 'mb@FcM', 'ge@FcM', 'ps@FcM',
                     'mot@FcM', 'mb@FcM', 'ge@FcM', 'ps@FcM', 'mot@FcM',
                     'mb@FcM', 'ge@FcM', 'ps@FcM', 'mb@FcM', 'ge@FcM',
                     'ps@FcM', 'mb@FcM', 'ge@FcM', 'ps@FcM', 'mb@FcM',
                     'ge@FcM', 'ps@FcM', 'mot@FcM', 'mb@FcM', 'ge@FcM',
                     'ps@FcM', 'tag@FcM'])

#---------------------------------------------------------------------------------------------------
def runTests():

   test_dfs()
   test_getHeader()
   test_getLine()
   test_getTierStructure()
   test_getAll()

   test_nestedTiers_1()
   test_aliceTaff_1()
   test_nataliaComplex()

#---------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    runTests()
