import re
import sys
sys.path.append("../slexil")
from eafParser import *
#----------------------------------------------------------------------------------------------------
pd.set_option('display.width', 1000)
#----------------------------------------------------------------------------------------------------
def runTests(display=False):

    test_ctor()
    test_extractStartAndStopTimes()

#----------------------------------------------------------------------------------------------------
def test_ctor():

    print("--- test_ctor")

    elanXmlFilename="../testData/inferno/inferno-threeLines.eaf"
    p = EAFParser(elanXmlFilename)
    assert(p.getFilename() == elanXmlFilename)

#----------------------------------------------------------------------------------------------------
def test_extractStartAndStopTimes():

    print("--- test_extractStartAndStopTimes")

    elanXmlFilename="../testData/inferno/inferno-threeLines.eaf"
    p = EAFParser(elanXmlFilename)
    p.extractStartAndEndTimes()
    tbl = p.getPandasTable()

    assert(tbl.ndim == 2)
    assert(tbl.shape == (3,5))  # 3 rows, 5 columns

    expected = ['lineID', 'start', 'end', 't1', 't2']
    assert([str(colname) for colname in tbl.columns] == expected)

    starts = [e for e in tbl.loc[:, "start"]]
    assert(starts == [0, 3093, 5624])

    ends = [e for e in tbl.loc[:, "end"]]
    assert(ends == [3093, 5624, 8033])

    t1s = [e for e in tbl.loc[:, "t1"]]
    t2s = [e for e in tbl.loc[:, "t2"]]
    assert(t1s == ['ts1', 'ts2', 'ts3'])
    assert(t2s == ['ts2', 'ts3', 't4'])

    stringifiedTable = p.getStringifiedStartStopTable()
    expected = '0,start,end,lineID\n1,0,3093,a1\n2,3093,5624,a2\n3,5624,8033,a3'
    assert(stringifiedTable == expected)
    
#----------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    runTests()
