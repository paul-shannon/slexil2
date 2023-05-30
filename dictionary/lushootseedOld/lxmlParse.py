from lxml import etree
#  xmlFilename = "LushDict.xml"
#  parser = etree.XMLParser(remove_blank_text=True)
#  tree = etree.parse(xmlFilename, parser)
#  tree.write("lushootseedDictionary.xml", pretty_print=True)

xmlFilename = "lushootseedDictionary.xml"

ns = {"tei": "http://www.tei-c.org/ns/1.0"}
tree = etree.parse(xmlFilename, parser)
tree.write("lushootseedDict.xml", pretty_print=True)

root = tree.getroot()
nss = root.nsmap

print("root child count: %d" % len(root.getchildren()))  # 2

entries = tree.xpath("//TEI/text/body/entry", namespaces=nss)
print("entry count: %d" % len(entries))  # 3599
forms = tree.xpath("//TEI/text/body/entry/form", namespaces=nss)
print("form count: %d" % len(forms))  # 8512
orths = tree.xpath("//TEI/text/body/entry/form/orth", namespaces=nss)
len(orths) # 3599

entries[1686].xpath("form")[0].xpath("orth")[0].text          # '   ləx̌ '
entries[1686].xpath("form")[0].xpath("orth")[0].text.strip()  # 'ləx̌'

print(etree.tostring(entries[1686], pretty_print=True, encoding="unicode"))

                     #--------------
                     # ləx̌
                     #--------------
print(etree.tostring(entries[1686], pretty_print=True, encoding="unicode"))

#  <entry xmlns:xi="http://www.w3.org/2001/XInclude" xmlns:svg="http://www.w3.org/2000/svg" xmlns:math="http://www.w3.org/1998/Math/MathML" xmlns:tei="http://www.tei-c.org/ns/1.0">
#    <form type="lemma">
#      <orth>   ləx̌ </orth>
#      <bibl type="Hess">   275.5</bibl>
#      <gloss>  *light </gloss>
#      <ref type="compare">    húdud under hud(u)  "light it, burn it" </ref>
#      <ref type="contrast">    ɬač'ad under ɬač'(a)  "extinguish it" </ref>
#      <gramGrp>
#        <usg>   ʔəs^ləx̌ </usg>
#        <gloss>   light <note type="cnslt">LG</note> </gloss>
#      </gramGrp>
#    </form>
#    <form type="derivative">
#      <subc> tra </subc>
#      <w>   ləx̌ə-d </w>
#      <gloss>  light it <note type="cnslt">LG</note> </gloss>
#      <gramGrp>
#        <usg>   lə́x̌əd tə ləx̌šàd </usg>
#        <gloss>   Turn the light on. Light the lamp. <note type="cnslt">LG</note> </gloss>
#      </gramGrp>
#    </form>
#    <form type="derivative">
#      <subc> bf </subc>
#      <w>   ləx̌-yí-d </w>
#      <gloss>  light it for him, give him light <note type="cnslt">LG</note> </gloss>
#    </form>
#    <form type="derivative">
#      <subc> incep </subc>
#      <w>   ləx̌-íl </w>
#      <gloss>  grow light, day </gloss>
#      <gramGrp>
#        <usg>   ləx̌iləxʷ ʔal tiʔiɬ ɬup. </usg>
#        <gloss>   It became daylight early. <note type="cnslt">ML 12.270</note> </gloss>
#      </gramGrp>
#    </form>
#    <form type="derivative">
#      <subc> ipfx </subc>
#      <w>   tu^lə́x̌-i(l) </w>
#      <gloss>  this morning <note type="cnslt">EB</note> </gloss>
#      <lang>  SL </lang>
#    </form>
#    <form type="derivative">
#      <subc> nom </subc>
#      <w>   s^ləx̌-íl </w>
#      <gloss>  *day </gloss>
#      <note type="cm">   as opposed to night </note>
#      <oVar>   s^lə́x̌-i</oVar>
#      <lang> SL </lang>
#      <ref type="contrast">    ɬáx̌il  "night" </ref>
#      <ref type="compare">    kʷáčil  "dawn, tomorrow" </ref>
#      <ref type="compare">    ɬup  "morning" </ref>
#      <ref type="compare">    dat  "twenty-four hour period" </ref>
#      <ref type="compare">    dadatut  "morning" </ref>
#      <gramGrp>
#        <usg>   háʔɬ s^ləx̌ìl </usg>
#        <gloss>   nice day (a greeting) <note type="cnslt">LG</note> </gloss>
#      </gramGrp>
#      <gramGrp>
#        <usg>   làʔb háʔɬ s^ɬəx̌ìl </usg>
#        <gloss>   a real nice day <note type="cnslt">LG</note> </gloss>
#      </gramGrp>
#      <gramGrp>
#        <usg>   pùt háʔɬ s^ləx̌ìl </usg>
#        <gloss>   a very nice day <note type="cnslt">ML</note> </gloss>
#      </gramGrp>
#      <gramGrp>
#        <usg>   s^ɬáx̌il gʷəl bə^ləx̌il. </usg>
#        <gloss>   Night and again day(light). </gloss>
#      </gramGrp>
#      <gramGrp>
#        <usg>   ʔáhəxʷ dxʷ^ʔal ti s^ləx̌íls. </usg>
#        <gloss>   He (stayed) there all that day. <note type="cnslt">EC 5.85</note> </gloss>
#      </gramGrp>
#    </form>
#    <form type="derivative">
#      <subc> isfx </subc>
#      <w>   ʔu^ləx̌-íl-əxʷ </w>
#      <gloss>  *dawn <note type="cnslt">LL</note> </gloss>
#      <note type="cm">   lit, It is now light. </note>
#      <ref type="compare">    ləgʷəqíləxʷ under gʷəqíl  "dawn" </ref>
#    </form>
#    <form type="derivative">
#      <subc> isfx </subc>
#      <w>   ləx̌-íl-ad-əb </w>
#      <gloss>  early breakfast <note type="cnslt">EK</note> </gloss>
#    </form>
#    <form type="derivative">
#      <subc> lx </subc>
#      <w>   ləx̌=šád </w>
#      <gloss type="tool">   *lamp </gloss>
#      <gramGrp>
#        <usg>   púʔud tə ləx̌šàd </usg>
#        <gloss>   Blow out the lamp. <note type="cnslt">LG</note> </gloss>
#      </gramGrp>
#      <gramGrp>
#        <usg>   ʔu^ɬáč' tə ləx̌šàd </usg>
#        <gloss>   The light went out. <note type="cnslt">EK</note> </gloss>
#      </gramGrp>
#    </form>
#    <form type="derivative">
#      <subc> mv </subc>
#      <w>   ləx̌=šáhəd-əb </w>
#      <gloss>  Turn the light on. <note type="cnslt">EK</note> </gloss>
#    </form>
#    <form type="derivative">
#      <subc> bf </subc>
#      <w>   ləx̌=šád-i-d </w>
#      <gloss>  Give him light. <note type="cnslt">EK</note> </gloss>
#    </form>
#    <form type="derivative">
#      <subc> red2 </subc>
#      <w>   ləx̌+^ləx̌=šád-əb </w>
#      <gramGrp>
#        <usg>   ʔalc̕uləx̌^ləx̌šádəb tə x̌ʷìqʷadiʔ </usg>
#        <gloss>   lightning (lit, flashing thunder) <note type="cnslt">LG</note> </gloss>
#      </gramGrp>
#    </form>
#    <form type="derivative">
#      <subc> red1 </subc>
#      <w>   lí+ləx̌+^ləx̌=šàd </w>
#      <gramGrp>
#        <usg>   ʔəlc̕ulíləx̌+^ləx̌šàd ʔə tə pàstəd </usg>
#        <gloss>   flashlight (lit, the little flashing light of the whiteman) <note type="cnslt">LG</note> </gloss>
#      </gramGrp>
#    </form>
#    <form type="derivative">
#      <subc> lx </subc>
#      <w>   ləx̌-il=ič </w>
#      <gramGrp>
#        <usg>   ƛ'uləx̌iličəxʷ əlgʷəʔ </usg>
#        <gloss>   they would be enveloped with light <note type="cnslt">HM daylight</note> </gloss>
#      </gramGrp>
#    </form>
#    <form type="derivative">
#      <subc> red1 </subc>
#      <w>   ʔəlc̕u-lí+^ləx̌ </w>
#      <gloss>  it flashes (slowly, dimly) <note type="cnslt">LG</note> </gloss>
#    </form>
#    <form type="derivative">
#      <subc> red2 </subc>
#      <w>   ʔəlc̕u-lə́x̌+^ləx̌ </w>
#      <gloss>  it flashes <note type="cnslt">LG</note> </gloss>
#    </form>
#    <form type="derivative">
#      <subc> tra </subc>
#      <w>   ləx̌+^ləx̌-á-d </w>
#      <gloss>  light (all the candles) <note type="cnslt">LG</note> </gloss>
#    </form>
#  </entry>
#   
