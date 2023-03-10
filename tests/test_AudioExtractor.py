# test_AudioExtractor.py
#----------------------------------------------------------------------------------------------------
import re
import sys
sys.path.append("../slexil")

from audioExtractor import *
#----------------------------------------------------------------------------------------------------
def runTests():

    test_constructor()
    test_determineStartAndEndTimes()
    test_extraction()

#----------------------------------------------------------------------------------------------------
def test_constructor():

    print("--- test_constructor")

    ea = AudioExtractor("../testData/inferno/inferno-threeLines.wav",
                        "../testData/inferno/inferno-threeLines.eaf",
                        "../testData/audio-tmp")
    assert(ea.validInputs)

#----------------------------------------------------------------------------------------------------
def clearAudioDirectory(targetDirectory):

    fileList=os.listdir(targetDirectory)

    for f in fileList:
        os.remove(os.path.join(targetDirectory,f))

#----------------------------------------------------------------------------------------------------
def test_determineStartAndEndTimes():

    print("--- test_determineStartAndEndTimes")

    ea = AudioExtractor("../testData/inferno/inferno-threeLines.wav",
                        "../testData/inferno/inferno-threeLines.eaf",
                        "../testData/audio-tmp")

    tbl = ea.determineStartAndEndTimes()
    assert(tbl.shape == (3, 5))   # just 3 lines
    assert(list(tbl.columns) == ["lineID", "start", "end", "t1", "t2"])
    (a3_start, a3_end) = tbl.loc[tbl['lineID'] == 'a3'][['start', 'end']].iloc[0].tolist()
    assert(a3_start == 5624)
    assert(a3_end == 8033)

#----------------------------------------------------------------------------------------------------
def test_extraction():

    print("--- test tierGuide-specific extraction")

    clearAudioDirectory("../testData/audio-tmp")

    ea = AudioExtractor("../testData/inferno/inferno-threeLines.wav",
                        "../testData/inferno/inferno-threeLines.eaf",
                        "../testData/audio-tmp")

    ea.extract(quiet=True)
    fileList = [f for f in os.listdir("../testData/audio-tmp") if not f.startswith('.')]
    fileList.sort()
    expected = ['a1.wav', 'a2.wav', 'a3.wav', 'inferno-threeLines.wav']
    assert(fileList == expected)

#----------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    runTests()
