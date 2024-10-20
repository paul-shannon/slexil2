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

from slexil.textFromYaml import TextFromYaml

eafFiles = open("../testData/eafFileList.txt").read().split('\n')
if(eafFiles[-1] == ""):
    del eafFiles[-1]
print("eaf file count: %d" % len(eafFiles))

#---------------------------------------------------------------------------------------------------
def runTests():

   #test_lineToYAML()
   test_toYAML_inferno()
   #test_toYAML_tlingit()
   #test_toYAML_pesh()

#---------------------------------------------------------------------------------------------------
def test_lineToYAML():

    print("--- test_lineToYAML")
    f = "../testData/validEafFiles/inferno-threeLines.eaf"
    assert(os.path.isfile(Path(f)))
    parser = EafParser(f, verbose=False, fixOverlappingTimeSegments=False)
    parser.run()
    lines = parser.getAllLinesTable()
    assert(len(lines) == 3)
    line = lines[0]
    x = parser.lineToYAML(line, 1)
    assert(x[0] == '  - lineNumber: 1')
    assert(x[1] == '    startTime: 0')
    assert(x[2] == '    endTime: 2828')
    assert(x[3] == '    italianSpeech: Nel mezzo del cammin di nostra vita')
    assert(x[4] == '    morphemes: [en=il,mezz–o,de=il,cammin–Ø,di,nostr–a,vit–a]')
    assert(x[5] == '    morpheme-gloss: [in=DEF:MASC:SG,middle-MASC:SG,of=DEF:MASC:SG,journey–MASC:SG,of,our-FEM:SG,life-FEM]')
    assert(x[6] == '    english: Midway upon the journey of our life')
    
#---------------------------------------------------------------------------------------------------
def test_toYAML_inferno():

    print("--- test_toYAML_inferno")

    f = "../testData/validEafFiles/inferno-threeLines.eaf"
    parser = EafParser(f, verbose=False, fixOverlappingTimeSegments=False)
    parser.run()
    x = parser.toYAML("Dante's Inferno", "Roberto Benigni", "Paul Shannon")

    assert(len(x) == 31)

      # spot check some lines

    assert(x[0]  == "title: Dante's Inferno")
    assert(x[10]  == '    italianSpeech: Nel mezzo del cammin di nostra vita')
    assert(x[14] == '') # blank line between tierd line groups
    assert(x[18] == '    italianSpeech: mi ritrovai per una selva oscura')
    assert(x[29] == '    english: For the straightforward pathway had been lost.')

    fy = "inferno.yaml"
    parser.writeYAML(x, fy)
    fgt = "../explore/misc/inferno/tierGuide.yaml"
    ftg = "../explore/misc/inferno/grammaticalTerms.txt"

    pdb.set_trace()
    text = TextFromYaml(fy, fgt, ftg)


    
#---------------------------------------------------------------------------------------------------
def test_toYAML_tlingit():

    print("--- test_toYAML_tlingit")

    f = "../testData/validEafFiles/4EthelAnita230503Slexil.eaf"
    parser = EafParser(f, verbose=False, fixOverlappingTimeSegments=False)
    parser.run()
    x = parser.toYAML("Tlingit Conversation #4", "Ethel", "Alice Taff")

    assert(len(x) == 3039)

      # spot check some lines

    assert(x[0:6] == ['title: Tlingit Conversation #4',
                      'narrator: Ethel',
                      'textEntry: Alice Taff',
                      'mediaFile: https://slexildata.artsrn.ualberta.ca/tlingit/4EthelAnita.m4v',
                      'mimeType: video/mp4',
                      ''])

    assert(x[25:32] == ['  - lineNumber: 4',
                        '    startTime: 2887',
                        '    endTime: 5220',
                        '    utterance: Yéi ákwé, iduwasáakw? Aaá.',
                        '    translation: Is that what you are called? Yes.',
                        '    Speaker Initials: DEM',
                        ''])

    assert(x[3032:3039] == ['  - lineNumber: 438',
                            '    startTime: 1718633',
                            '    endTime: 1723169',
                            '    utterance: Gunalchéesh x̱á!',
                            '    translation: Thank you!',
                            '    Speaker Initials: KRL',
                            ''])

    
#---------------------------------------------------------------------------------------------------
def test_toYAML_pesh():

    print("--- test_toYAML_pesh")

    f = "../testData/validEafFiles/186_TheShaman.eaf"
    parser = EafParser(f, verbose=False, fixOverlappingTimeSegments=False)
    parser.run()
    tbl = parser.getTierTable()
    pdb.set_trace()

    x = parser.toYAML("Pesh Shaman #186", "unknown", "Natalia Caceres")

    assert(len(x) == 351)

    assert(x[0:6] == ['title: Pesh Shaman #186',
                      'narrator: unknown',
                      'textEntry: Natalia Caceres',
                      'mediaFile: https://slexildata.artsrn.ualberta.ca/pesh/186_Pesh.wav',
                      'mimeType: audio/x-wav',
                      ''])

    assert(x[8:15] == ['    startTime: 0',
                       '    endTime: 6920',
                       '    ref@BM: ar ye aparakan ʃana tiʃkwa akaki atusri',
                       '    to@BM: [ar,ye,apara=kan,ʃana,ta–iʃk–Ø–wa,a–kaki,a–tus=ri]',
                       '    ot@BM: [HES,small,youth=SIM,sick,MID–make–S3SG–PFV,POSS3SG–mother,POSS3SG–father=COORD]',
                       '    ft@BM: BM: ‘A teenager child gets sick, his mother and his father (call the shaman).’',
                       ''])
    parser.writeYAML(x, "shaman.yaml")    
    pdb.set_trace()
    f = "shaman.yaml"
    ftg = None
    fgt = None
    # text = TextFromYaml(f, fgt, ftg,
    #                     projectDirectory="shaman",
    #                     verbose = True,
    #                     fontSizeControls = True,
    #                     startLine = None,
    #                     endLine = None,
    #                     pageTitle = "inferno with markup",
    #                     helpFilename = None,
    #                     helpButtonLabel = None,
    #                     kbFilename = None,
    #                     linguisticsFilename = None,
    #                     fixOverlappingTimeSegments = False,
    #                     webpackLinksOnly=False,
    #                     useTooltips=False)


#---------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    runTests()
