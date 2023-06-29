from slexil.eafParser import EafParser
import pandas as pd
pd.set_option('display.width', 1000)
pd.set_option('display.max_columns', None)

eafFiles = open("../testData/eafFileList.txt").read().split('\n')
if(eafFiles[-1] == ""):
	del eafFiles[-1]

f = eafFiles[0]
parser = EafParser(f)
parser.constructTiersTable()
parser.constructTimeTable()
parser.parseAllLines()
x = parser.getAllLines()

len(x)

def sortFunction(tbl):
	print(tbl.loc[0])
	return(tbl.loc[0].startTime)

x.sort(reverse=False, key=sortFunction)
x[0]
x[1]
x[2]
