
'''
******************************************************************
SLEXIL—Software Linking Elan XML to Illuminated Language
Copyright (C) 2019 Paul Shannon and David Beck

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

The full version of the GNU General Public License is found at
<https://www.gnu.org/licenses/>.

Information about the software can be obtained by contacting
david.beck at ualberta.ca.
******************************************************************
'''

# -*- coding: utf-8 -*-
#
# MorphemeGloss.py: a class to capture, and render into HTML, the morphemes of the spoken text, using
# standard grammatical terms
#
# see https://en.wikipedia.org/wiki/List_of_glossing_abbreviations
# from https://en.wikipedia.org/wiki/Interlinear_gloss#Structure
#
#  grammatical terms are commonly abbreviated and printed in SMALL CAPITALS to keep them distinct
#  from translations,  especially when they are frequent or important for analysis.
#
#  for IJAL style requirements of interlinear glosses, see http://www.americanlinguistics.org/?page_id=93
#  also see the Leipzig Glossing Rules: https://www.eva.mpg.de/lingua/resources/glossing-rules.php
#
# in interlinear morphological glosses, punctuation separating the glosses:
#
#        .  equivalent to a space (separating words) in the morpheme line
#        _  when a source language word corresponds to a phrase in the glossing language
#        =  separates clitics (a morpheme with syntactic characteristics of a word, but which
#           depends phonologically upon another word or phrase)
#        ~  reduplication
#        -- and more...
#
# david beck (email 12 aug 2018):
#
#    I usually leave the numbers in the abbreviations in normal font size, as well as punctuation
#    marks like the colon and the period (which are reserved characters for interlinear glossing). The
#    morpheme delimiters are also in regular sized type, and in the original GUI there was a field
#    where the user could list the symbols in use. – (n-dash), =, and • are the most common, but there
#    are others people are likely to use such as ~ (for reduplication), ^ (to add a floating tone to a
#    morph), and < > (for infixes). Another thing that we haven’t come up against yet is that there are
#    sometimes subscripts, most commonly used to label something as belonging to a particular class.
#------------------------------------------------------------------------------------------------------------------------
import re
from pprint import pprint
from yattag import *
import pdb
from grammaticalTerms import *

#------------------------------------------------------------------------------------------------------------------------
class MorphemeGloss:

   rawText = ""
   grammaticalTerms = []
   delimiters = "(<sub>|</sub>|<sup>|</sup>|[=•\-\.–~\^+<>:])"

   def __init__(self, rawText, grammaticalTerms):
      self.rawText = rawText
      self.grammaticalTerms = grammaticalTerms

   def show(self):
      pprint(vars(self))

   def parse(self):
      """ identify terms, delimiters, plain words """
      self.parts = _extractParts(self.delimiters, self.rawText)
      self.addNumberedAbbreviations() #extends self.grammaticalTerms to include 1sg, 2sg, etc.
      self.gtObjectList = []
      for part in self.parts:
         gt = GrammaticalTerms(part,self.grammaticalTerms)
         self.gtObjectList.append(gt)

   def addNumberedAbbreviations(self):
      ''' adds number + abbreviation combinations used
         in the text (e.g., 1sg, 3obj) to grammaticalTerms list
         and ensures these are in the correct case
      ''' 
      newTerms = [part for part in self.parts if any(i.isdigit() for i in part)]
      for term in newTerms:
         if term[0].isdigit() and term[1:].lower() in self.grammaticalTerms:
             self.grammaticalTerms.append(term.lower())
         elif term[-1].isdigit() and term[:-1].lower() in self.grammaticalTerms:
             self.grammaticalTerms.append(term.lower())
         elif not term in self.grammaticalTerms:
             self.grammaticalTerms.append(term)           

   def getParts(self):
      parts = []
      for gt in self.gtObjectList:
         part = gt.getTerm()
         parts.append(part)
      return(parts)

   def getTermsList(self):
      return(self.grammaticalTerms)

   def toHTML(self, htmlDoc):
      """ iterate over the parts list, identify each grammaticalTerm
          wrap each of those in a <span class='grammaticalTerm'> tag
      """
      with htmlDoc.tag("div", klass="morpheme-gloss"):
         for term in self.gtObjectList:
            part = term.getTerm()
            if(self.grammaticalTerms) and (part in self.grammaticalTerms):
               with htmlDoc.tag("span", klass="grammatical-term"):
                  htmlDoc.asis(part)
            else:
               htmlDoc.asis(part)


#------------------------------------------------------------------------------------------------------------------------
# non-class functions
#------------------------------------------------------------------------------------------------------------------------
def _extractParts(delimiters, string):
   parts = re.split(delimiters, string)
   parts_noEmptyStrings = [part for part in parts if part != ""]
   return(parts_noEmptyStrings)
