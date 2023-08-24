from lxml import etree
import xmltodict
import pprint
import pdb
pp = pprint.PrettyPrinter(indent=2)

xmlFilename = "LushDict.xml"
ns = {"tei": "http://www.tei-c.org/ns/1.0",
      "re": "http://exslt.org/regular-expressions"}

tree = etree.parse(xmlFilename)

query = 'tei:text/tei:body/tei:entry/tei:form[@type="lemma"]/..'  # 701 of these forms
lemmaEntries = tree.xpath(query, namespaces=ns)
len(lemmaEntries) # 701

   #-----------------------------------------------------
   # get the first entry/form/orth in the file
   # then check its tag and text contents
   #-----------------------------------------------------

e0 = tree.xpath('tei:text/tei:body/tei:entry/tei:form[@type="lemma"]/tei:orth', namespaces=ns)[0]
e0.tag  # '{http://www.tei-c.org/ns/1.0}orth'
e0.text # '   ʔa '


   #-----------------------------------------------------
   # find orth elements which contain the target string
   #-----------------------------------------------------

query = 'tei:text/tei:body/tei:entry/tei:form[@type="lemma"]/tei:orth'
len(tree.xpath(query, namespaces=ns))  # 701
query = 'tei:text/tei:body/tei:entry/tei:form[@type="lemma"]/tei:orth[contains(., "ləx̌")]'
len(tree.xpath(query, namespaces=ns))  # 4   

   #-----------------------------------------------------
   # find the orth element with exact match to the target
   #-----------------------------------------------------

query = 'tei:text/tei:body/tei:entry/tei:form[@type="lemma"]/tei:orth[text()="ləx̌"]'
x = tree.xpath(query, namespaces=ns)
len(x)

   #-----------------------------------------------------
   # find the entry element which has the orth element 
   # with exact match to the target
   # element:form:orth
   #-----------------------------------------------------

query = 'tei:text/tei:body/tei:entry/tei:form[@type="lemma"]/tei:orth[text()="ləx̌"]/../..'  # exact match
entry = tree.xpath(query, namespaces=ns)[0]
len(entry)  # 17  forms

   #--------------------------------------------------
   # get the derivative lexemes of the current entry
   #--------------------------------------------------

query = 'tei:form[@type="derivative"]'  # exact match
x = entry.xpath(query, namespaces=ns)
len(x)  # 16

   #------------------------------------------------------
   # find the types of all the forms in the current entry
   # and their distribution.
   # just 1 lemma and 16 derivative forms
   #------------------------------------------------------

query = 'tei:form/@type'  # exact match
types = entry.xpath(query, namespaces=ns)
# ['lemma', 'derivative', 'derivative', 'derivative', 'derivative', 'derivative', 'derivative', 'derivative', 'derivative', 'derivative', 'derivative', 'derivative', 'derivative', 'derivative', 'derivative', 'derivative', 'derivative']
len(types) # 17
pandas.value_counts(pandas.Series([i for i in types]))
   # derivative    16
   # lemma          1

   #------------------------------------------------------
   # find the types of all the forms in the current entry
   # and their distribution.
   # just 1 lemma and 16 derivative forms
   #------------------------------------------------------




#----------------------------------------------------------------------------------------------------
# <gramGrp> grammatical information group,
#  grouping morpho-syntactice information about a lexical item:
#    pos: part of speech
#    gen: gender
#    number:
#    case:
#    iType: inflectional type

entry = """  # copied from LushDict.xml
<entry>
   <form type="lemma">
      <orth>ləx̌</orth>
      <bibl type="Hess">   275.5</bibl>
      <gloss>  *light </gloss>
      <ref type="compare">    húdud under hud(u)  "light it, burn it" </ref>
      <ref type="contrast">    ɬač'ad under ɬač'(a)  "extinguish it" </ref>
      <gramGrp>    
         <usg>   ʔəs^ləx̌ </usg>
         <gloss>   light 
            <note type="cnslt">LG</note>
         </gloss>
      </gramGrp>
   </form>

   <form type="derivative">
      <subc> tra </subc>
      <w>   ləx̌ə-d </w>
      <gloss>  light it 
         <note type="cnslt">LG</note>
      </gloss>
      <gramGrp>
         <usg>   lə́x̌əd tə ləx̌šàd </usg>
         <gloss>   Turn the light on. Light the lamp. 
            <note type="cnslt">LG</note>
         </gloss>
      </gramGrp>
   </form>

   <form type="derivative">
      <subc> bf </subc>
      <w>   ləx̌-yí-d </w>
      <gloss>  light it for him, give him light 
         <note type="cnslt">LG</note>
      </gloss>
   </form>

   <form type="derivative">
      <subc> incep </subc>
      <w>   ləx̌-íl </w>
      <gloss>  grow light, day </gloss>
      <gramGrp>
         <usg>   ləx̌iləxʷ ʔal tiʔiɬ ɬup. </usg>
         <gloss>   It became daylight early. 
            <note type="cnslt">ML 12.270</note>
         </gloss>
      </gramGrp>
   </form>

   <form type="derivative">
      <subc> ipfx </subc>
      <w>   tu^lə́x̌-i(l) </w>
      <gloss>  this morning 
         <note type="cnslt">EB</note>
      </gloss>
      <lang>  SL </lang>
   </form>

   <form type="derivative">
      <subc> nom </subc>
      <w>   s^ləx̌-íl </w>
      <gloss>  *day </gloss>
      <note type="cm">   as opposed to night </note>
      <oVar>   s^lə́x̌-i</oVar>
      <lang> SL </lang>
      <ref type="contrast">    ɬáx̌il  "night" </ref>
      <ref type="compare">    kʷáčil  "dawn, tomorrow" </ref>
      <ref type="compare">    ɬup  "morning" </ref>
      <ref type="compare">    dat  "twenty-four hour period" </ref>
      <ref type="compare">    dadatut  "morning" </ref>
      <gramGrp>
         <usg>   háʔɬ s^ləx̌ìl </usg>
         <gloss>   nice day (a greeting) 
            <note type="cnslt">LG</note>
         </gloss>
      </gramGrp>
      <gramGrp>
         <usg>   làʔb háʔɬ s^ɬəx̌ìl </usg>
         <gloss>   a real nice day 
            <note type="cnslt">LG</note>
         </gloss>
      </gramGrp>
      <gramGrp>
         <usg>   pùt háʔɬ s^ləx̌ìl </usg>
         <gloss>   a very nice day 
            <note type="cnslt">ML</note>
         </gloss>
      </gramGrp>
      <gramGrp>
         <usg>   s^ɬáx̌il gʷəl bə^ləx̌il. </usg>
         <gloss>   Night and again day(light). </gloss>
      </gramGrp>
      <gramGrp>
         <usg>   ʔáhəxʷ dxʷ^ʔal ti s^ləx̌íls. </usg>
         <gloss>   He (stayed) there all that day. 
            <note type="cnslt">EC 5.85</note>
         </gloss>
      </gramGrp>
   </form>

   <form type="derivative">
      <subc> isfx </subc>
      <w>   ʔu^ləx̌-íl-əxʷ </w>
      <gloss>  *dawn 
         <note type="cnslt">LL</note>
      </gloss>
      <note type="cm">   lit, It is now light. </note>
      <ref type="compare">    ləgʷəqíləxʷ under gʷəqíl  "dawn" </ref>
   </form>

   <form type="derivative">
      <subc> isfx </subc>
      <w>   ləx̌-íl-ad-əb </w>
      <gloss>  early breakfast 
         <note type="cnslt">EK</note>
      </gloss>
   </form>

   <form type="derivative">
      <subc> lx </subc>
      <w>   ləx̌=šád </w>
      <gloss type="tool">   *lamp </gloss>
      <gramGrp>
         <usg>   púʔud tə ləx̌šàd </usg>
         <gloss>   Blow out the lamp. 
            <note type="cnslt">LG</note>
         </gloss>
      </gramGrp>
      <gramGrp>
         <usg>   ʔu^ɬáč' tə ləx̌šàd </usg>
         <gloss>   The light went out. 
            <note type="cnslt">EK</note>
         </gloss>
      </gramGrp>
   </form>

   <form type="derivative">
      <subc> mv </subc>
      <w>   ləx̌=šáhəd-əb </w>
      <gloss>  Turn the light on. 
         <note type="cnslt">EK</note>
      </gloss>
   </form>

   <form type="derivative">
      <subc> bf </subc>
      <w>   ləx̌=šád-i-d </w>
      <gloss>  Give him light. 
         <note type="cnslt">EK</note>
      </gloss>
   </form>

   <form type="derivative">
      <subc> red2 </subc>
      <w>   ləx̌+^ləx̌=šád-əb </w>
      <gramGrp>
         <usg>   ʔalc̕uləx̌^ləx̌šádəb tə x̌ʷìqʷadiʔ </usg>
         <gloss>   lightning (lit, flashing thunder) 
            <note type="cnslt">LG</note>
         </gloss>
      </gramGrp>
   </form>

   <form type="derivative">
      <subc> red1 </subc>
      <w>   lí+ləx̌+^ləx̌=šàd </w>
      <gramGrp>
         <usg>   ʔəlc̕ulíləx̌+^ləx̌šàd ʔə tə pàstəd </usg>
         <gloss>   flashlight (lit, the little flashing light of the whiteman) 
            <note type="cnslt">LG</note>
         </gloss>
      </gramGrp>
   </form>

   <form type="derivative">
      <subc> lx </subc>
      <w>   ləx̌-il=ič </w>
      <gramGrp>
         <usg>   ƛ'uləx̌iličəxʷ əlgʷəʔ </usg>
         <gloss>   they would be enveloped with light 
            <note type="cnslt">HM daylight</note>
         </gloss>
      </gramGrp>
   </form>

   <form type="derivative">
      <subc> red1 </subc>
      <w>   ʔəlc̕u-lí+^ləx̌ </w>
      <gloss>  it flashes (slowly, dimly) 
         <note type="cnslt">LG</note>
      </gloss>
   </form>

   <form type="derivative">
      <subc> red2 </subc>
      <w>   ʔəlc̕u-lə́x̌+^ləx̌ </w>
      <gloss>  it flashes 
         <note type="cnslt">LG</note>
      </gloss>
   </form>

   <form type="derivative">
      <subc> tra </subc>
      <w>   ləx̌+^ləx̌-á-d </w>
      <gloss>  light (all the candles) 
         <note type="cnslt">LG</note>
      </gloss>
   </form>
</entry>
"""

davidEntry = """
<Lex LexID="LX001" Date="" Update="" Spkr="" Rschr="TMH">
   <Orth>ləx̌</Orth>
   <IPA>ləx̌</IPA>
   <Cf CrossRef="LX????"{húdud}></Cf>
   <Cf CrossRef="LX????"{ɬač'ad}></Cf>
   <Def>
     <L1>light</L1>
     <Line LnRef="Ex001"/>
   </Def>
   <Drvn LexIDRef="LX002"/>
   <Drvn LexIDRef="LX003"/>
   <Drvn LexIDRef="LX004"/>
   <Comment>Hess 275.5</Comment>
</Lex>

<Lex LexID="LX002" Date="" Update="" Spkr="LG" Rschr="TMH" >
   <Orth>ləx̌əd</Orth>
   <POS>vt</POS>
   <IPA>ləx̌əd</IPA>
   <Lit>ləx̌ ‘light’ + -d ‘ICS’</Lit>
   <Def>
      <L1>light it</L1>
      <Line LnRef="Ex0002"/>
   </Def>
   <Root LexIDRef="LX001">
</Lex>
<Lex LexID="LX003" Date="" Update="" Spkr="LG" Rschr="TMH" >
   <Orth>ləx̌yíd</Orth >
   <POS>v3</POS>
   <IPA>ləx̌yíd</IPA>
   <Lit>ləx̌ ‘light’ + -yi ‘DAT’ + -d ‘ICS’</Lit>
   <Def>
      <L1>light it for him, give him light</L1>
   </Def>
   <Root LexIDRef="LX001">
</Lex>
<Lex LexID="LX004" Date="" Update="" Spkr="" Rschr="TMH" >
   <Orth>ləx̌íl</Orth>
   <POS>vi</POS>
   <IPA>ləx̌íl</IPA>
   <Lit>ləx̌ ‘light’ + -il ‘INCH’</LIT>
   <Def>
      <L1>grow light, day</L1>
      <Ln LnRef="Ex0003"/>
   </Def>
   <Root LexIDRef="LX001">
</Lex>
<Ex ExID="EX001" Date="" Update="" Spkr="LG" Rschr="TMH" >
   <Line>ʔəsləx̌</Line>
   <Mrph />
   <ILEG />
   <L1Gloss>light</L1gloss>
</Ex>
<Ex ExID="EX002" Date="" Update="" Spkr="LG" Rschr="TMH" >
   <Line>lə́x̌əd tə ləx̌šàd</Line>
   <Mrph />
   <ILEG />
   <L1Gloss>Turn the light on. Light the lamp.</L1gloss>
</Ex>
<Ex ExID="EX003" Date="" Update="" Spkr="ML" Rschr="TMH" >
   <Line>ləx̌iləxʷ ʔal tiʔiɬ ɬup.</Line>
   <Mrph />
   <ILEG />
   <L1Gloss>It became daylight early.</L1gloss>
   <Comment>ML 12.270</Comment>
</Ex>

You’ll notice first off that the root-based entry gets broken up into
4 lexeme-based entries, and the example sentences get stored in their
own <Ex> elements. The <Root> element in the <Lex> elements provides a
link back to the root.

I’m not sure what we can do programmatically about the <POS> and <LIT>
elements. The Dictionary conspicuously does not provide actual
part-of-speech information, but some of that can be recovered from the
<subc> element Deryle provides (I’m guessing he added that by
hand). We could make a transformation key (tra = vt; bf = v3; incep =
vi, etc.) that would get some of it. Likewise the <Lit> elements could
be paternally populated since Deryle’s XML breaks up derivatives,
which is appropriate only if they are not headwords for a
dictionary. So a form like this

   <w> ləx̌ə-d </w>

would appear in our XML as

   <Orth> ləx̌əd</Orth>

but the parsing of the word would be in a <Lit> element

   <Lit>ləx̌ ‘light’ + -d ‘ICS’</Lit>

The problem would be getting the glosses of the pieces, the lexical
bit having the gloss of the root and the rest coming, I guess, from an
affix dictionary of some kind. In retrospect, I could have structured
the <Lit> element better, into a string of <Mrpm><Gloss> elements, but
that doesn’t really affect the problem at hand too much.

The parsing of the lines in the <Ex> elements is probably not worth
doing at this point. If at some time in the future, we import the
lines from the Beck & Hess text collections, we could leverage that to
do some exemplar-based parsing. My database does that already, though
not in a really sophisticated way. Joshua Crowley built an FST for
Lushootseed based on those texts that might be useful to apply to the
words/sentences in the dictionary. Though, to be honest, doing the
parsing by hand is a useful way to learn how the language works.

I’m not sure what the <bibl type> references are to and there is
probably other obscure stuff, but that is what the <Comments> element
is for.

The two data structures seem quite different to me, but probably less
so to you.
 
"""
