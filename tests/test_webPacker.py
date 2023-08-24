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
		assert(len(cssFiles) == 2)
		jsFiles = packer.getJSFilenames()
		assert(len(jsFiles) == 5)

	def test_readCSS(self):
		print("--- running TestWebPacker.test_readCSS")
		packer = WebPacker()
		packer.readCSS()
		cssText = packer.getCSSText()
		assert(len(cssText) > 20000)
		openTags = [m.start() for m in re.finditer("<style>", cssText)]
		closeTags = [m.start() for m in re.finditer("</style>", cssText)]
		assert(len(openTags) == 2)
		assert(len(closeTags) == 2)

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
		expected = "https://slexilData.artsrn.ualberta.ca/includes/bootstrap.min.css\nhttps://slexilData.artsrn.ualberta.ca/includes/slexil.css\n"
		assert(packer.getCSSText() == expected)
		expected = "https://slexilData.artsrn.ualberta.ca/includes/showdown.min.js\nhttps://slexilData.artsrn.ualberta.ca/includes/jquery-3.6.3.min.js\nhttps://slexilData.artsrn.ualberta.ca/includes/slexil.js\nhttps://slexilData.artsrn.ualberta.ca/includes/bootstrap.bundle.min.js\nhttps://slexilData.artsrn.ualberta.ca/includes/annotations.js\n"
		assert(packer.getJSText() == expected)

if __name__ == '__main__':
		unittest.main()
