import sys, pdb, os
assert(len(sys.argv) == 2)

file = sys.argv[1]

print("remove speaker id lines from %s" % file)
f = open(file, "r")
lines = f.readlines()

speakerLineCount = 0
keeperLineCount = 0
newFileName = "tmp.yaml"
fNew = open(newFileName, "a")

for line in lines:
   if "speaker initials:" in line.lower():
       speakerLineCount += 1
if speakerLineCount == 0:
    print("\n *** no 'Speaker Initials' lines in %s, exiting\n" % file)
    sys.exit(0)
    
for line in lines:
   if not "speaker initials:" in line.lower():
      fNew.write(line)
      
print(" *** found %d speaker id lines" % speakerLineCount)
print(" *** wrote %d keeper lines" % keeperLineCount)
fNew.close()

os.rename(file, "%s-old" % file)
os.rename("tmp.yaml", file)
