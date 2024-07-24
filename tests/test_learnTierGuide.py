# -*- tab-width: 3 -*-
from slexil.learnTierGuide import LearnTierGuide
import pdb
import pandas as pd
import yaml, os

pd.set_option('display.width', 1000)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

#---------------------------------------------------------------------------------------------------
eafFiles = open("../testData/eafFileList.txt").read().split('\n')
if(eafFiles[-1] == ""):
    del eafFiles[-1]
print("eaf file count: %d" % len(eafFiles))
#---------------------------------------------------------------------------------------------------
def runTests():

   #test_getTimeAlignedTierCount()
   #test_getTimeAlignedTiersAndTheirChildren()
   #test_getTokenizedTierPairs()
   #test_learnTierGuide()
   test_learnTierGuide_novelTierName()

#------------------------------------------------------------------------------------------
def test_getTimeAlignedTierCount():

   print("--- test_getTimeAlignedTierCount")
   for f in eafFiles:
      print("    %s" % f)
      ltg = LearnTierGuide(f, verbose=False)
      #if f == "../explore/halkomelem/raven/2_CDA_raven.eaf":
      #    pdb.set_trace()
      assert(len(ltg.getTimeAlignedTiers()) in [1,2,3])
       
#------------------------------------------------------------------------------------------
def test_getTimeAlignedTiersAndTheirChildren():

   print("--- test_getTimeAlignedTiersAndTheirChildren")

     #---------------------------------------------------------------
     # first, an eaf with just one time-aligned tier, just one child
     #---------------------------------------------------------------

   f = "../explore/aliceTaff/01/01RuthNora230503Slexil.eaf"
   print("    01RuthNora230503Slexil.eaf")
   ltg = LearnTierGuide(f, verbose=False)
   tbl = ltg.getTierTable()
   taTiers = ltg.getTimeAlignedTiers()
   assert(taTiers == ['utterance'])
   children = ltg.getTimeAlignedTierChildren("utterance")
   assert(children == ['translation'])

     #---------------------------------------------------------------
     # second, the standard IJAL 4-tier line, one time-aligned
     #---------------------------------------------------------------

   f = "../explore/misc/inferno/inferno-threeLines.eaf"
   print("    inferno-threeLines.eaf")
   ltg = LearnTierGuide(f)
   tbl = ltg.getTierTable()
   taTiers = ltg.getTimeAlignedTiers()
   assert(taTiers == ['italianSpeech'])
   children = ltg.getTimeAlignedTierChildren("italianSpeech")
   assert(children == ['morphemes', 'morpheme-gloss', 'english'])

     #---------------------------------------------------------------
     # third, another standard IJAL 4-tier line, one time-aligned,
     # morpheme-gloss, however, specified as child of the morpheme tier
     #---------------------------------------------------------------

   f = "../explore/daylight/beckAndHess/beckAndHess.eaf"
   print("    daylight, beckAndHess.eaf")
   ltg = LearnTierGuide(f)
   tbl = ltg.getTierTable()
   taTiers = ltg.getTimeAlignedTiers()
   assert(taTiers == ['lushootseed'])
   children= ltg.getTimeAlignedTierChildren("lushootseed")
   assert(children == ['morphemes', 'morphemeGloss', 'english'])

#
#     #---------------------------------------------------------------
#     # third, two time-aligned tiers, each with full IJAL set of children
#     #---------------------------------------------------------------
#
#   f = "../explore/nataliaCaceres/085-motherOfTheFish/085_TheMotherOfTheFishAndThePrankster.eaf"
#   print("   085_TheMotherOfTheFishAndThePrankster.eaf")
#   parser = EafParser(f, verbose=False, fixOverlappingTimeSegments=False)
#   taTiers = parser.getTimeAlignedTiers()
#   assert(taTiers == ['ref@VG', 'ref@AM'])
#   children = parser.getTimeAlignedTierChildren("ref@VG")
#   assert(children == ['to@VG', 'ot@VG', 'ft@VG'])
#   children = parser.getTimeAlignedTierChildren("ref@AM")
#   assert(children == ['to@AM', 'ot@AM', 'ft@AM'])


#---------------------------------------------------------------------------------------------------
def test_getTokenizedTierPairs():

   print("--- test_getTimeAlignedTiersAndTheirChildren")


     #---------------------------------------------------------------
     # first, a standard IJAL 4-tier schema, one time-aligned
     # one pair of tokenized lines
     #---------------------------------------------------------------

   f = "../explore/misc/inferno/inferno-threeLines.eaf"
   print("    inferno-threeLines.eaf")
   ltg = LearnTierGuide(f)
   ltg.parser.run()
   tat = ltg.getTimeAlignedTiers()[0]
   assert(ltg.getTokenizedTierPairs(tat) == {'morphemes': 16, 'morpheme-gloss': 16})

     #---------------------------------------------------------------
     # second, an eaf with just one time-aligned tier, just one child
     # no tokenized pairs
     #---------------------------------------------------------------

   f = "../explore/aliceTaff/01/01RuthNora230503Slexil.eaf"
   print("    01RuthNora230503Slexil.eaf")
   ltg = LearnTierGuide(f, verbose=False)
   ltg.parser.run()
   tat = ltg.getTimeAlignedTiers()[0]
   assert(ltg.getTokenizedTierPairs(tat) == {})
   
     #---------------------------------------------------------------
     # third, another standard IJAL 4-tier line, one time-aligned,
     # morpheme-gloss, however, specified as child of the morpheme tier
     #---------------------------------------------------------------

   f = "../explore/daylight/beckAndHess/beckAndHess.eaf"
   print("    daylight, beckAndHess.eaf")
   ltg = LearnTierGuide(f, verbose=False)
   ltg.parser.run()
   tat = ltg.getTimeAlignedTiers()[0]
   pairs = ltg.getTokenizedTierPairs(tat)
   assert(pairs == {'morphemes': 554, 'morphemeGloss': 554})
   
#---------------------------------------------------------------------------------------------------
def test_learnTierGuide():

   print("--- test_learnTierGuide")
    
     #---------------------------------------------------------------
     # first the standard IJAL 4-tier line, one time-aligned
     # one pair of tokenized (tab-delimited) tiers
     #---------------------------------------------------------------

   print("    inferno-threeLines")

   f = "../explore/misc/inferno/inferno-threeLines.eaf"
   ltg = LearnTierGuide(f, verbose=False)
   ltg.parser.run()
   tg = ltg.learnTierGuide()
   assert(tg['speech'] == 'italianSpeech')
   assert(tg['morpheme'] == 'morphemes')
   assert(tg['morphemeGloss'] == 'morpheme-gloss')
   assert(tg['translation'] == 'english')
   with open('tierGuide.yaml', 'w') as outfile:
      yaml.dump(tg, outfile, default_flow_style=False)
   tg2 = yaml.safe_load(open("tierGuide.yaml"))
   tgKeys = list(tg.keys())
   tgKeys.sort()
   tg2Keys = list(tg2.keys())
   tg2Keys.sort()
   assert(tgKeys == tg2Keys)
   os.remove("tierGuide.yaml")
   
     #---------------------------------------------------------------
     # second, an eaf with just one time-aligned tier, just one child
     #---------------------------------------------------------------

   print("    01RuthNora230503Slexil")
   f = "../explore/aliceTaff/01/01RuthNora230503Slexil.eaf"
   ltg = LearnTierGuide(f, verbose=False)
   ltg.parser.run()
   tg = ltg.learnTierGuide()
   assert(tg['speech'] == 'utterance')
   assert(tg['translation'] == 'translation')

     #---------------------------------------------------------------
     # third, another standard IJAL 4-tier line, one time-aligned,
     # morpheme-gloss, specified as child of the morpheme tier
     #---------------------------------------------------------------

   f = "../explore/daylight/beckAndHess/beckAndHess.eaf"
   print("    daylight, beckAndHess.eaf")
   ltg = LearnTierGuide(f, verbose=False)
   ltg.parser.run()
   ltg = LearnTierGuide(f, verbose=False)
   ltg.parser.run()
   tg = ltg.learnTierGuide()

   assert(tg['speech'] == 'lushootseed')
   assert(tg['morpheme'] == 'morphemes')
   assert(tg['morphemeGloss'] == 'morphemeGloss')
   assert(tg['translation'] == 'english')

#----------------------------------------------------------------------------------------------------
def test_learnTierGuide_novelTierName():

   print("--- test_learnTierGuide_novelTierName")
    
   f = "../explore/lushootseed/grammars/grammar1-withNovelTier.eaf"
   ltg = LearnTierGuide(f, verbose=False)
   ltg.parser.run()
   tg = ltg.learnTierGuide()

#---------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    runTests()
