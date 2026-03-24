import unittest
import re
import os
import pdb
import slexil
from slexil.webPacker import WebPacker
#--------------------------------------------------------------------------------
def test_ctor():

   print("--- running TestWebPacker.test_ctor")
   packer = WebPacker()
   cssFiles = packer.getCSSFilenames()
   jsFiles = packer.getJSFilenames()
   assert(len(cssFiles) == 4)
   assert(len(jsFiles) == 8)

#--------------------------------------------------------------------------------
def test_readCSS():

   print("--- running TestWebPacker.test_readCSS")
   packer = WebPacker()
   packer.readCSS()
   cssText = packer.getCSSText()
   assert(len(cssText) > 20000)
   openTags = [m.start() for m in re.finditer("<style>", cssText)]
   closeTags = [m.start() for m in re.finditer("</style>", cssText)]
   assert(len(openTags) == 4)
   assert(len(closeTags) == 4)

#--------------------------------------------------------------------------------
def test_readJS():

   print("--- running TestWebPacker.test_readJS")
   packer = WebPacker()
   packer.readJS()
   jsText = packer.getJSText()
   len(jsText)
   openTags = [m.start() for m in re.finditer("<script>", jsText)]
   closeTags = [m.start() for m in re.finditer("</script>", jsText)]
   assert(len(openTags) >= 5)
   assert(len(closeTags) >= 5)

#--------------------------------------------------------------------------------
def test_noTextJustURLs():

   print("--- running TestWebPacker.test_noTextJustURLs")
   packer = WebPacker(fullText=False)
   assert(len(packer.getCSSText()) == 372)
   assert(len(packer.getJSText()) == 693)

#--------------------------------------------------------------------------------
def runTests():
        
   test_ctor()
   test_readCSS()
   test_readJS()
   test_noTextJustURLs()
   
#--------------------------------------------------------------------------------
if __name__ == '__main__':
  runTests()
