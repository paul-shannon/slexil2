import sys
import pdb
from slexil.sfmt import *
assert(len(sys.argv) == 2)

f = sys.argv[1]
sfmt = SFMT(f)
sfmt.parse()
tiers = sfmt.getTiers()

tbl = sfmt.getTimeTable()
print("dim(tbl)")
print(tbl.shape)
rows = tbl.shape[0]
for i in range(rows-1):
    end = int(tbl.iloc[[i]]['end'])
    nextStart = int(tbl.iloc[[i+1]]['start'])
    delta = nextStart - end
    if(delta < 200):
       print("%d: %d-%d -> %d" % (i+1, end, nextStart, delta))
       if 'translation' in tiers[i].keys():
          print(tiers[i]['translation'])
       else:
          print(tiers[i]['utterance'])
       # pdb.set_trace()
    


