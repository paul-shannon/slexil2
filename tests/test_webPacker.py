import unittest
import re
import os
import pdb
import slexil
from slexil.webPacker import WebPacker

baseDir = os.path.dirname(slexil.__file__)

class TestWebPacker(unittest.TestCase):

	def test_ctor(self):
		print("--- running TestWebPacker.test_ctor")
		packer = WebPacker(baseDir)
		cssFiles = packer.getCSSFilenames()
		assert(len(cssFiles) == 2)
		jsFiles = packer.getJSFilenames()
		assert(len(jsFiles) == 4)

	def test_readCSS(self):
		print("--- running TestWebPacker.test_readAll")
		packer = WebPacker(baseDir)
		packer.readCSS()
		cssText = packer.getCSSText()
		assert(len(cssText) > 20000)
		openTags = [m.start() for m in re.finditer("<style>", cssText)]
		closeTags = [m.start() for m in re.finditer("</style>", cssText)]
		assert(len(openTags) == 3)
		assert(len(closeTags) == 3)

	def test_readJS(self):
		print("--- running TestWebPacker.test_readAll")
		packer = WebPacker(baseDir)
		packer.readJS()
		jsText = packer.getJSText()
		len(jsText)
		openTags = [m.start() for m in re.finditer("<script>", jsText)]
		closeTags = [m.start() for m in re.finditer("</script>", jsText)]
		print("js open  tags: %d" % len(openTags))
		print("js close tags: %d" % len(closeTags))


	def test_showdownjs(self):
		print("--- running TestWebPacker.test_showdownjs")
		packer = WebPacker()
		jsText = packer.getShowdownjs()
		assert(len(jsText) > 180000)
		assert("<script>" in jsText)
		assert("/script>" in jsText)

	def test_annotationjs(self):
		print("--- running TestWebPacker.test_annotationjs")
		packer = WebPacker()
		jsText = packer.getAnnotationjs()
		assert(len(jsText) > 3000)
		assert("<script>" in jsText)
		assert("/script>" in jsText)




