
         #---------------------------------------------
         # check agreement of eaf tiers and tierGuide
         # some tiers in the eaf may not be mentioned in
         # the tierGuide,  but all tierGuide tier ids
         # must be found verbatim in the eaf
         #---------------------------------------------
      tree = etree.parse(self.xmlFilename)
      tierElements = tree.findall("TIER")
      tierIDs = [tier.attrib["TIER_ID"] for tier in tierElements]
      pdb.set_trace()
      documentedTierIDs = list(self.tierGuide.values())
      undocumentedInXmlFile = list(set(documentedTierIDs).difference(set(tierIDs)))
      try:
         assert(len(undocumentedInXmlFile) == 0)
      except AssertionError as e:
         msg = "unrecognized tierIDs in eaf file: "
         for unknown in undocumentedInXmlFile:
            unknowns = "%s %s" % (unknowns, unknown)
         msg = "%s %s" % (msg, unknowns)
         raise Exception(msg)

