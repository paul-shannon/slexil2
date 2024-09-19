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

import pandas as pd
pd.set_option('display.max_columns', None)
from xml.etree import ElementTree as etree
from morphemeGloss import *
from pprint import pprint
from yattag import *
import pdb
import formatting
from translationLine import *

# ------------------------------------------------------------------------------------------------------------------------
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------------------------------------------------
class IjalLineFromDict:
    tbl = None
    tierInfo = []
    spokenTextID = ""
    rootElement = None
    rootID = None
    tierElements = []
    doc = None
    lineNumber = None
    quiet = True
    grammaticalTerms = None
    morphemes =  None
    morphemeGlosses = None
    morphemeSpacing = None
    useTooltips = False   

    def __init__(self, lineDict, lineNumber, tierGuide, grammaticalTerms=[],
                 useTooltips=False,verbose=True):
        self.x = lineDict
        self.lineNumber = lineNumber
        self.tierGuide = tierGuide
        self.grammaticalTerms = grammaticalTerms
        self.useTooltips = useTooltips
        self.verbose = verbose
        

    def getTierCount(self):
        canonicalTiers = set(["speech", "translation", "morphemes", "morphemeGlosses"])
        return len(canonicalTiers & set(list(self.x.keys())))


    '''the next three methods handle a use case where there is a missing or 
    empty transcription (line) tier but assume that there is a valid time-
    aligned translation tier (not sure we can save a file that has neither)'''

    def getStartTime(self):
       return(self.x["startTime"])

    def getEndTime(self):
       return(self.x["endTime"])

    def getAnnotationID(self):
       return(self.x["lineNumber"])

    def getSpokenText(self):

       return self.x["speech"]

    # ----------------------------------------------------------------------------------------------------
    def getTranslation(self):

        if "translation" in self.x.keys():
           return self.x["translation"]
        return(None)

    # ----------------------------------------------------------------------------------------------------
        # may be separated by spaces or tabs, tabs preferred 
    def getMorphemes(self):

        tierName = "morphemes"
        if tierName in self.x.keys():
            return self.x[tierName]
        return None

    # ----------------------------------------------------------------------------------------------------
    def getMorphemeGlosses(self):

        tierName = "morphemeGlosses"
        if tierName in self.x.keys():
            return self.x[tierName]
        return None

    # ----------------------------------------------------------------------------------------------------
    def getGrammaticalTerms(self):

        return(self.grammaticalTerms)

    # ----------------------------------------------------------------------------------------------------
    def calculateMorphemeSpacing(self):

        """
         the spacing is used to create a morphemeSpacingStyleString, specifying grid cell widths which
         accomodate the widest of each morpheme/gloss pair, so that they each member of
         each pair is vertically aligned:
             m1        m2        ----m3-----
             g1     ---g2---         g3
        """
        morphemes = self.getMorphemes()
        glosses = self.getMorphemeGlosses()
        if(morphemes == None):
           self.morphemeSpacing == None
           return
        self.morphemeSpacing = []
        if(glosses):
           if (len(morphemes) > len(glosses)):
               theDifference = len(morphemes) - len(glosses)
               for i in range(0, theDifference):
                   glosses.append("⚠️")
           elif (len(morphemes) < len(glosses)):
               theDifference = len(glosses) - len(morphemes)
               for i in range(0, theDifference):
                   morphemes.append("⚠️")


        for i in range(len(morphemes)):
            if "<su" in morphemes[i]:
                newmorph = morphemes[i].replace("<sub>", "")
                newmorph = newmorph.replace("</sub>", "")
                newmorph = newmorph.replace("<sup>", "")
                newmorph = newmorph.replace("</sup>", "")
                morphemeSize = len(newmorph)
            else:
                morphemeSize = len(morphemes[i])
            glossSize = 0
            if(glosses):
               if "<su" in glosses[i]:
                  newGloss = glosses[i].replace("<sub>", "")
                  newGloss = newGloss.replace("</sub>", "")
                  newGloss = newGloss.replace("<sup>", "")
                  newGloss = newGloss.replace("</sup>", "")
                  glossSize = len(newGloss)
               else:
                  glossSize = len(glosses[i])
            self.morphemeSpacing.append(max(morphemeSize, glossSize) + 3)

    # ----------------------------------------------------------------------------------------------------
    def getMorphemeSpacing(self):

        return (self.morphemeSpacing)

    # ----------------------------------------------------------------------------------------------------
    def htmlLeadIn(self, htmlDoc): # , audioDirectory, audioFileType):

        buttonLabelNumber = self.lineNumber + 1
        #print("buttonLabelNumber: %d" % buttonLabelNumber)
        clickActionString = "playSample(%d, %d, %d)" % \
                            (self.lineNumber+1, self.getStartTime(), self.getEndTime())
        buttonTag = htmlDoc.tag("button", onclick=clickActionString,
                                klass="standardSlexilButton slexilTooltip")
        if(self.useTooltips):
            buttonTag.attrs["class"] = "standardSlexilButton slexilTooltip"
        with buttonTag:
           htmlDoc.text(buttonLabelNumber)
           if(self.useTooltips):
              with htmlDoc.tag("span", klass="slexilTooltipText"):
                  htmlDoc.text("Play Line %d" % buttonLabelNumber)

    # ----------------------------------------------------------------------------------------------------
    def toHTML(self, htmlDoc):

        with htmlDoc.tag("div", klass="line-content", id=self.lineNumber+1):
            with htmlDoc.tag("div", klass="line"):
                with htmlDoc.tag("span", klass="speech-tier"):
                    htmlDoc.asis(self.getSpokenText())

            morphemes = self.getMorphemes()
            morphemeSpacingStyleString = ""
            if (morphemes):
               if(len(morphemes) > 0):
                  morphemeSpacingStyleString = "grid-template-columns: %s;" % ''.join(["%dch " % p for p in self.morphemeSpacing])
                  with htmlDoc.tag("div", klass="morpheme-tier", style=morphemeSpacingStyleString):
                     for morpheme in morphemes:
                        with htmlDoc.tag("div", klass="morpheme-cell"):
                            htmlDoc.asis(morpheme)

            morphemeGlosses = self.getMorphemeGlosses()
            if (morphemes and morphemeGlosses):
               if(len(morphemeGlosses) > 0):
                  with htmlDoc.tag("div", klass="morpheme-tier", style=morphemeSpacingStyleString):
                     for morphemeGloss in self.getMorphemeGlosses():
                         with htmlDoc.tag("div", klass="morpheme-cell"):
                            mg = MorphemeGloss(morphemeGloss, self.grammaticalTerms)
                            mg.parse()
                            mg.toHTML(htmlDoc)

            translation = self.getTranslation()
            if translation:
               with htmlDoc.tag("div", klass="freeTranslation-tier"):
                   htmlDoc.asis(translation)

# ------------------------------------------------------------------------------------------------------------------------
def replaceHyphensWithNDashes(list):
    ''' replace hyphens with n-dashes
        '''
    newList = []
    if(isinstance(list, str)):  # account for single string 
        list = [list]
    for text in list:
        text = text.replace('-', '–')
        newList.append(text)
    return (newList)
