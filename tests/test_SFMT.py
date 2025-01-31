from slexil.sfmt import *
import pdb
import os, sys
#--------------------------------------------------------------------------------
def test_ctor():

   print("--- test_ctor")

   f = "../testData/validEafYamlFiles/inferno-withHtmlLines.yaml"
   sfmt = SFMT(f)
   assert(sfmt.lastLine == 45)
   assert(len(sfmt.getRawLines()) == 46)

#--------------------------------------------------------------------------------   
def test_parse():
    
   print("--- test_parse")

   f = "../testData/validEafYamlFiles/inferno-withHtmlLines.yaml"
   sfmt = SFMT(f)
   sfmt.parse()

   assert(sfmt.startLines == [11, 18, 31])
   assert(sfmt.endLines == [12, 19, 32])
   assert(sfmt.blankLines == [4, 6, 8, 10, 17, 24, 26, 28, 30, 37])

   assert(sfmt.htmlLines == [7, 9, 25, 27, 29, 38])

#--------------------------------------------------------------------------------   
def test_identifyTierBlocks():

   print("--- test_identifyTierBlocks")
   f = "../testData/validEafYamlFiles/inferno-withHtmlLines.yaml"
   sfmt = SFMT(f)
   sfmt.parse()

   assert(sfmt.blockStarts == [11, 18, 31])
   assert(sfmt.blockEnds == [17, 24, 37])

   assert(sfmt.getTierCount() == 3)
   
#--------------------------------------------------------------------------------   
def test_getTierTable():

   print("--- test_getTierTable")
   f = "../testData/validEafYamlFiles/inferno-withHtmlLines.yaml"
   sfmt = SFMT(f)
   sfmt.parse()
   tbl = sfmt.getTierTable()
   assert(tbl.shape == (4,2))
   assert(list(tbl.columns) == ["Field", "Lines"])
   assert(tbl.loc[3]['Lines'])

#--------------------------------------------------------------------------------   
def test_getTier():

   print("--- test_getTier")
   f = "../testData/validEafYamlFiles/inferno-withHtmlLines.yaml"
   sfmt = SFMT(f)
   sfmt.parse()

   assert(sfmt.blockStarts == [11, 18, 31])
   assert(sfmt.blockEnds == [17, 24, 37])

   assert(sfmt.getTierCount() == 3)

   tier = sfmt.getTier(0)
   keys = [key for key in tier]
   expected = ['startTime', 'endTime', 'italianSpeech', 'morphemes',
               'morpheme-gloss', 'english']
   assert(keys == expected)
   assert(tier['startTime'] == 0)
   assert(tier['endTime'] == 2828)
   assert(tier['italianSpeech'] == 'Nel mezzo del cammin di nostra vita')
   assert(tier['morphemes'] ==  ['en=il','mezz–o','de=il','cammin–Ø','di','nostr–a','vit–a'])
   assert(tier['morpheme-gloss'] ==
          ['in=DEF:MASC:SG','middle-MASC:SG','of=DEF:MASC:SG','journey–MASC:SG','of','our-FEM:SG','life-FEM'])
   assert(tier['english'] == 'Midway upon the journey of our life')

#--------------------------------------------------------------------------------   
def test_getTiers():

   print("--- test_getTiers")
   f = "../testData/validEafYamlFiles/inferno-withHtmlLines.yaml"
   sfmt = SFMT(f)
   sfmt.parse()
   tiers = sfmt.getTiers()
   assert(len(tiers) == 3)

   f = "../testData/validEafYamlFiles/inferno-heterogeneousTiers.yaml"
   sfmt = SFMT(f)
   sfmt.parse()
   tiers = sfmt.getTiers()
   assert(len(tiers) == 3)
   assert("speaker" in list(tiers[2].keys()))  # last line in last tier

#--------------------------------------------------------------------------------   
def test_inferTierStructure():

   print("--- test_inferTierStructure")
   
#--------------------------------------------------------------------------------   
def test_getHtml():

   print("--- test_getHtml")
   f = "../testData/validEafYamlFiles/inferno-withHtmlLines.yaml"
   
   sfmt = SFMT(f)
   sfmt.parse()
    
   assert(len(sfmt.htmlLines) == 6)
   traceFileName = "test_SFMT.py"
   traceLineNumber = 103
   print("--- trace: %s at %d" % (traceFileName, traceLineNumber))

   assert(sfmt.getHtml(0) == '<h3> Read by Roberto Begnini</h3>')
   
   html = sfmt.getHtml(5)
   expected = "<div style='margin: 30px'><h6> a multi-line html element</h6>        " + \
              "   <ul>             <li> item one             <li> item two     " + \
              "        <li> item three           </ul>           </div>"
   assert(html == expected)

   traceFileName = "test_SFMT.py"
   traceLineNumber = 113
   print("--- trace: %s at %d" % (traceFileName, traceLineNumber))

   allHtml = sfmt.getAllHtml()
   assert(len(allHtml) == 6)
   print(allHtml[0])
   assert(allHtml[1] == 'taken from youtube')
    
#--------------------------------------------------------------------------------   
def test_getOrderedLineObjectsTieredAndHTML():

   print("--- test_getOrderedLineObjectsTieredAndHTML")

   f = "../testData/validEafYamlFiles/inferno-withHtmlLines.yaml"
   sfmt = SFMT(f)
   sfmt.parse()

   tbl = sfmt.getOrderedLineObjectsTieredAndHTML()

   assert(tbl.shape == (9,3))
   assert(list(tbl.columns) == ['type', 'rawIndex', 'signature'])

   expected = ["html", "html", "tier", "tier", "html", "html", "html", "tier", "html"]
   assert(list(tbl['type']) == expected)

   expected = [7, 9, 11, 18, 25, 27, 29, 31, 38]
   assert(list(tbl['rawIndex']) == expected)

   assert(tbl.loc[0]['signature'] == "<h3> Read by Roberto Begnini</h3>")
   assert(tbl.loc[1]['signature'] == "taken from youtube")
   assert(tbl.loc[2]['signature'] == "0")
   assert(tbl.loc[3]['signature'] == "3095")
   assert(tbl.loc[4]['signature'] == "<div style='margin: 30px'><h6> another line</h6></div>")
   assert(tbl.loc[5]['signature'] == "<div style='margin: 30px'><h6> another line</h6></div>")
   assert(tbl.loc[6]['signature'] == "<div style='margin: 30px'><h6> another line</h6></div>")
   assert(tbl.loc[7]['signature'] == "5624")
   assert(tbl.loc[8]['signature'] == "<div style='margin: 30px'><h6> a multi-line html element</h6>")
          

#--------------------------------------------------------------------------------   
def test_getTimeTable():

   print("--- test_getTimeTable")

   f = "../testData/validEafYamlFiles/inferno.yaml"
   sfmt = SFMT(f)

   tbl = sfmt.getTimeTable()
   
   assert(tbl.shape == (3, 2))
   assert(tbl['start'].tolist() == [0,3095,5624])
   assert(tbl['end'].tolist() == [2828, 5500, 8033])

#--------------------------------------------------------------------------------   
def test_lineDictToTable():

   print("--- test_lineDictToTable")
   f = "../testData/validEafYamlFiles/inferno.yaml"
   sfmt = SFMT(f)
   sfmt.parse()
   #assert(len(sfmt.getLines()) == 9)
   assert(len(sfmt.getHtmlLines()) == 6)
   assert(len(sfmt.getTieredLines()) == 3)
   line = sfmt.getTieredLines()[1]
   assert(isinstance(line, dict))

#----------------------------------------------------------------------------------------------------
def test_getTierGuide():

   print("--- test_getTierGuide")

   f = "../testData/validEafYamlFiles/inferno.yaml"
   ftg = "../testData/validEafYamlFiles/infernoTierGuide.yaml"
   yp = NewYamlParser(f, ftg)
   info = yp.getTierGuide()
   keys = list(info.keys())
   values = list(info.values())
   assert(keys == ['speech', 'analysis_1', 'analysis_2', 'tier_1'])
   assert(values == ['italianSpeech', 'morphemes', 'morpheme-gloss', 'english'])
    
#----------------------------------------------------------------------------------------------------
def test_getMetadata():

    print("--- test_getMetadata")

    f = "../testData/validEafYamlFiles/inferno.yaml"
    sfmt = SFMT(f)
    sfmt.parse()
    assert(sfmt.getTitle() == "Dante's Inferno")
    assert(sfmt.getSpeakers() == "Roberto Benigni")
    assert(sfmt.getTextEntry() == "Paul Shannon")
    
#----------------------------------------------------------------------------------------------------
def test_mediaGetters():

    print("--- test_mediaGetters: inferno audio")

    f = "../testData/validEafYamlFiles/inferno.yaml"
    sfmt = SFMT(f)

    expected = "https://slexildata.artsrn.ualberta.ca/misc/inferno-threeLines.wav"
    assert(sfmt.getAudioURL() == expected)
    assert(sfmt.getVideoURL() == None)
    assert(sfmt.getMimeType() == "audio/x-wav")
    assert(sfmt.getMediaURL() == expected)
    
    print("--- test_mediaGetters: tlingit video")

    f = "../testData/validEafYamlFiles/tlingitVan-2lines.yaml"
    sfmt = SFMT(f)

    expected = "https://slexildata.artsrn.ualberta.ca/tlingit/83VanRescue.m4v"
    assert(sfmt.getAudioURL() == None)
    assert(sfmt.getVideoURL() == expected)
    assert(sfmt.getMimeType() == "video/m4v")
    assert(sfmt.getMediaURL() == expected)

#----------------------------------------------------------------------------------------------------
def test_getAllTierNames():

    print("--- test_getAllTierNames")

    f = "../testData/validEafYamlFiles/inferno-withHtmlLines.yaml"
    sfmt = SFMT(f)
    sfmt.parse()
    
    x = sfmt.getAllTierNames()
    expected = ['italianSpeech', 'morphemes', 'morpheme-gloss', 'english']
    assert(x.sort() == expected.sort())

#----------------------------------------------------------------------------------------------------
def test_identifyAnalysisTiers():

    print("--- test_identifyAnalysisTiers")

    f = "../testData/validEafYamlFiles/inferno-heterogeneousTiers.yaml"
    sfmt = SFMT(f)
    sfmt.parse()

    analysisTiers = list(sfmt.getAnalysisTierNameMap().values())
    assert(analysisTiers.sort() == ['morphemes', 'morpheme-gloss'].sort())

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

    f = "../testData/validEafYamlFiles/61.yaml"
    sfmt = SFMT(f)
    tiers = sfmt.getGenericTierNameMap()

       # make sure that Speaker initials comes last

    assert(tiers == {'tier_1': 'translation', 'tier_2': 'Speaker initials'})
    assert(list(tiers.values()) == ['translation', 'Speaker initials'])

    f = "../testData/validEafYamlFiles/inferno-heterogeneousTiers.yaml"
    sfmt = SFMT(f)
    tiers = sfmt.getGenericTierNameMap()
    assert(tiers == {'tier_1': 'soundsLike', 'tier_2': 'english', 'tier_3': 'speaker'})
    assert(list(tiers.values()) == ['soundsLike', 'english', 'speaker'])

#----------------------------------------------------------------------------------------------------
def test_getSpeechTier():

    print("--- test_getSpeechTier")

    f = "../testData/validEafYamlFiles/inferno-heterogeneousTiers.yaml"
    sfmt = SFMT(f)
    
    stMap = sfmt.getSpeechTierNameMap()
    assert(stMap == {'speech': 'italianSpeech'})

       # here's how to get the tier names and values
    assert(list(stMap.keys()) == ['speech'])
    assert(list(stMap.values()) == ['italianSpeech'])

#----------------------------------------------------------------------------------------------------
def test_getGenericTiers():

    print("--- test_getGenericTiers")

    f = "../testData/validEafYamlFiles/inferno-heterogeneousTiers.yaml"
    sfmt = SFMT(f)
    gtMap = sfmt.getGenericTierNameMap()

       # check the generic tier map
    expected = ['tier_1', 'tier_2', 'tier_3', 'tier_4']
    assert([tierName in gtMap.keys() for tierName in expected])
    expected = ['soundsLike', 'english', 'speaker', 'italianSpeech']
    assert([tierValue in gtMap.values() for tierValue in expected])

#----------------------------------------------------------------------------------------------------
def test_getAnalysisTiers():

    print("--- test_getAnalysis")

    f = "../testData/validEafYamlFiles/inferno-heterogeneousTiers.yaml"
    sfmt = SFMT(f)
    atMap = sfmt.getAnalysisTierNameMap()
    expected = {'analysis_1': 'morphemes', 'analysis_2': 'morpheme-gloss'}
    assert(atMap == expected)

#----------------------------------------------------------------------------------------------------
def test_recognizeAbsentAnalysisTiers():

    print("--- test_recognizeAbsentAnalysisTiers")

    f = "../testData/validEafYamlFiles/inferno-noAnalysisTiers.yaml"
    sfmt = SFMT(f)
    assert(sfmt.getAllTierNames() == ['italianSpeech', 'soundsLike', 'english', 'speaker'])
    assert(sfmt.getGenericTierNameMap() ==
           {'tier_1': 'soundsLike', 'tier_2': 'english', 'tier_3': 'speaker'})
    assert(sfmt.getAnalysisTierNameMap() == {})

#----------------------------------------------------------------------------------------------------
# resurrect this later if needed
def test_writeTierGuide():

    print("--- test_writeTierGuide")

    f = "../testData/validEafYamlFiles/inferno-heterogeneousTiers.yaml"
    sfmt = SFMT(f)
    #yamlFile = "/tmp/tierGuide.yaml"
    #sfmt.writeTierGuide(yamlFile)
    # x = yaml.load(open(yamlFile), Loader=yaml.FullLoader)
    # assert(x['speech'] == 'italianSpeech')
    # assert(x['tier_1'] == 'soundsLike')
    # assert(x['analysis_1'] == 'morphemes')
    # assert(x['analysis_2'] == 'morpheme-gloss')
    # assert(x['tier_2'] == 'english')
    # assert(x['tier_3'] == 'speaker')

#----------------------------------------------------------------------------------------------------
def test_getTierGuide():

    print("--- test_getTierGuide")

    f = "../testData/validEafYamlFiles/inferno-heterogeneousTiers.yaml"
    sfmt = SFMT(f)
    tg = sfmt.getTierGuide()
    assert(list(tg.keys()) ==
           ['speech', 'tier_1', 'analysis_1', 'analysis_2', 'tier_2', 'tier_3'])
    assert(tg["speech"] == "italianSpeech")
    assert(tg['tier_1'] == "soundsLike")
    assert(tg['analysis_1'] == "morphemes")
    assert(tg['analysis_2'] == "morpheme-gloss")
    assert(tg['tier_2'] == "english")
    assert(tg['tier_3'] == "speaker")

#----------------------------------------------------------------------------------------------------
def test_getTierGuide_fileHasSomeHtmlLines():

    print("--- test_getTierGuide_fileHasSomeHtmlLines")

    f = "../testData/validEafYamlFiles/inferno-withHtmlLines.yaml"
    sfmt = SFMT(f)
    tg = sfmt.getTierGuide()
    assert(list(tg.keys()) == ['speech', 'analysis_1', 'analysis_2', 'tier_1'])
    assert(tg["speech"] == "italianSpeech")
    assert(tg['analysis_1'] == "morphemes")
    assert(tg['analysis_2'] == "morpheme-gloss")
    assert(tg['tier_1'] == "english")

    assert(len(sfmt.getAllLines()) == 46)
    assert(len(sfmt.getTieredLines()) == 3)  # these are parsed from many into just 3 objects
    assert(len(sfmt.getHtmlLines()) == 6)

#----------------------------------------------------------------------------------------------------
def test_hawkBabyMissingTier():

   print("--- test_hawkBabyMissingTier")
   f = "../testData/validEafYamlFiles/HawkBaby231112.yaml"
   sfmt = SFMT(f)
   sfmt.parse()
   
   assert(len(sfmt.getTiers()) == 196)
   assert(sfmt.allTierNames == ['utterance', 'translation'])
   assert(sfmt.allAnalysisTierNames == [])
   assert(list(sfmt.getSpeechTierNameMap().values()) == ['utterance'])
          
#----------------------------------------------------------------------------------------------------
def runTests():

   test_getTierTable()
   sys.exit(0)
   
   test_hawkBabyMissingTier()

   test_ctor()
   test_parse()
   test_identifyTierBlocks()
   test_getTier()
   test_getTiers()
   test_getHtml()
   test_getOrderedLineObjectsTieredAndHTML()
   test_getTimeTable()
   test_lineDictToTable()

   test_mediaGetters()
   test_getMetadata()
   
   test_getAllTierNames()
   test_identifyAnalysisTiers()
   test_getSpeechTier()
   test_getGenericTiers()
   test_getGenericTiers_inProperOrder()
   test_getAnalysisTiers()
   test_getTierGuide()
   test_getTierGuide_fileHasSomeHtmlLines()
   test_recognizeAbsentAnalysisTiers()
   test_getOrderedLineObjectsTieredAndHTML()

   #test_writeTierGuide()

#----------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    runTests()
   
