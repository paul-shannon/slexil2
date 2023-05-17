import unittest
from slexil.htmlInserter import HtmlInserter
import pdb

class TestHtmlInserter(unittest.TestCase):

	def test_css(self):
		print("--- running TestHtmlInserter.test_css")
		inserter = HtmlInserter()
		cssText = inserter.getCSS()
		assert(len(cssText) > 3500)
		assert("<style>" in cssText)
		assert("/style>" in cssText)

	def test_slexiljs(self):
		print("--- running TestHtmlInserter.test_slexiljs")
		inserter = HtmlInserter()
		jsText = inserter.getSlexiljs()
		assert(len(jsText) > 3000)
		assert("<script>" in jsText)
		assert("/script>" in jsText)

	def test_showdownjs(self):
		print("--- running TestHtmlInserter.test_showdownjs")
		inserter = HtmlInserter()
		jsText = inserter.getShowdownjs()
		assert(len(jsText) > 180000)
		assert("<script>" in jsText)
		assert("/script>" in jsText)

	def test_annotationjs(self):
		print("--- running TestHtmlInserter.test_annotationjs")
		inserter = HtmlInserter()
		jsText = inserter.getAnnotationjs()
		assert(len(jsText) > 3000)
		assert("<script>" in jsText)
		assert("/script>" in jsText)




