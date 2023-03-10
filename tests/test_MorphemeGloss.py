# -*- coding: utf-8 -*-

import sys,os
sys.path.append("../slexil")
from morphemeGloss import *


#------------------------------------------------------------------------------------------------------------------------
sampleLines = ["hab=3A=mouth•cry",
               "1S=walk–INC",
               "HAB=3A=work=IAM",
               "PROG=1A=know–INTR",
               "more",
               "1pro",
               ]


#----------------------------------------------------------------------------------------------------
grammaticalTermsFiles = ["../testData/inferno/grammaticalTerms.txt"]
grammaticalTerms = []
for file in grammaticalTermsFiles:
   newTerms = open(file).read().split("\n")
   grammaticalTerms += newTerms[:-1]


#----------------------------------------------------------------------------------------------------
def runTests():

    test_constructor()
    test_parse()
    test_inferno()
    test_toHTML_sampleLine_0()
    test_toHTML_sampleLine_1()
    test_toHTML_sampleLine_2()
    test_toHTML_sampleLine_3()
    test_toHTML_sampleLine_4()
    test_toHTML_sampleLine_5()
    test_nDashes()
    test_Sub_and_Sup()
    test_Additional_Delimiters()
    test_toHTML_sampleLine_6()
    test_praying_morpheme_glosses

def test_constructor():
   
    print("--- test_constructor")
    #grammaticalTerms = open(grammaticalTermsFile).read().split("\n")
    mg = MorphemeGloss(sampleLines[0], grammaticalTerms)

def test_parse():

    #grammaticalTerms = open(grammaticalTermsFile).read().split("\n")
    print("--- test_parse")
    mg = MorphemeGloss(sampleLines[0], grammaticalTerms)
    mg.parse()
    assert(mg.getParts() == ['hab', '=', '3A', '=', 'mouth', '•', 'cry'])

def test_toHTML_sampleLine_0(displayPage=False):
    """
      create an empty htmlDoc, then render the MorhphemeGloss into it
    """
    print("--- test_toHTML_sampleLine_0")

    #grammaticalTerms = open(grammaticalTermsFile).read().split("\n")
    grammaticalTerms = ['3A','hab','mouth']
    mg = MorphemeGloss(sampleLines[0], grammaticalTerms)
    mg.parse()
    try:
    	assert(mg.getParts() == ['hab', '=', '3A', '=', 'mouth', '•', 'cry'])
    except AssertionError as e:
    	raise Exception(mg.getParts()) from e

    htmlDoc = Doc()

    htmlDoc.asis('<!DOCTYPE html>')
    with htmlDoc.tag('html', lang="en"):
        with htmlDoc.tag('head'):
            htmlDoc.asis('<link rel="stylesheet" href="ijal.css">')
            with htmlDoc.tag('body'):
                mg.toHTML(htmlDoc)

    htmlText = htmlDoc.getvalue()
    assert(htmlText.count('<span class="grammatical-term">') == 3)  # HAB, A, MOUTH

    if(displayPage):
        f = open("morphemeGloss.html", "w")
        f.write(indent(htmlText))
        f.close()
        os.system("open %s" % "morphemeGloss.html")

def test_toHTML_sampleLine_1(displayPage=False):
    """
      create an empty htmlDoc, then render the MorhphemeGloss into it
    """
    print("--- test_toHTML_sampleLine_1")

    #grammaticalTerms = open(grammaticalTermsFile).read().split("\n")
    grammaticalTerms = ['1S','inc']
    mg = MorphemeGloss(sampleLines[1], grammaticalTerms)
    mg.parse()
    assert(mg.getParts() == ['1S', '=', 'walk', '–', 'inc'])

    htmlDoc = Doc()

    htmlDoc.asis('<!DOCTYPE html>')
    with htmlDoc.tag('html', lang="en"):
        with htmlDoc.tag('head'):
            htmlDoc.asis('<link rel="stylesheet" href="ijal.css">')
            with htmlDoc.tag('body'):
                mg.toHTML(htmlDoc)

    htmlText = htmlDoc.getvalue()
    assert(htmlText.count('<span class="grammatical-term">') == 2)  # S  INC

    if(displayPage):
        f = open("morphemeGloss.html", "w")
        f.write(indent(htmlText))
        f.close()
        os.system("open %s" % "morphemeGloss.html")

def test_toHTML_sampleLine_2(displayPage=False):
    """
      create an empty htmlDoc, then render the MorhphemeGloss into it
    """
    print("--- test_toHTML_sampleLine_2")

    #grammaticalTerms = open(grammaticalTermsFile).read().split("\n")
    grammaticalTerms = ['hab','3A','iam']
    mg = MorphemeGloss(sampleLines[2], grammaticalTerms)
    mg.parse()
    mg.getParts()
    assert(mg.getParts() == ['hab', '=', '3A', '=', 'work', '=', 'iam'])

    htmlDoc = Doc()

    htmlDoc.asis('<!DOCTYPE html>')
    with htmlDoc.tag('html', lang="en"):
        with htmlDoc.tag('head'):
            htmlDoc.asis('<link rel="stylesheet" href="ijal.css">')
            with htmlDoc.tag('body'):
                mg.toHTML(htmlDoc)

    htmlText = htmlDoc.getvalue()
    assert(htmlText.count('<span class="grammatical-term">') == 3)  # HAB A IAM

    if(displayPage):
        f = open("morphemeGloss.html", "w")
        f.write(indent(htmlText))
        f.close()
        os.system("open %s" % "morphemeGloss.html")

def test_toHTML_sampleLine_3(displayPage=False):
    """
      create an empty htmlDoc, then render the MorhphemeGloss into it
    """
    print("--- test_toHTML_sampleLine_3")

    #grammaticalTerms = open(grammaticalTermsFile).read().split("\n")
    grammaticalTerms = ['prog','1A','intr']
    mg = MorphemeGloss(sampleLines[3], grammaticalTerms)
    mg.parse()
    mg.getParts()
    assert(mg.getParts() == ['prog', '=', '1A', '=', 'know', '–', 'intr'])

    htmlDoc = Doc()

    htmlDoc.asis('<!DOCTYPE html>')
    with htmlDoc.tag('html', lang="en"):
        with htmlDoc.tag('head'):
            htmlDoc.asis('<link rel="stylesheet" href="ijal.css">')
            with htmlDoc.tag('body'):
                mg.toHTML(htmlDoc)

    htmlText = htmlDoc.getvalue()
    assert(htmlText.count('<span class="grammatical-term">') == 3)  # PROG A INTR

    if(displayPage):
        f = open("morphemeGloss.html", "w")
        f.write(indent(htmlText))
        f.close()
        os.system("open %s" % "morphemeGloss.html")

def test_toHTML_sampleLine_4(displayPage=False):
    """
      create an empty htmlDoc, then render the MorhphemeGloss into it
    """
    print("--- test_toHTML_sampleLine_4")

    #grammaticalTerms = open(grammaticalTermsFile).read().split("\n")
    mg = MorphemeGloss(sampleLines[4], grammaticalTerms)
    mg.parse()
    mg.getParts()
    assert(mg.getParts() == ['more'])

    htmlDoc = Doc()

    htmlDoc.asis('<!DOCTYPE html>')
    with htmlDoc.tag('html', lang="en"):
        with htmlDoc.tag('head'):
            htmlDoc.asis('<link rel="stylesheet" href="ijal.css">')
            with htmlDoc.tag('body'):
                mg.toHTML(htmlDoc)

    htmlText = htmlDoc.getvalue()
    assert(htmlText.count('<span class="grammatical-term">') == 0)  # none in this gloss

    if(displayPage):
        f = open("morphemeGloss.html", "w")
        f.write(indent(htmlText))
        f.close()
        os.system("open %s" % "morphemeGloss.html")


def test_toHTML_sampleLine_5(displayPage=False):
    """
      create an empty htmlDoc, then render the MorhphemeGloss into it
    """
    print("--- test_toHTML_sampleLine_5")

    #grammaticalTerms = open(grammaticalTermsFile).read().split("\n")
    mg = MorphemeGloss(sampleLines[5], grammaticalTerms)
    mg.parse()
    mg.getParts()
    assert(mg.getParts() == ['1pro'])

    htmlDoc = Doc()

    htmlDoc.asis('<!DOCTYPE html>')
    with htmlDoc.tag('html', lang="en"):
        with htmlDoc.tag('head'):
            htmlDoc.asis('<link rel="stylesheet" href="ijal.css">')
            with htmlDoc.tag('body'):
                mg.toHTML(htmlDoc)

    htmlText = htmlDoc.getvalue()
    assert(htmlText.count('<span class="grammatical-term">') == 1)  # PRO

    if(displayPage):
        f = open("morphemeGloss.html", "w")
        f.write(indent(htmlText))
        f.close()
        os.system("open %s" % "morphemeGloss.html")


def test_inferno(displayPage=False):
    """
      a bunch of new terms came with this text.  test them all out here
    """
    print("--- test_inferno")

    mg = MorphemeGloss("in=def–masc–sg", grammaticalTerms)
    mg.parse()
    assert(mg.getParts() == ['in', '=', 'def', '–', 'masc', '–', 'sg'])

    mg = MorphemeGloss("middle–masc", grammaticalTerms); mg.parse()
    assert(mg.getParts() == ['middle', '–', 'masc'])

    mg = MorphemeGloss("of=def–masc–sg", grammaticalTerms); mg.parse();
    assert(mg.getParts() == ['of', '=', 'def', '–', 'masc', '–', 'sg'])

    mg = MorphemeGloss("journey–masc", grammaticalTerms); mg.parse();
    assert(mg.getParts() == ['journey', '–', 'masc'])

    mg = MorphemeGloss("our–fem–sg", grammaticalTerms); mg.parse();
    assert(mg.getParts() == ['our', '–', 'fem', '–', 'sg'])

    mg = MorphemeGloss("life–fem", grammaticalTerms); mg.parse();
    assert(mg.getParts() == ['life', '–', 'fem'])

    mg = MorphemeGloss("be–3sg–impf", grammaticalTerms); mg.parse();
    assert(mg.getParts() == ['be', '–', '3sg', '–', 'impf'])

    mg = MorphemeGloss("found–1sg–indef–rem–past", grammaticalTerms); mg.parse();
    assert(mg.getParts() ==  ['found', '–', '1sg', '–', 'indef', '–', 'rem', '–', 'past'])

def test_nDashes(displayPage=False):
    """
      test for hyphens
    """
    print("--- test_nDashes")

    gt = MorphemeGloss("in=def–masc–3sg", grammaticalTerms)
    gt.parse()
    assert(gt.getParts() ==  ['in', '=', 'def', '–', 'masc', '–', '3sg'])

def test_Sub_and_Sup(displayPage=False):
    """
      test input with subscripts and superscripts
    """
    print("--- test_Sub_and_Sup")

    gt = MorphemeGloss("gu<sup>1</sup>hin<sub>masc</sub>–pl", ["masc","pl"])
    gt.parse()
    assert(gt.getParts() ==  ['gu', '<sup>', '1', '</sup>', 'hin', '<sub>', 'masc', '</sub>', '–', 'pl'])

def test_Additional_Delimiters(displayPage=False):
    """
      customizable test to make sure added delimiters don't cause problems
      Currently configured for: ^, +, < >
    """
    print("--- test_Additional_Delimiters")

    gt = MorphemeGloss("PL^Dog<masc>+pl", ["masc","pl"])
    gt.parse()
    assert(gt.getParts() ==  ['pl', '^', 'Dog', '<', 'masc','>', '+', 'pl'])

def test_toHTML_sampleLine_6(displayPage=False):
    """
      create an empty htmlDoc, then render the MorphemeGloss into it
    """
    print("--- test_toHTML_sampleLine_6")

    #grammaticalTerms = open(grammaticalTermsFile).read().split("\n")
    gt = MorphemeGloss("PL^black.dog<sub>masc</sub>+pl", ["masc","pl"])
    gt.parse()
    gt.getParts()
    assert(gt.getParts() ==  ['pl', '^', 'black', '.', 'dog', '<sub>', 'masc', '</sub>', '+', 'pl'])


    htmlDoc = Doc()

    htmlDoc.asis('<!DOCTYPE html>')
    with htmlDoc.tag('html', lang="en"):
        with htmlDoc.tag('head'):
            htmlDoc.asis('<link rel="stylesheet" href="ijal.css">')
            with htmlDoc.tag('body'):
                gt.toHTML(htmlDoc)

    htmlText = htmlDoc.getvalue()
    #print(htmlText.count('<span class="grammatical-term">'))
    assert(htmlText.count('<span class="grammatical-term">') == 3)

    if(displayPage):
        f = open("morphemeGloss.html", "w")
        f.write(indent(htmlText))
        f.close()
        os.system("open %s" % "morphemeGloss.html")

def test_praying_morpheme_glosses(displayPage=False):
    """
      make sure MorphemeGloss handles the portmanteaus types in this text properly
    """
    print("--- test_praying_morpheme_glosses")

    mg = MorphemeGloss("PROG:be:2SG", ['PROG','2sg'])
    mg.parse()
    assert(mg.getParts() == ['prog', ':', 'be', ':', '2sg'])

##    mg = MorphemeGloss("middle-MASC", grammaticalTerms); mg.parse()
##    assert(mg.getParts() == ['middle', '–', 'masc'])


if __name__ == '__main__':
    runTests()

