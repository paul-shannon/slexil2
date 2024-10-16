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
from slexil.standardizeIjalTierTable import StandardizeIjalTierTable

# ------------------------------------------------------------------------------------------------------------------------
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------------------------------------------------
class IjalLine:
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

    def __init__(self, lineTable, lineNumber, tierGuide, grammaticalTerms=[],
                 useTooltips=False,verbose=True):
        # self.tbl = standardizeTable(lineTable, tierGuide, verbose)
        std = StandardizeIjalTierTable(lineTable, tierGuide, verbose)
        std.guideAndLinesAgree()
        std.addCanonicalTierNameColumn()
        self.tbl = std.getTable()
        # print("ijalLine ctor, self.tbl has been standardized")
        # print(lineTable)
        # print(self.tbl)
        self.lineNumber = lineNumber
        self.tierGuide = tierGuide
        self.grammaticalTerms = grammaticalTerms
        self.useTooltips = useTooltips
        self.verbose = verbose
        #if(self.verbose):
        #   print(self.tbl)


    def getTierCount(self):
        return (self.getTable().shape[0])

    def getTable(self):
        return (self.tbl)

    '''the next three methods handle a use case where there is a missing or 
    empty transcription (line) tier but assume that there is a valid time-
    aligned translation tier (not sure we can save a file that has neither)'''

    def getStartTime(self):
        return(self.tbl.iloc[0]["startTime"])

    def getEndTime(self):
        return(self.tbl.iloc[0]["endTime"])

    def getAnnotationID(self):
        return(self.tbl.iloc[0]["id"])
        if self.speechRow != None:
            return (self.tbl.iloc[self.speechRow][self.tbl.columns.values.tolist().index("ANNOTATION_ID")])
        else:
            return (self.tbl.iloc[self.translationRow][self.tbl.columns.values.tolist().index("ANNOTATION_ID")])

    # ----------------------------------------------------------------------------------------------------
    def show(self):

        pprint(vars(self))

    # ----------------------------------------------------------------------------------------------------
    def getSpokenText(self):

        canonicalTierName = "speech"
        row = self.tbl["canonicalTier"].tolist().index(canonicalTierName)
        spokenText = self.tbl.iloc[row]["text"]
        if(spokenText == None):
           spokenText = ""
        return(spokenText)

    # ----------------------------------------------------------------------------------------------------
    def getTranslation(self):

        canonicalTierName = "translation"
        if(not canonicalTierName in self.tbl["canonicalTier"].tolist()):
           return(None)
        rowNumbers = self.tbl.index
        whichRowNumber = self.tbl["canonicalTier"].tolist().index(canonicalTierName)
        rowNumber = rowNumbers[whichRowNumber]
        rawTranslation = self.tbl.iloc[rowNumber]["text"]
        if(rawTranslation == None):
           return("")
        if(len(rawTranslation) == 0):
           return("")
        translationLine = TranslationLine(rawTranslation)
        return (translationLine.getStandardized())

    # ----------------------------------------------------------------------------------------------------
    def getTranslation2(self):

        canonicalTierName = "translation2"
        if(not canonicalTierName in self.tbl["canonicalTier"].tolist()):
           return(None)
        row = self.tbl["canonicalTier"].tolist().index(canonicalTierName)
        rawTranslation = self.tbl.iloc[row]["text"]
        translationLine = TranslationLine(rawTranslation)
        return (translationLine.getStandardized())

    # ----------------------------------------------------------------------------------------------------
    def getSoundsLike(self):

        canonicalTierName = "soundsLike"
        if(not canonicalTierName in self.tbl["canonicalTier"].tolist()):
           return(None)
        rowNumbers = self.tbl.index
        whichRowNumber = self.tbl["canonicalTier"].tolist().index(canonicalTierName)
        rowNumber = rowNumbers[whichRowNumber]
        rawText = self.tbl.iloc[rowNumber]["text"]
        if(rawText == None):
           return("")
        if(len(rawText) == 0):
           return("")
        return ("<i>%s</i>" % rawText)
    
    # ----------------------------------------------------------------------------------------------------
        # may be separated by spaces or tabs, tabs preferred 
    def extractMorphemes(self):

        canonicalTierName = "morpheme"
        if(not canonicalTierName in self.tbl["canonicalTier"].tolist()):
           #if(self.verbose):
           #   print("=== found no tier named '%s'" % canonicalTierName)
           return(None)
        morphemeRow = self.tbl["canonicalTier"].tolist().index(canonicalTierName)

        #pdb.set_trace()
        #rawMorphemeText = self.tbl.iloc[morphemeRow, "text"]
        rawMorphemeText = self.tbl.iloc[morphemeRow]["text"]
        self.morphemes = []
        if(rawMorphemeText):
           if "\t" in rawMorphemeText:
               rawMorphemeList = rawMorphemeText.split('\t')
           elif " " in rawMorphemeText:
               rawMorphemeList = rawMorphemeText.split(' ')
           else:  # neither tab nor space separators
               rawMorphemeList = rawMorphemeText
           self.morphemes = replaceHyphensWithNDashes(rawMorphemeList)
        return (self.morphemes)

    # ----------------------------------------------------------------------------------------------------
    def extractMorphemeGlosses(self):

        canonicalTierName = "morphemeGloss"
        if(not canonicalTierName in self.tbl["canonicalTier"].tolist()):
           #if(self.verbose):
           #   print("=== found no tier named '%s'" % canonicalTierName)
           return(None)
        morphemeGlossRow = self.tbl["canonicalTier"].tolist().index(canonicalTierName)

        rawMorphemeGlossText = self.tbl.iloc[morphemeGlossRow]["text"]
        self.morphemeGlosses = []
        if(rawMorphemeGlossText):
           if "\t" in rawMorphemeGlossText:
               rawMorphemeGlossList = rawMorphemeGlossText.split('\t')
           elif (" " in rawMorphemeGlossText):
               rawMorphemeGlossList = rawMorphemeGlossText.split(' ')
           else:  # neither space nor tab separators found
               rawMorphemeGlossList = rawMorphemeGlossText
           self.morphemeGlosses = replaceHyphensWithNDashes(rawMorphemeGlossList)
        return (self.morphemeGlosses)

    # ----------------------------------------------------------------------------------------------------
    def getMorphemes(self):

        return (self.morphemes)

    # ----------------------------------------------------------------------------------------------------
    def getGrammaticalTerms(self):

        return(self.grammaticalTerms)

    # ----------------------------------------------------------------------------------------------------
    def getMorphemeGlosses(self):

        return (self.morphemeGlosses)

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
               #logging.warning("EAF error - There are more morphs (%d) than glosses (%d) in line %s." % (len(morphemes), len(glosses), int(self.lineNumber) + 1))
               theDifference = len(morphemes) - len(glosses)
               for i in range(0, theDifference):
                   glosses.append("⚠️")
           elif (len(morphemes) < len(glosses)):
               #logging.warning("EAF error - There are more glosses (%d) than morphs (%d) in line %s." % (len(glosses), len(morphemes), int(self.lineNumber) + 1))
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

            soundsLike = self.getSoundsLike()
            if soundsLike:
               with htmlDoc.tag("div", klass="freeTranslation-tier"):
                   htmlDoc.asis(soundsLike)

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

            translation2 = self.getTranslation2()
            if translation2 != None:
               with htmlDoc.tag("div", klass="freeTranslation-tier"):
                   htmlDoc.text(translation2)
               # add a div to hold annotations
            with htmlDoc.tag("div", klass="annotationDiv"):
                pass#;


# ------------------------------------------------------------------------------------------------------------------------
def findChildren(doc, rootElement):
    elementsToDo = [rootElement]
    elementsCompleted = []

    while (len(elementsToDo) > 0):
        currentElement = elementsToDo[0]
        parentRef = currentElement.attrib["ANNOTATION_ID"]
        pattern = "TIER/ANNOTATION/REF_ANNOTATION[@ANNOTATION_REF='%s']" % parentRef
        childElements = doc.findall(pattern)
        elementsToDo.remove(currentElement)
        elementsCompleted.append(currentElement)
        if (len(childElements) > 0):
            elementsToDo.extend(childElements)

    return (elementsCompleted)


# ------------------------------------------------------------------------------------------------------------------------
# every line in the text is transformed from ELAN xml to a pandas table.
# each row in the table corresponds to a tier in the xml.  Here we
# aassociate canonical IJAL tiers (e.g., speech, morpheme, morphemeGloss, translation)
# with each of the tiers in the xml, using the user-supplied tierGuide.
# for example: 	tierGuide = {'speech': 'italianSpeech',
#                            'transcription2': None,
#                            'morpheme': 'morphemes',
#                            'morphemeGloss': 'morpheme-gloss',
#                            'translation': 'english',
#                            'translation2': None}
# futhermore, since a speech tier is a mandatory minimum, we chack for that,
# return None if insufficient information is provided.
def obsolete_standardizeTable(tbl, tierGuide, verbose):

    tierNames = tbl["tierID"].tolist()
    userValues = list(tierGuide.values())
    recognizedUserValues = list(set(userValues).intersection(set(tierNames)))
    if(len(recognizedUserValues) == 0):
       msg = "error in IjalLine standardizeTable: tier names not in tierGuide"
       raise Exception(msg)
    
    allCanonicalNames = ('speech', 'morpheme', 'morphemeGloss', 'translation', 'translation2')
    userCanonicalNames = list(tierGuide.keys())
    #pdb.set_trace()
    
    userIllegals = list(set(userCanonicalNames).difference(set(allCanonicalNames)))
    if(len(userIllegals) > 0):
       print("tierGuide uses unknown canonical IJAL categories: %s" % userIllegals)
    
    recognized = [tierName for tierName in allCanonicalNames if tierName in userCanonicalNames]
    if(len(recognized) == 0):
       print("error no valid canonical tier names in your tierGuide")
       print(tierGuide)
       return(None)

       # extract the user's tier names for the recognized canonical tier names
    keepers = [tierGuide[key] for key in recognized]
    tbl_trimmed = [tbl[tbl["tierID"].isin(keepers)]][0]

    # subset the tbl to only include rows with a canonical tier name 
    if(verbose):
       print("shared, recongized tierNames, keys: %s" % recognized)

    canonicalTier = []
    userTierNames = list(tbl_trimmed["tierID"])
    # reverse the guide so we can map from user-supplied and often idiosyncratic
    # TIER_ID values, to the IJAL standard types: speech, translation, morpheme, 
    # morphemeGloss

    revGuide = {v: k for k, v in tierGuide.items()}
    if(verbose):
        print("revGuide: %s" % revGuide)
        print("userTierNames: %s" % userTierNames)
    canonicalTierNames = [revGuide[key] for key in userTierNames]
    if(not "speech" in canonicalTierNames):
       print("no tier designated as the spoken line ('speech' tier)")
       return(None)

      # add a new column to the table.  we will use this later to assemble the html
    tbl_final = tbl_trimmed.assign(canonicalTier=canonicalTierNames)

    return (tbl_final)

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
