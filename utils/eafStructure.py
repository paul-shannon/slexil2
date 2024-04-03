import argparse
parser = argparse.ArgumentParser(prog='eafStructure.py',
                                 description='access to the parsed eaf tables')

parser.add_argument('--eaf', type=str, required=True)
args = parser.parse_args()
eafFile = args.eaf

import pandas as pd
pd.set_option('display.width', 1000)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

from slexil.eafParser import EafParser
parser = EafParser(eafFile, verbose=True, fixOverlappingTimeSegments=False)
tbl = parser.getTierTable()
tblTimes = parser.getTimeTable()
# parser.parseAllLines()
x = parser.getAllLinesTable()  # a list of time-ordered line tables
print("parsed %d lines into variable x" % len(x))
print("tier table in variable tbl, %d rows" % tbl.shape[0])
print("time table in variable tblTimes, %d rows" % tblTimes.shape[0])

