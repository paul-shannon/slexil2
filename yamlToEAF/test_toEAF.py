# test_toEAF.py
#----------------------------------------------------------------------------------------------------
import re
import sys
sys.path.append("..")
from audioExtractor import *
#----------------------------------------------------------------------------------------------------
def runTests():

    test_makestartStopTable()

def test_makestartStopTable():

    print("--- test_makestartStopTable")
    ea = AudioExtractor("../testData/harryMosesDaylight/daylight_1_4.wav",
                        "../testData/harryMosesDaylight/daylight_1_4.eaf",
                        "../testData/harryMosesDaylight/audioPhrases")
    ea.extract()
    # print(tbl)


if __name__ == '__main__':
    runTests()

