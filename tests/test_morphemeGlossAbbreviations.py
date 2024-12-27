# -*- tab-width: 3 -*-
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
import os, sys
import pdb
#-------------------------------------------------------------------------------
from slexil.morphemeGlossAbbreviations import MorphemeGlossAbbreviations
import pdb
#----------------------------------------------------------------------------------------------------
def test_simple():

    print("--- test_simple")
    mga = MorphemeGlossAbbreviations()
    assert(len(mga.getAll()) >= 1445)
    assert(len(mga.getAll()) <= 1600)

#----------------------------------------------------------------------------------------------------
def test_recognized():

    print("--- test_recognized")

    mga = MorphemeGlossAbbreviations()
    known = ["PROX", "SBJ", "SUBJ", "1PL"]
    map(mga.recognized, known)
    knownLower = [e.lower() for e in known]
    map(mga.recognized, knownLower)

    assert(not mga.recognized("fubar"))
    assert(not mga.recognized("FUBAR"))

#----------------------------------------------------------------------------------------------------
def test_lookup():

    print("--- test_lookup")

    mga = MorphemeGlossAbbreviations()

    assert(mga.lookup("ALTV") == "allative applicative")
    assert(mga.lookup("ALL") == "allative")
    assert(mga.lookup("ATV") == None)

    assert(mga.lookup("altv") == "allative applicative")
    assert(mga.lookup("all") == "allative")
    assert(mga.lookup("atv") == None)

      # a wikipedia entry, for which values were not (yet) extracted
    assert(mga.recognized("DPP"))
    assert(mga.lookup("DPP") == None)

#----------------------------------------------------------------------------------------------------
def runTests():

    test_simple()
    test_recognized()
    test_lookup()
    
    
#----------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    runTests()
