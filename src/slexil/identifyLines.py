import yaml
from xml.etree import ElementTree as etree

'''this module eliminates errors with files that have more than one type of alignable annotation
and overgenerate lines and audiophrases for non-lines. We need to ensure that only needed lines are 
processed and that the lines sent to IjalLine conform to the Tierguide'''

def getList(doc,tierGuide):
    speechTier = tierGuide['speech']
    '''we need to cull the list of alignable annotations to include only the ones we want under various 
    use case scenarios'''
    speechTierList = doc.findall("TIER[@TIER_ID='%s']/ANNOTATION/ALIGNABLE_ANNOTATION" % speechTier)
    '''CASE I: speech-tier is only alignable tier ==> use speechTierList'''
    '''CASE II: speech-tier is alignable, but not the only alignable ==> use speechTierList'''
    if len(speechTierList) == 0:
        '''CASE III: speech-tier is not alignable, daughter of only alignable tier'''
        '''CASE IV: speech-tier is not alignable, there is another alignable tier'''
        speechTierList = doc.findall("TIER[@TIER_ID='%s']/ANNOTATION/REF_ANNOTATION" % speechTier)
        # alignableTierList = doc.findall("TIER/ANNOTATION/ALIGNABLE_ANNOTATION")
        speechTierList = findAlignableParents(doc,speechTierList)

    return speechTierList

def findAlignableParents(doc,speechTierList):
    parentTierList = []
    for item in speechTierList:
        alignableParent = None
        parentID = item.attrib["ANNOTATION_REF"]
        while not alignableParent:
            alignableParent = doc.find('TIER/ANNOTATION/ALIGNABLE_ANNOTATION[@ANNOTATION_ID="%s"]' %parentID)
            if not alignableParent:
                parent = doc.find('TIER/ANNOTATION/REF_ANNOTATION[@ANNOTATION_ID="%s"]' %parentID)
                # print(etree.tostring(parent,encoding="unicode"))
                parentID = parent.attrib["ANNOTATION_REF"]
        parentTierList.append(alignableParent)
    return parentTierList