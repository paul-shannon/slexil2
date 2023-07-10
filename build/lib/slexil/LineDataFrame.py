import pandas as pd
from xml.etree import ElementTree as etree
pd.set_option('display.max_columns', 500)

class DataFrame:

    def __init__(self, doc, allElements):
        '''doc = .eaf file; allElements = line element and its children'''
        self.doc = doc
        self.allElements = allElements
        self.tbl = self.buildTable(doc,self.allElements)

    def getTbl(self):
        return self.tbl

    # def getTimeSlotIDs(self, doc, tbl_elements):
    #     '''next step asks for row 0 of dataframe (speech), get value of TSRef1 (start time)'''
    #     startTimeSlotID = tbl_elements.iloc[0, tbl_elements.columns.values.tolist().index('TIME_SLOT_REF1')]
    #     endTimeSlotID = tbl_elements.iloc[0, tbl_elements.columns.values.tolist().index('TIME_SLOT_REF2')]
    #     return startTimeSlotID, endTimeSlotID

    def getTimeSlotIDs(self, doc, tbl_elements):
        '''next step asks for row 0 of dataframe (speech), get value of TSRef1 (start time)'''
        if 'TIME_SLOT_REF1' in tbl_elements.columns:
            startTimeSlotID = tbl_elements.iloc[0, tbl_elements.columns.values.tolist().index('TIME_SLOT_REF1')]
            endTimeSlotID = tbl_elements.iloc[0, tbl_elements.columns.values.tolist().index('TIME_SLOT_REF2')]
        else:
            startTimeSlotID = False
            parentRefID = tbl_elements.iloc[0, tbl_elements.columns.values.tolist().index('ANNOTATION_REF')]
            while startTimeSlotID == False:
                # print(parentRefID)
                parentAnnotation = doc.find('TIER/ANNOTATION/ALIGNABLE_ANNOTATION[@ANNOTATION_ID="%s"]' %parentRefID)
                if not parentAnnotation:
                    parentAnnotation = doc.find('TIER/ANNOTATION/REF_ANNOTATION[@ANNOTATION_ID="%s"]' % parentRefID)
                if 'TIME_SLOT_REF1' in parentAnnotation.attrib:
                    startTimeSlotID = parentAnnotation.attrib['TIME_SLOT_REF1']
                    endTimeSlotID = parentAnnotation.attrib['TIME_SLOT_REF2']
                    newTSR1_column = [startTimeSlotID]
                    newTSR2_column = [endTimeSlotID]
                    for i in range(1,tbl_elements.shape[0]):
                        newTSR1_column.append("NaN")
                        newTSR2_column.append("NaN")
                    tbl_elements.insert(0,'TIME_SLOT_REF1',newTSR1_column)
                    tbl_elements.insert(0, 'TIME_SLOT_REF2', newTSR2_column)
                    # row = tbl_elements.loc[tbl_elements['TIER_ID'] == self.speechTier]
                    # print("speech tier row is %s" %row)
                else:
                    try:
                        parentRefID = parentAnnotation.attrib[('ANNOTATION_REF')]
                    except KeyError:
                        '''this will happen if the speech tier is not time-aligned or the child
                        of a time-aligned tier; this will probably crash SLEXIL, but this is an inadmissible
                        file type anyway, we can figure out how to warn the user later'''
                        print('bailing')
                        startTimeSlotID = float('NaN')
                        endTimeSlotID = float('NaN')
        return startTimeSlotID, endTimeSlotID

    def buildTable(self, doc, lineElements):
        #doc = .eaf file; lineElements = line element and its children
        tbl_elements = pd.DataFrame(e.attrib for e in lineElements)
        startTimeSlotID, endTimeSlotID = self.getTimeSlotIDs(doc, tbl_elements)
        pattern = "TIME_ORDER/TIME_SLOT[@TIME_SLOT_ID='%s']" % startTimeSlotID
        startTime = int(doc.find(pattern).attrib["TIME_VALUE"])
        startTimes = [startTime]
        rowCount = tbl_elements.shape[0]
        '''next step fills in NaN for all the children of the time-aligned tier, but since that 
        messes us up with the getStart/End methods in IjalLine if the *speech tier* isn't aligned,
        let's just give every row a copy of the start and end times'''
        for i in range(1, rowCount):
            # startTimes.append(float('NaN'))
            startTimes.append(startTime)
        '''repeat previous for end times'''
        pattern = "TIME_ORDER/TIME_SLOT[@TIME_SLOT_ID='%s']" % endTimeSlotID
        endTime = int(doc.find(pattern).attrib["TIME_VALUE"])
        endTimes = [endTime]
        for i in range(1, rowCount):
            # endTimes.append(float('NaN'))
            endTimes.append(endTime)

        tbl_times = pd.DataFrame({"START": startTimes, "END": endTimes}) #dataframe of timecodes speech & children
        # print(tbl_times)

        ids = [e.attrib["ANNOTATION_ID"] for e in lineElements] #list of ids
        tierInfo = []
        text = []

        for id in ids:
            parentPattern = "*/*/*/[@ANNOTATION_ID='%s']/../.." % id
            tierAttributes = doc.find(parentPattern).attrib
            tierInfo.append(tierAttributes)
            childPattern = "*/*/*/[@ANNOTATION_ID='%s']/ANNOTATION_VALUE" % id
            elementText = doc.find(childPattern).text
            if (elementText is None):
                elementText = ""
            # print("elementText: %s" % elementText)
            text.append(elementText.strip())

        tbl_tierInfo = pd.DataFrame(tierInfo) #a dataframe of the attributes of speech & children

        tbl_text = pd.DataFrame({"TEXT": text}) #dataframe of text contents of speech & children

        # print("---- tbl_elements")
        # print(tbl_elements)
        #
        # print("---- tbl_tierInfo")
        # print(tbl_tierInfo)
        #
        # print("---- tbl_times")
        # print(tbl_times)
        #
        # print("---- tbl_text")
        # print(tbl_text)

        tbl = pd.concat([tbl_elements, tbl_tierInfo, tbl_times, tbl_text], axis=1)
        preferredColumnOrder = ["ANNOTATION_ID", "LINGUISTIC_TYPE_REF", "START", "END", "TEXT", "ANNOTATION_REF",
                                "TIME_SLOT_REF1", "TIME_SLOT_REF2",
                                "PARENT_REF", "TIER_ID"]
        try:
            tbl = tbl[preferredColumnOrder]
        except KeyError:
            preferredColumnOrder = ["ANNOTATION_ID", "LINGUISTIC_TYPE_REF", "START", "END", "TEXT",
                                    "TIME_SLOT_REF1", "TIME_SLOT_REF2", "TIER_ID"]
            tbl = tbl[preferredColumnOrder]
        textLengths = [len(t) for t in tbl["TEXT"].tolist()]
        tbl["TEXT_LENGTH"] = textLengths
        hasTabs = ["\t" in t for t in tbl["TEXT"].tolist()]
        tbl["HAS_TABS"] = hasTabs
        hasSpaces = [" " in t for t in tbl["TEXT"].tolist()]
        tbl["HAS_SPACES"] = hasSpaces
        # eliminate rows with no text
        # leave it in for now, take the tiers at face value, handle empty lines in toHTML
        tbl = tbl.query("TEXT != ''").reset_index(drop=True)

        # print("---- tbl")
        # print(tbl)

        return (tbl)

