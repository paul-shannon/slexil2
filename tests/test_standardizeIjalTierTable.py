import os
import slexil
import pandas as pd

packageRoot = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dataDir = os.path.join(packageRoot, "data")
eafFile = os.path.join(dataDir, "infernoDemo", "inferno-threeLines.eaf")
tierGuideFile = os.path.join(dataDir, "infernoDemo", "tierGuide.yaml")

from slexil.standardizeIjalTierTable import StandardizeIjalTierTable

#------------------------------------------------------------------------------------------
def runTests():

   test_ctor()
   test_tierGuideAndLinesAgreement()
   
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
                 'transcription2': None,
                 'morpheme': 'morphemes',
                 'morphemeGloss': 'morpheme-gloss',
                 'translation': 'english',
                 'translation2': None}

    tbl = createLinesTable()
    std = StandardizeIjalTierTable(tbl, tierGuide, verbose=False)
#------------------------------------------------------------------------------------------
# all tierIDs in the tbl must be also in the tierGuide
def test_tierGuideAndLinesAgreement():

    print("--- test_tierGuideAndLinesAgreement")
    tierGuide = {'speech': 'italianSpeech',
                 #'transcription2': None,
                 'morpheme': 'morphemes',
                 'morphemeGloss': 'morpheme-gloss',
                 'translation': 'english',
                 #'translation2': None
                 }

    tbl = createLinesTable()
    std = StandardizeIjalTierTable(tbl, tierGuide, verbose=False)
    assert(std.guideAndLinesAgree())

       #-------------------
       # should fail
       #--------------------

    tierGuide["speech"] = "ItalianSpeach"  #
    try:
       std = StandardizeIjalTierTable(tbl, tierGuide, verbose=False)
       assert(std.guideAndLinesAgree())
    except Exception as ex:
        assert(True)
        print(ex)
    
#------------------------------------------------------------------------------------------
if __name__ == '__main__':
    runTests()
    
