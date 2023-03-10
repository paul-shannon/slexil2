# learn the tier ID names used by the recording linguist to identify the four
# crucial tiers, put them into the text's tierGuide.yaml file
#
# speech:
# translation:
# morpheme:
# morpehemGloss:
# morphemePacking: tabs|tiers
#
import sys
sys.path.append("../slexil")
from xml.etree import ElementTree as etree
from ijalLine import IjalLine as Line
import yaml

filename = "../testData/inferno/inferno-threeLines.eaf"
tierGuideFile = "../testData/inferno/tierGuide.yaml"
with open(tierGuideFile, 'r') as f:
   tierGuide = yaml.safe_load(f)
xmlDoc = etree.parse(filename)
x = Line(xmlDoc, 0, tierGuide, grammaticalTerms=[])

print(x.tblRaw["TIER_ID"].tolist())
