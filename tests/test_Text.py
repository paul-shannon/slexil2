import re
import sys
sys.path.append("../slexil")
from text import *
import importlib
import os
import pdb
import tempfile
#----------------------------------------------------------------------------------------------------
pd.set_option('display.width', 1000)
#----------------------------------------------------------------------------------------------------
def runTests(display=False):

    #test_inferno(display)
    test_tlingitVideo(display)

#----------------------------------------------------------------------------------------------------
def test_inferno(display):

    print("--- test_inferno")

    audioFilename = "../testData/inferno/inferno-threeLines.wav"
    elanXmlFilename="../testData/inferno/inferno-threeLines.eaf"
    targetDirectory = "audio"
    projectDirectory="infernoProject"
    tierGuideFile="../testData/inferno/tierGuide.yaml"
    grammaticalTermsFile="../testData/inferno/grammaticalTerms.txt"

    text = Text(elanXmlFilename, audioFilename, grammaticalTermsFile, tierGuideFile,
                projectDirectory, quiet=True)
    assert(text.validInputs())
    x = text.getTierSummary()
    assert(x.shape == (5,3))
    x = text.getMediaInfo()
    #assert(x["url"] == 'file://inferno-threeLines.wav')
    assert(x["url"] == 'http://localhost:60050/slexil/inferno-threeLines.wav')

    assert(x["mimeType"] == 'audio/x-wav')

       # make sure start and end times have been extracted into a pandas dataframe
    times = text.determineStartAndEndTimes()
    assert(times.shape == (3,5))
    expected = ['lineID', 'start', 'end', 't1', 't2']
    assert([str(colname) for colname in times.columns] == expected)
    endTimes = [e for e in times.loc[:, "end"]]
    assert(endTimes == [3093, 5624, 8033])

    htmlText = indent(text.toHTML())

    display = True;
    if(display):
        filename = "inferno.html"
        htmlFile = open(filename, "w")
        try:
            htmlFile.write(htmlText) #, "utf-8"))
            htmlFile.close()
        finally:
            print("opening %s in browser" % filename)
            os.system("open %s" % filename)


#----------------------------------------------------------------------------------------------------
def test_tlingitVideo(display):

    print("--- test_tlingitVideo")

    audioFilename = "../testData/inferno/inferno-threeLines.wav"
    elanXmlFilename="../testData/videoDemo/tlingit-video-demo.eaf"
    targetDirectory = "audio"
    projectDirectory="tlingitVideoProject"
    tierGuideFile="../testData/videoDemo/tierGuide.yaml"
    grammaticalTermsFile="../testData/videoDemo/grammaticalTerms.txt"

    text = Text(elanXmlFilename, audioFilename, grammaticalTermsFile, tierGuideFile,
                projectDirectory, quiet=True)
    assert(text.validInputs())
    x = text.getTierSummary()
    assert(x.shape == (3,3))
    x = text.getMediaInfo()

    assert(x["url"] == 'https://igv-data.systemsbiology.net/slexil/1RuthNora2Wide.m4v')

    assert(x["mimeType"] == 'video/m4v')

       # make sure start and end times have been extracted into a pandas dataframe
    times = text.determineStartAndEndTimes()
    assert(times.shape == (168,5))
    expected = ['lineID', 'start', 'end', 't1', 't2']
    assert([str(colname) for colname in times.columns] == expected)
    endTimes = [e for e in times.loc[:, "end"]]
    assert(endTimes[0:5] == [5090, 7530, 9782, 11727, 12821])

    htmlText = indent(text.toHTML())

    display = True;
    if(display):
        filename = "videoDemo.html"
        htmlFile = open(filename, "w")
        try:
            htmlFile.write(htmlText) #, "utf-8"))
            htmlFile.close()
        finally:
            print("opening %s in browser" % filename)
            os.system("open %s" % filename)


#----------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    display = False
    if(len(sys.argv) == 2 and sys.argv[1] == "display"):
        display = True
    runTests(display)
