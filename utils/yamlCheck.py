import sys, pdb
import yaml

if not len(sys.argv) == 2:
    print("usage: python yamlCheck.py <eafFile>")
    sys.exit(1)

f = sys.argv[1]
x = yaml.load(open(f), Loader=yaml.FullLoader)
pdb.set_trace()
print(list(x.keys()))
print(len(x['lines']))


