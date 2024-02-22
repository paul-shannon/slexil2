import argparse
import os, sys, pdb
from slexil.eafParser import EafParser
import pandas as pd
pd.set_option('display.max_rows', 1000)
#----------------------------------------------------------------------------------------------------
parser = argparse.ArgumentParser(prog='eafCheck.py',
          description='creates interactive webpage from eaf xml')

parser.add_argument('--eaf', type=str, required=True)
parser.add_argument('--times', action="store_true")
args = parser.parse_args()
eafFile = args.eaf
checkTimes = args.times
#----------------------------------------------------------------------------------------------------
parser = EafParser(eafFile, verbose=False, fixOverlappingTimeSegments=False)

if(checkTimes):
   tbl = parser.getTimeTable()
   rowCount = tbl.shape[0]
   print("--- %d rows" % rowCount)
   starts = list(tbl["start"])
   ends = list(tbl["end"])
   durations = [int(1 + end - start) for start, end in zip(starts, ends)]
      # remove the first start and the last end
   del starts[0]
   del ends[-1]
   nextGap = [int(start - end) for start, end in zip(starts, ends)]
   nextGap.append(0)
   tbl.insert(5, "duration", durations)
   tbl.insert(6, "nextGap", nextGap)
   print(tbl.to_string())

   
    
