import os
import slexil
import pdb
import pandas as pd
from slexil.eafParser import EafParser

packageRoot = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dataDir = os.path.join(packageRoot, "data")
eafFile = os.path.join(dataDir, "infernoDemo", "inferno-threeLines.eaf")
tierGuideFile = os.path.join(dataDir, "infernoDemo", "tierGuide.yaml")

from slexil.standardizeIjalTierTable import StandardizeIjalTierTable

#------------------------------------------------------------------------------------------
def runTests():

   test_ctor()
   test_tierGuideAndLinesAgreement()
   test_addCanonicalTierNameColumn()
   test_multipleValuesInCanonicalTiers()
   
#------------------------------------------------------------------------------------------
# we create a pandas dataframe from the tiers of an ELAN eaf file
# simulate that here
def createLinesTable():

   tbl = pd.DataFrame(columns=["id","parent","startTime","endTime","tierID","tierType","text"])
   tbl["id"] = (0, 1, 2, 3)
   tbl["parent"] = ("a1", "a5", "a9", "a13")
   tbl["startTime"] = (0.0, float("NaN"), float("NaN"), float("NaN"))
   tbl["endTime"] = (3093.0, float("NaN"), float("NaN"), float("NaN"))
   tbl["tierID"] = ("italianSpeech", "morphemes", "morpheme-gloss", "english")
   tbl["tierType"] = ("default-lt", "morpheme", "morpheme-gloss", "translation")
   tbl["text"] = ("line 1", "line 2", "line 3", "line 4")

      #id parent  startTime  endTime          tierID        tierType                                               text
      #0   a1               0.0   3093.0   italianSpeech      default-lt                Nel mezzo del cammin di nostra vita
      #1   a5     a1        NaN      NaN       morphemes        morpheme  en=il\tmezz–o\tde=il\tcammin–Ø\tdi\tnostr–a\tv...
      #2   a9     a5        NaN      NaN  morpheme-gloss  morpheme-gloss  in=DEF:MASC:SG\tmiddle-MASC:SG\tof=DEF:MASC:SG...
      #3  a13     a1        NaN      NaN         english     translation                Midway upon the journey of our life


   return(tbl)

#------------------------------------------------------------------------------------------
def test_ctor():

    print("--- test_ctor")

    tierGuide = {'speech': 'italianSpeech',
                 'morpheme': 'morphemes',
                 'morphemeGloss': 'morpheme-gloss',
                 'translation': 'english'}

    tbl = createLinesTable()
    std = StandardizeIjalTierTable(tbl, tierGuide, verbose=False)
    tbl2 = std.getTable()
    assert(tbl2.shape == (4,7))  # all four tiers

    tierGuide = {'speech': 'italianSpeech'}
    std = StandardizeIjalTierTable(tbl, tierGuide, verbose=False)
    tbl2 = std.getTable()
    assert(tbl2.shape == (1,7))
    
    tierGuide = {'speech': 'italianSpeech',
                 'translation': 'english'}
    std = StandardizeIjalTierTable(tbl, tierGuide, verbose=False)
    tbl2 = std.getTable()
    assert(tbl2.shape == (2,7))

    tierGuide = {"speech": "esperanto"}
    try:
       std = StandardizeIjalTierTable(tbl, tierGuide, verbose=False)
    except Exception as ex:
        assert(True)
        msg = str(ex)
        expected = "none of the tbl tier names are in the tierGuide"
        assert(msg == expected)

    tierGuide = {'spooch': 'italianSpeech',
                 'translation': 'english'}
    try:
       std = StandardizeIjalTierTable(tbl, tierGuide, verbose=False)
    except Exception as ex:
        assert(True)
        msg = str(ex)
        expected = "required 'speech' tier not found in the tierGuide"
        assert(msg == expected)


    tbl2 = std.getTable()
    

#------------------------------------------------------------------------------------------
# all tierIDs in the tbl must be also in the tierGuide
def test_tierGuideAndLinesAgreement():

    print("--- test_tierGuideAndLinesAgreement")
    tierGuide = {'speech': 'italianSpeech',
                 'morpheme': 'morphemes',
                 'morphemeGloss': 'morpheme-gloss',
                 'translation': 'english',
                 }

    tbl = createLinesTable()
    std = StandardizeIjalTierTable(tbl, tierGuide, verbose=False)
    assert(std.guideAndLinesAgree())

       #---------------------------------------------------
       # should fail: the eaf (and therefore the lines tbl) 
       # has "italianSpeech"  for the canonical tier
       # name "speech"
       #---------------------------------------------------

    tierGuide["speech"] = "ItalianSpeach"  #

    try:
       std = StandardizeIjalTierTable(tbl, tierGuide, verbose=False)
       assert(std.guideAndLinesAgree())
    except Exception as ex:
        assert(True)
        msg = str(ex)
        expected = 'error in IjalLine standardizeTable. tier name/s not found in tierGuide:  ItalianSpeach'
        assert(msg == expected)

       #---------------------------------------------------------
       # the other kind of failure:  the keys of the tierGuide
       # are not a proper subset of the IJAL canonical tier names
       #---------------------------------------------------

    tierGuide = {'speech': 'italianSpeech',
                 'morphemeGliss': 'morpheme-gloss',
                 'translation': 'english',
                 }

    try:
       std = StandardizeIjalTierTable(tbl, tierGuide, verbose=False)
       assert(std.guideAndLinesAgree())
    except Exception as ex:
        assert(True)
        msg = str(ex)
        assert("error in IjalLine standardizeTable. tier name keys not IJAL canonicals: " in msg)
        assert("morphemeGliss" in msg)

      # speech is the only required tier
    tierGuide = {'speech': 'italianSpeech'}
    std = StandardizeIjalTierTable(tbl, tierGuide, verbose=False)
    assert(std.guideAndLinesAgree())


#------------------------------------------------------------------------------------------
def test_multipleValuesInCanonicalTiers():

   print("--- test_multipleValuesInCanonicalTiers")

     # now test for agreement when the tierGuide categories are multiple
   tierGuide = {'speech': ["ref@VG", "ref@AM"],
                 "translation": ["ft@VG", "ft@AM"],
                 "morpheme": ["to@VG", "to@AM"],
                 "morphemeGloss": ["ot@VG", "ot@AM"]}

   f = "../testData/validEafFiles/084_TheWomanOfTheWater-DonkeyTiger.eaf"
   parser = EafParser(f, verbose=False, fixOverlappingTimeSegments=False)
   parser.run()
   assert(parser.getLineCount() == 139)
   #parser.parseAllLines()
   tbls = parser.getAllLinesTable()  # a list of time-ordered line tables

   std = StandardizeIjalTierTable(tbls[0], tierGuide, verbose=False)
   tbl2 = std.getTable()
   assert(std.guideAndLinesAgree())

#------------------------------------------------------------------------------------------
def test_addCanonicalTierNameColumn():

   print("--- test_addCanonicalTierNameColumn")

   tbl = createLinesTable()

      #--------------------------------------------------
      # first, with a 4-tier table and a 4-tier tierGuide
      #--------------------------------------------------
     
   tierGuide = {'speech': 'italianSpeech',
                'morpheme': 'morphemes',
                'morphemeGloss': 'morpheme-gloss',
                'translation': 'english',
                }

   std = StandardizeIjalTierTable(tbl, tierGuide, verbose=False)
   assert(std.guideAndLinesAgree())
   std.addCanonicalTierNameColumn()
   tbl2 = std.getTable()

   assert(list(tbl2["tierID"]) ==
          ['italianSpeech', 'morphemes', 'morpheme-gloss', 'english'])
   assert(list(tbl2["canonicalTier"]) ==
          ['speech', 'morpheme', 'morphemeGloss', 'translation'])


      #--------------------------------------------------
      # second, with a 4-tier table and a 1-tier tierGuide
      # the table should be trimmed to only 1 row
      #--------------------------------------------------
     
   tierGuide = {'speech': 'italianSpeech'}

   std = StandardizeIjalTierTable(tbl, tierGuide, verbose=False)
   assert(std.guideAndLinesAgree())
   std.addCanonicalTierNameColumn()
   tbl2 = std.getTable()

   assert(tbl2.shape == (1, 8))
   assert(list(tbl2["tierID"]) == ['italianSpeech'])
   assert(list(tbl2["canonicalTier"]) ==  ['speech'])

#------------------------------------------------------------------------------------------
if __name__ == '__main__':
    runTests()
    
