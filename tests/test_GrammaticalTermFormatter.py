# test_newMorphemeGloss.py
#--------------------------------------------------------------------------------
from slexil.grammaticalTermFormatter import GrammaticalTermFormatter
import pdb
import yattag
import os
#--------------------------------------------------------------------------------
# from the first line of inferno:

glosses = ["in=DEF:MASC:SG","middle-MASC:SG","of=DEF:MASC:SG",
           "journey–MASC:SG","of", "our-FEM:SG","life-FEM"]
terms = ["IMPF","REM","PAST","INDEF","DEF","FEM","MASC","SG","DAT","PARTIC"]
#--------------------------------------------------------------------------------
def test_DEF():

   print("--- test_DEF")
   
   mgs = ["in=DEF:MASC:SG","middle-MASC:SG","of=DEF:MASC:SG",
         "journey–MASC:SG","of", "our-FEM:SG","life-FEM"]
   terms = ["IMPF","REM","PAST","INDEF","DEF","FEM","MASC","SG","DAT","PARTIC"]

   mg = GrammaticalTermFormatter("in=DEF", terms)
   mg.parse()
   s = mg.parse()

   expected = "in=<span klass='glossTerm'>DEF</span>"
   assert(s == expected)

#--------------------------------------------------------------------------------
def test_DEF_MASC():

   print("--- test_DEF_MASC")

   mg = GrammaticalTermFormatter("in=DEF:MASC", terms)
   mg.parse()
   s = mg.format()

   expected = "in=<span klass='glossTerm'>DEF</span>:<span klass='glossTerm'>MASC</span>"
   assert(s == expected)

#--------------------------------------------------------------------------------
def test_fromNatalia():

   print("--- test_fromNatalia")

   terms = ["INCL", "POSS1", "NMLZ", "COP", "S3SG", "PST"]
   mg = GrammaticalTermFormatter("INCL–POSS1–say–NMLZ=COP–S3SG–PST", terms)
   mg.parse()
   s = mg.format()

      # note presence of visually indistincuishable
      # HYPHEN-MINUS and EN DASH.  both are now included in
      # the default delimiters
   expected = "%s%s%s%s%s%s" % ("<span klass='glossTerm'>INCL</span>–",
                                "<span klass='glossTerm'>POSS1</span>–",
                                "say–<span klass='glossTerm'>NMLZ</span>=",
                                "<span klass='glossTerm'>COP</span>–",
                                "<span klass='glossTerm'>S3SG</span>–",
                                "<span klass='glossTerm'>PST</span>")
   assert(s == expected)

#--------------------------------------------------------------------------------
def runTests():

   test_DEF()
   test_DEF_MASC()
   test_fromNatalia()
   
#--------------------------------------------------------------------------------
if __name__ == '__main__':
    runTests()

# packageRoot = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# dataDir = os.path.join(packageRoot, "data")
# grammaticalTermsFile = os.path.join(dataDir, "infernoDemo", "grammaticalTerms.txt")
# tierGuideFile = os.path.join(dataDir, "infernoDemo", "tierGuide.yaml")
# 
# assert(os.path.exists(grammaticalTermsFile))
# termsRaw = open(grammaticalTermsFile).readlines()
# grammaticalTerms = [term.strip() for term in termsRaw]
# assert(os.path.exists(tierGuideFile))
# 
# class TestMorphemeGloss(unittest.TestCase):
# 
#         def test_morphemGloss(self):
#                 print("--- test_morphemeGloss")
#                 mg = MorphemeGloss(rawText, grammaticalTerms)
#                 mg.parse()
#                 parts = mg.getParts()
#                 pdb.set_trace()
#                 self.assertEqual(len(parts), 27)
# 
#         def test_getTermsList(self):
#                 print("--- test_getTermsList")
#                 mg = MorphemeGloss(rawText, grammaticalTerms)
#                 mg.parse()
#                 terms = mg.getTermsList()
#                 self.assertEqual(terms, grammaticalTerms)
# 
#         def test_HTML(self):
#                 print("--- test_getHTML")
#                 mg = MorphemeGloss(rawText, grammaticalTerms)
#                 mg.parse()
#                 htmlDoc = yattag.Doc()
#                 mg.format(htmlDoc)
#                 html = htmlDoc.getvalue()
#                 self.assertEqual(html.count("grammatical-term"), 8)
# 
# if __name__ == '__main__':
#                 unittest.main()
#                 
