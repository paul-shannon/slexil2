import sys, os, pdb
from pathlib import Path


eafFile = "try.txt"
f = open(eafFile)
eafs = f.readlines()
eafs = [f.rstrip() for f in eafs]
eafs = [f for f in eafs if f.find("#") < 0]
eafs = [f for f in eafs if len(f.strip()) > 5]
#eafs = [Path(f).stem for f in eafs]
eafs = list(set(eafs))
len(eafs)  # 294

htmls = os.listdir("testResults")
htmls = [f for f in htmls if Path(f).suffix == ".html"]
htmls = [Path(f).stem for f in htmls]
len(htmls) # 268


keepers = [eaf for eaf in eafs if Path(eaf).stem in htmls]
len(keepers)  # successful transformation from eaf to yaml to html
failures = [eaf for eaf in eafs if Path(eaf).stem not in htmls]
len(failures) # 26
for failure in failures:
    print("%s" % failure)
    
