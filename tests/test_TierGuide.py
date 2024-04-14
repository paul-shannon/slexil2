from slexil.tierGuide import TierGuide
import pdb
#--------------------------------------------------------------------------------
def runTests():

   test_basic()
   test_speechOnly()
   test_detectUnsupportedTierNames()
   test_speechTierMissingOrMisname()
   test_pluralValues()

   test_deduceTierGuideFromEAF()
   
#--------------------------------------------------------------------------------
def test_basic():

   print("--- test_basic")
   x = TierGuide("../testData/tierGuides/inferno.yaml")

   tg = x.getGuide()
   assert(len(tg) == 4)
   assert(tg["speech"] == "italianSpeech")
   assert(tg["morpheme"] == "morphemes")
   assert(tg["morphemeGloss"] == "morpheme-gloss")
   assert(tg["translation"] == "english")

   assert(x.getTierNames() == ['speech', 'morpheme', 'morphemeGloss', 'translation'])
   assert(x.getTierValues() == ['italianSpeech', 'morphemes', 'morpheme-gloss', 'english'])
   
#--------------------------------------------------------------------------------
def test_speechOnly():

   print("--- test_speechOnly")
   x = TierGuide("../testData/tierGuides/speechOnly.yaml")

   tg = x.getGuide()
   assert(len(tg) == 1)
   assert(tg["speech"] == "italianSpeech")

   tierNames = x.getTierNames()
   tierValues = x.getTierValues()
   assert(x.getTierNames() == ['speech'])
   assert(x.getTierValues() == ['italianSpeech'])
   
   
#--------------------------------------------------------------------------------
def test_speechOnly():

   print("--- test_speechOnly")
   x = TierGuide("../testData/tierGuides/speechOnly.yaml")

   tg = x.getGuide()
   assert(len(tg) == 1)
   assert(tg["speech"] == "italianSpeech")
   
#--------------------------------------------------------------------------------
def test_speechTierMissingOrMisname():

   print("--- test_speechOnlyOrMisnamed")
   x = TierGuide("../testData/tierGuides/speechOnlyMisnamed.yaml")

   tg = x.getGuide()
   assert(x.valid()["valid"] == False)
   
#--------------------------------------------------------------------------------
def test_detectUnsupportedTierNames():

   print("--- test_detectUnsupportedTierNames")
   x = TierGuide("../testData/tierGuides/unsupportedTierNames.yaml")

   tg = x.getGuide()
   assert(len(tg) == 4)
   assert(tg["speechX"] == "italianSpeech")

   validity = x.valid()
   assert(not validity["valid"])
   badTierNames = validity["invalidNames"]
   assert("speechX" in badTierNames)
   assert("Xmorpheme" in badTierNames)
   assert("morphemeXGloss" in badTierNames)
   assert("translationnnn" in badTierNames)
   
#--------------------------------------------------------------------------------
def test_pluralValues():

   print("--- test_pluralValues")
   x = TierGuide("../testData/tierGuides/pluralValues.yaml")
   assert(x.getTierNames() == ['speech', 'translation', 'morpheme', 'morphemeGloss'])
   tg = x.getGuide()

   assert(len(tg) == 4)
   assert(tg["speech"] == ['ref@VG', 'ref@AM'])
   assert(tg["translation"] == ['ft@VG', 'ft@AM'])
   assert(tg["morpheme"] == ['to@VG', 'to@AM'])
   assert(tg["morphemeGloss"] == ['ot@VG', 'ot@AM'])

#--------------------------------------------------------------------------------
if __name__ == '__main__':
	runTests()
