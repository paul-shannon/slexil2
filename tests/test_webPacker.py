import unittest
import re
import os
import pdb
import slexil
from slexil.webPacker import WebPacker

# baseDir = os.path.dirname(slexil.__file__)

class TestWebPacker(unittest.TestCase):

        def test_ctor(self):
                print("--- running TestWebPacker.test_ctor")
                packer = WebPacker()
                cssFiles = packer.getCSSFilenames()
                assert(len(cssFiles) == 3)
                jsFiles = packer.getJSFilenames()
                assert(len(jsFiles) == 6)

        def test_readCSS(self):
                print("--- running TestWebPacker.test_readCSS")
                packer = WebPacker()
                packer.readCSS()
                cssText = packer.getCSSText()
                assert(len(cssText) > 20000)
                openTags = [m.start() for m in re.finditer("<style>", cssText)]
                closeTags = [m.start() for m in re.finditer("</style>", cssText)]
                assert(len(openTags) == 3)
                assert(len(closeTags) == 3)

        def test_readJS(self):
                print("--- running TestWebPacker.test_readJS")
                packer = WebPacker()
                packer.readJS()
                jsText = packer.getJSText()
                len(jsText)
                openTags = [m.start() for m in re.finditer("<script>", jsText)]
                closeTags = [m.start() for m in re.finditer("</script>", jsText)]
                assert(len(openTags) >= 5)
                assert(len(closeTags) >= 5)

        def test_noTextJustURLs(self):
                print("--- running TestWebPacker.test_noTextJustURLs")
                packer = WebPacker(fullText=False)
                assert(len(packer.getCSSText()) == 273)
                assert(len(packer.getJSText()) == 517)

if __name__ == '__main__':
                unittest.main()
