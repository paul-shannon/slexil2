import re
import sys, os
from copy import deepcopy
from slexil.practiceLists import PracticeLists

import pdb
import yaml
import yattag
import pandas as pd

pd.set_option('display.width', 1000)
pd.set_option('display.max_columns', None)
#--------------------------------------------------------------------------------
def runTests():

   test_ctor()
   test_getJavascript()
   test_addHTML()
   test_randomizeWithinLists()

#--------------------------------------------------------------------------------
def test_ctor():

  print("--- test_ctor")

  dataDir = os.path.join("..", "testData", "practiceLists")
  f = os.path.join(dataDir, "daylight.yaml")

  pl = PracticeLists(f)
  assert(type(pl).__name__ == 'PracticeLists')

  cats = pl.getCategories()
  assert(cats==['firstFive', 'thirdFive'])
  assert(pl.getList('firstFive') == [1,2,3,4,5])
  assert(pl.getList('thirdFive') == [11,12,13,14,15])
  
#--------------------------------------------------------------------------------
def test_getJavascript():

  print("--- test_getJavascript")

  dataDir = os.path.join("..", "testData", "practiceLists")
  f = os.path.join(dataDir, "daylight.yaml")
  pl = PracticeLists(f)
  js = pl.getJavascript()
  expected = '\n<script>\nwindow.practiceLists = {"firstFive": [1, 2, 3, 4, 5], "thirdFive": [11, 12, 13, 14, 15]}\n</script>'
  assert(js == expected)

#--------------------------------------------------------------------------------
def test_addHTML():

  print("--- test_addHTML")

  dataDir = os.path.join("..", "testData", "practiceLists")
  f = os.path.join(dataDir, "daylight.yaml")
  pl = PracticeLists(f)

  htmlDoc = yattag.Doc()
  pl.addHTML(htmlDoc)
  html = htmlDoc.getvalue()
  expected = '<div id="practiceDiv"><button id="practice-firstFive" class="practiceButton">firstFive</button><button id="practice-thirdFive" class="practiceButton">thirdFive</button></div>'
  assert(html == expected)

#--------------------------------------------------------------------------------
def test_randomizeWithinLists():

  print("--- test_randomizeWithinLists")

  dataDir = os.path.join("..", "testData", "practiceLists")
  f = os.path.join(dataDir, "daylight.yaml")
  pl = PracticeLists(f)
  categories = pl.getCategories()
  assert(len(categories) >= 2)
  x0 = pl.getList(categories[0])
  x1 = pl.getList(categories[1])
  x0c = deepcopy(x0)
  x1c = deepcopy(x1)
  pl.randomizeWithinLists()
  x0r = pl.getList(categories[0])
  x1r = pl.getList(categories[1])

  assert(x0c != x0r)
  assert(x1c != x1r)

#--------------------------------------------------------------------------------
if __name__ == '__main__':
    runTests()
