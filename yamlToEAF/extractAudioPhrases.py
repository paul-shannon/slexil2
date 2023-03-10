import re
import sys
import os.path

sys.path.append("/Users/paul/github/slexil2/slexil")
if(len(sys.argv) != 4):
    print("usage: extractAudioPhrases.py <audio.wav> <out.eaf> <targetDirectory>")
    sys.exit(0)

audioFile = sys.argv[1]
assert(os.path.exists(audioFile))

eafFile = sys.argv[2]
assert(os.path.exists(eafFile))

targetDirectory = sys.argv[3]
assert(os.path.exists(targetDirectory))

from audioExtractor import *

ea = AudioExtractor(audioFile, eafFile, targetDirectory)
ea.extract(quiet=False)
