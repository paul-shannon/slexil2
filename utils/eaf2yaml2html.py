# eaf2yaml2html.py

import sys, os, pdb
from pathlib import Path

if (len(sys.argv) != 2):
    print("usage: python eaf2yaml2html.py <eafFile> or <lists.txt>")
    sys.exit(1)

file = sys.argv[1]
fileStem = Path(file).stem
fileExtension = Path(file).suffix

assert(fileExtension in [".eaf", ".txt"])

if fileExtension == ".txt":
    f = open(file)
    eafFiles = f.readlines()
    eafFiles = [f.rstrip() for f in eafFiles]
      # eliminate comment lines:
    eafFiles = [f for f in eafFiles if f.find("#") < 0]
    eafFiles = [f for f in eafFiles if len(f.strip()) > 5]
else:
    eafFiles = [file]

outputDir = "testResults"

for eafFile in eafFiles:

   try:
      print(); print();
      print("--- eaf2yaml2html %s" % eafFile, flush=True)
      print()
      cmd1 = "python eaf2yaml.py --eaf %s --outputDir %s" % (eafFile, outputDir)
      print("cmd1: %s" % cmd1)
      status1 = os.system(cmd1)
   
      yamlFile = "%s/%s.yaml" % (outputDir, Path(eafFile).stem)
      if os.path.isfile(yamlFile):
         cmd2 = "python yaml2html.py --yaml %s --outputDir %s" % (yamlFile, outputDir)
         print("cmd2: %s" % cmd2)
         status2 = os.system(cmd2)

   except Exception as ex:
       print(ex)

    
