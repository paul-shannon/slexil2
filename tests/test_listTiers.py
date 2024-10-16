import os
import unittest
import slexil
from xml.etree import ElementTree as etree

packageRoot = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dataDir = os.path.join(packageRoot, "testData")
eafFile = os.path.join(dataDir, "inferno", "inferno-threeLines.eaf")
tierGuideFile = os.path.join(dataDir, "inferno", "tierGuide.yaml")

class TestListTiers(unittest.TestCase):

	def test_tierCount(self):
		print("--- running test_listTiers.py, test_tierCount")
		tree = etree.parse(eafFile)
		root = tree.getroot()
		root.tag
		root.attrib
		tierElements = root.findall("TIER")
		self.assertEqual(len(tierElements), 4)


if __name__ == '__main__':
		unittest.main()
