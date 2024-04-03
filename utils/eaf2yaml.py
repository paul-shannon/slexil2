import argparse
from slexil.eafParser import EafParser
import argparse
import os, sys
import xmlschema
from lxml import etree
import yaml
import pdb

parser = argparse.ArgumentParser(prog='eaf2html.py',
          description='creates yaml version of eaf xml')

parser.add_argument('--eaf', type=str, required=True)
parser.add_argument('--title', type=str, required=True)
parser.add_argument('--narrator', type=str, required=True)
parser.add_argument('--textEntry', type=str, required=True)
parser.add_argument('--outputFile', type=str, required=True)
args = parser.parse_args()
eaf = args.eaf
title = args.title
narrator = args.narrator
textEntry = args.textEntry
outputFile = args.outputFile

p = EafParser(eaf, verbose=False, fixOverlappingTimeSegments=False)
p.toYAML(title, narrator, textEntry, outputFile)
