import argparse
from slexil.eafParser import EafParser
import argparse
import os, sys
from pathlib import Path
import xmlschema
from lxml import etree
import yaml
import pdb

parser = argparse.ArgumentParser(prog='eaf2html.py',
          description='creates yaml version of eaf xml')

parser.add_argument('--eaf', type=str, required=True)
parser.add_argument('--title', type=str, default="title")
parser.add_argument('--narrator', type=str, default="narrator")
parser.add_argument('--textEntry', type=str, default="textEntryBy X")
parser.add_argument('--outputDir', type=str, default="./")


args = parser.parse_args()
eaf = args.eaf
title = args.title
narrator = args.narrator
textEntry = args.textEntry
outputDir = args.outputDir
outputFile = "%s/%s.yaml" % (outputDir, Path(eaf).stem)


p = EafParser(eaf, verbose=False, fixOverlappingTimeSegments=False)
p.run()
yamlText = p.toYAML(title, narrator, textEntry)
p.writeYAML(yamlText, outputFile)
print("wrote %s" % outputFile)


