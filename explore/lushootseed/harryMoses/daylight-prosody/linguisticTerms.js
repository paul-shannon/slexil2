// https://sites.ualberta.ca/~dbeck/valency.pdf: a taxonomy of lushootseed valency-increasing affixes
// mechanism by which these terms are included:
// kb.pre has, for instance,
//   nominalization of LINGREF(adjunct, adjunct) and circumstantial
// kb.m4 has this macro:
//   m4_define(LINGREF, <button id="refButton" onclick="ref('$1');">$2</button>)m4_dnl
// which ceates a button labeled with arg1, where ref is a function
// in pshannon.js:
// function ref(key) {
//   $("#refPopupTitle").html(key)
//   lookupReference(key);
//   $("#refPopup").toggle();
//   };
// function lookupReference(key){
//   $("#refText").html(linguisticTerms[key]);
//   };
// in insertCustomCode.sed:
//   the <body> tag is expanded to be <body><div id="refPopup"><div id="refText"></div></div>
// which is invoked out of
//    make kb customize
// and see via
//    make view
// custom.html adds <script src="../linguisticTerms.js"></script>
linguisticTerms = {
"COPULA":`
<ul>
 <li>word or phrase that links the subject of a sentence to a subject
 complement, such as the word "is" in the sentence "The sky is blue" or
 the phrase "was not being" in the sentence "It was not being used." The
 word copula derives from the Latin noun for a "link" or "tie" that
 connects two different things.

 <li> also called a linking verb, which also includes verbs of
     perception such as look, sound, or taste and some other verbs
     that describe the subject, such as seem, become, or remain.

</ul>
`,
    
    "line1.english":`
      <img src="images/line1-diagram.png" width=400>
      <img src="images/line1-diagram-v2.png" width=400>
    `,
"PREDICATE":`
  Kroevers <i>predicate proper</i> [p58] may be a word whose English translation is a verb.
  However, throughout Salish, it is also perfectly possible for the predicate proper to be
  something translatable as an adjective or a noun.  Such predicates take whatever sort of 
  person marking is appropriate for intransivitve predicates in the language in question.
  <p>
  We should say that nouns and adjectives as well as verbs may be the predicates
  of clauses in Salish languages.
  <p>
   Alternatively (as Jelinek and Demrs recommend) we shouldclaim that Salish languages
   lack a sytactically relevant distinction between "noun", "verb", and "adjective"; 
   instead there is a single undifferentiated class (to be labeled, perhaps, "potential
   predicate")into which the Salish translation equivalent of Eglsih nouns, verbs, and
   adjectives fall.
  <p> I return later (section 1.5.5)to the issue of what major lexical classes ought
   to be recognized in Salish.  For now, it will help to keep matters straight if we 
   carefully distinguish between syntactic positions, such as "predicate" -- the 
   the syntactic position whtat is followed by subject and object nominal expression
   in unmarked order, that may be proceeded by auxilliaries or certain adverbs [p59]
`,
    

"COMPLEMENT":`
`,
    
"TENSE": `<b>Tense</b><p>
Thom Hess, LG1, p49: &nbsp; Obligatory in English, where
every sentence must locate the event before, after,
or during the moment of speaking (or with reference to some other 
event).
<p>
Optional in Lushootseed, tense is usually not mentioned.
Lushootseed grammar is instead much concerned with aspect, which
describes the period of time within which an event or process occurs.
<p>
Lushootseed verbs are either static or dynamic.  If static, they
typically bear the stative prefix <i><b>ʔəs-</b></i>.  If dynamic,
the divide into two groups called <b>perfective</b> 
(prefix <i><b>ʔu-</b></i>) and <b>imperfective</b> 
(prefix <i><b>lə-</b><i> for progressive, <i><b>ləs-</b></i> for
progressive state).
`,
    
"PERF": `<h5>Perfective Aspect</h5>

  The perfective aspect (abbreviated pfv), sometimes called the
  aoristic aspect, is a grammatical aspect that describes an action
  viewed as a simple whole; i.e., a unit without interior
  composition. The perfective aspect is distinguished from the
  imperfective aspect, which presents an event as having internal
  structure (such as ongoing, continuous, or habitual actions).

<p>

  The perfective is often thought of as for events of short duration
  (e.g., "John killed the wasp"). However, this is not necessarily
  true—a perfective verb is equally right for a long-lasting event,
  provided that it is a complete whole; e.g., Tarquinius Superbus
  regnavit annos quinque et viginti (Livy) "Tarquin the Proud reigned
  for 25 years." It simply "presents an occurrence in summary,
  viewed as a whole from the outside, without regard for the internal
  make-up of the occurrence."



<h6>Perfective Aspect vs Perfect Tense</h6>

A <i>perfect</i> tense (abbreviated <b>PERF</b> or <b>prf</b>) is a
grammatical form used to describe a past event with present relevance,
or a present state resulting from a past situation. For example, "I
have put it on the table" implies both that I put the object on the
table and that it is still there; "I have been to France" conveys that
this is a part of my experience as of now; and "I have lost my wallet"
implies that this loss is troublesome at the present moment. A perfect
tense does not necessarily have to be perfective in aspect. For
example, "I have been waiting here for an hour" and "I have been going
to that doctor all my life" are perfect but also imperfective in
aspect.

`,
    
    "And-fronting": `<b><i>And</i>-fronting</b>
      <ul>
        <li> Kroeber p376: and-fronting of determiner phrases (DPs) is rare in Coast Salish languages 
             generaly, but fairly common in Lushootseed. 
        <li>Hess v1 p122: The sentential adverb <i>gʷəl</i>, in addtion to starting
    sentences ("and then...") in long narratives, is also used to topicalize.  This is
    achieved by treating the topic as an entire clause and using <i>gʷəl</i> to introduce
    the following clause.
      </ul>
    <h5>More generally:</h5>
      <ul>
        <li> <b>Emphasis</b>: modifying the sense of the sentence.  A <i>sentential adverb</i> is a single word or short phrase, usually interrupting
        normal syntax, used to lend emphasis to words immediately proximal to the adverb:  <i>
        I did, <b>indeed</b>, complete the task. </i>  Or "Reluctantly, he completed the task.".
        <li> <b>Topicalization</b>:  the initial position of the adverb is not unlike the <i>wh</i>-position,
        which is unspecified for the kind of <i>wh</i>-element that can occupy it.  The fronted elements
        are <b>topics</b> representing information that is already part of the discourse (aka, old information).
        All of these fronted elements are pronounced with a pause after the initial phrase.
        <li> Unlike <i>wh</i>-elements, topicalization never demonstrates inversion or complementary
        distribution. (More detail <a href="http://primus.arts.u-szeged.hu/bese/Chapter7/7.5.1.htm#1307" target="_blank"> here</a>.
        </ul>`,
    

    "ECS": `<b>ECS: Event External Causative </b> &nbsp; <i>-txʷ</i>
     <p> Adds participant (a trajector) which is initiator of separate process of which it is not the trajector
     (the primary clausal figure). 

      <p>The notion of ‘separate process’ is a matter of construal and in
      practice there is considerable overlap in direct- and indirect-causation (ICS).

     <p> Two papers by David Beck:
      <ul>
      <li><a href="https://sites.ualberta.ca/~dbeck/CAUS.pdf" target="_blank">Transitivity and Causation in Lushootseed Morphology</a>.
      <li><a href="https://era.library.ualberta.ca/items/0ebf0b27-5436-404f-b7d8-8c74dd53d35a/view/108859df-0420-4df0-8d16-7208c7d2d2e3/IJAL_75_2009_533_clean.pdf" target="_blank">
         A Taxonomy and Typology of Lushootseed Valency-increasing Suffixes</a>
      </ul>

     <p>
      <b>TRAJECTOR</b> and <b>LANDMARK</b> are the terms proposed by R. Langacker to describe
      the semantics of the linguistic expressions denoting simple and complex
      events, in which one object (the Trajector) is moving or undergoing
      changes in relation to another object (the Landmark).  The line along which
      the Trajector is moving, either literally or metaphorically, is called the
      <b>Path</b>.

      <p>
       Two important constraints of Lushootseed grammar:
       <ol><li> Only one third-person direct actant (subject or direct object) may be overt in a clause: 
          in transitive clauses, third-person subjects are elided; first- and second-person subjects 
          in transitive clauses are realizable as pronominals, which are not NPs.
        <li> Oblique (intransitive) objects are not in the verb’s profile and surface as a PP.
       </ol>
     `,

    "determiner":`<b>Determiner</b>
     <p>
     A word, phrase, or affix that occurs together with a noun or noun phrase
     and serves to express the reference of that noun or noun phrase in the
     context. That is, a determiner may indicate whether the noun is referring
     to a definite or indefinite element of a class, to a closer or more distant
     element, to an element belonging to a specified person or thing, to a
     particular number or quantity, etc.
     <ul>
       <li> <b>articles:</b> definite or indefinite, <i>a, an, the</i>
       <li> <b>demonstratives:</b> <i>this, that</i>
       <li> <b>possessive determiners:</b> <i>my, hers, their</i>
       <li> <b>ordinal numerals:</b> <i>first, second</i> (last?)
       <li> <b>quantifiers:</b>  <i>many, both, all, no</i>
       <li> <b>distributive:</b>  <i>each, any</i>
       <li> <b>interrogative:</b> <i>which</i>
     </ul>

    `,

    "demonstrative": `<b>Demonstratives</b>
    <p>
    Words which distinguish entities of interest, often used in spatial or discourse deixis,
    or as anaphora.  

    <h5>English examples</h5> 
     <ul>
       <li> Asdjective: <i>put <b>that</b> hat on</i>.  
       <li> As pronoun: <i>put <b>that</b> on</i>.
       <li> As adverb: <i>He is not <b>that</b> nice</i>. <i>I came <b>this</b> close</i>. (with accompanying gesture).
     </ul>

   <h5>Lushootseed Reader volume 1, Lesson 15, p77: Demonstratives</h5>
    The demonstrative systems (pronomial, adjectival, and adverbial) are complex in Lushootseed
    for several reasons:
     <ul>
       <li>  They involve a fairly large number of concepts.
       <li> There is considerable variation among speakers in their use.  
       <li> Adjectival and adverbial demonstratives can  enter into a variety of combinations creating 
            still more, and often quite subtle, distinctions than occur in either subclass taken alone.
     </ul>
    The basic system, however, is straight forward; and that is what is presented here.  The complex
    and sometimes idiosyncratic combinations are dealt with in footnotes as they occur in the texts.
    <p>
    Five concepts are marked in the basic adjectival system.  These are distal, proximal, unique
    reference, non-contrastive (or neutral), and hypothetical and/or remote.  Each of these can
    be futhher marked for feminine.  The specific forms in Northern and Southern Lushootseed
    differ in several cases.

    <table>
     <caption>Adjectival Demonstratives</caption>
      <tr>
        <th>dialect</th>
        <th>distal</th>
        <th>proximal</th>
        <th>unique reference</th>
        <th>non-contrastive</th>
        <th>hypothetical and/or remote</th>
      </tr>
      <tr>
        <td>NL</td>
        <td>tiʔiɬ</td>
        <td>tiʔəʔ</td>
        <td>ti</td>
        <td>tə</td>
        <td>kʷi</td>
      </tr>
      <tr>
        <td>SL</td>
        <td>tiiɬ</td>
        <td>ti</td>
        <td>šə</td>
        <td>tə</td>
        <td>kʷi</td>
      </tr>
      <tr>
        <td>NL <i>fem</i></td>
        <td>tsiʔiɬ</td>
        <td>tsiʔəʔ</td>
        <td>tsi</td>
        <td>tsə</td>
        <td>kʷsi</td>
      </tr>
      <tr>
        <td>SL <i>fem</i></td>
        <td>tsiiɬ</td>
        <td>tsi</td>
        <td>sə</td>
        <td>tsə</td>
        <td>kʷsi</td>
      </tr>
    </table>

    `,

    "deixis":

    `<i>DIKE-sis</i>. Reference by means of an expression whose interpretation is
     relative to the (usually) extralinguistic context of the utterance, such as:
        <ul>
           <li>who is speaking
           <li>the time or place of speaking
           <li>the gestures of the speaker
           <li>the current location in the discourse
        </ul>

      wikipedia: The use of general words and phrases to refer to a specific
      time, place, or person in context, e.g., the words tomorrow, there, and
      they. Words are deictic if their semantic meaning is fixed but their
      denoted meaning varies depending on time and/or place. Words or phrases
      that require contextual information to be fully understood—for example,
      English pronouns—are deictic. Deixis is closely related to anaphora. In
      linguistic anthropology, deixis is treated as a particular subclass of the
      more general semiotic phenomenon of indexicality, a sign "pointing to"
      some aspect of its context of occurrence.  <p>

      <ul>
         <li> <b>deictic center</b>:  I, here, now
         <li> <b>time deixis</b>: [before, recently, yesterday] now [later, tomorrow, soon]
         <li> <b>space</b>: [there] here [there]
         <li> <b>person</b>: you, me, she/he, they
         <li> <b>deictic projection</b>:  speaker is not in the deictic center: <i> I am coming home now.</i>
         <li> <b>discourse deixis</b>:  <i>That was an amazing account.</i>
         <li> <b>social</b>:  T-V distinction, Latin "tu" and "vos", for languages with at least two
               second person pronouns.
      </ul>

     The terms deixis and <b>indexicality</b> are frequently used almost
     interchangeably, and both deal with essentially the same idea of
     contextually-dependent references. However, the two terms have different
     histories and traditions. In the past, deixis was associated specifically
     with spatiotemporal reference, and indexicality was used more broadly.[16]
     More importantly, each is associated with a different field of
     study. Deixis is associated with linguistics, and indexicality is
     associated with philosophy[17] as well as pragmatics.[18]

     <i>deixis</i> refers to words and phrases, such as "me" or "here", that cannot be fully understood
     without additional contextual information—in this case, the identity of the speaker ("me") and
     the speaker's location ("here"). Words are deictic if their semantic meaning is fixed but their
     denoted meaning varies depending on time and/or place. Words or phrases that require contextual
     information to convey any meaning—for example, English pronouns—are deictic.


    `,

    "anaphor":
    `

    The use of an expression whose interpretation depends upon another
    expression in context (its antecedent or postcedent).

    <p>In a narrower sense, <i>anaphora</i> is the use of an expression that
    depends specifically upon an antecedent expression and thus is contrasted
    with <i>cataphora</i>, which is the use of an expression that depends upon a
    postcedent expression. The anaphoric (referring) term is called an
    anaphor. 

    <p>For example, in the sentence <i>Sally arrived, but nobody saw her</i>, the
    pronoun <i>her</i> is an anaphor, referring back to the antecedent Sally. In the
    sentence <i>Before her arrival, nobody saw Sally</i>, the pronoun <i>her</i> refers
    forward to the postcedent Sally, so <i>her</i> is now a cataphor (and an anaphor in
    the broader, but not the narrower, sense). 

    <p>In <i>When they saw Ruth, the men looked slightly abashed</i>,
     the word <i>they</i> is used as a cataphor for <i>the men</i>.

    <p>Usually, an anaphoric expression is a proform or some other kind of
    deictic (contextually-dependent) expression. Both anaphora and cataphora
    are species of endophora, referring to something mentioned elsewhere in a
    dialog or text.

    <p>A linguistic entity which indicates a referential tie to some other linguistic 
     entity in the same text.

    <p>Thus an anaphor is a <a href="https://en.wikipedia.org/wiki/Pro-form"
     target="_top">proform</a> or some other kind of deictic
     (contextually-dependent) expression, where <i>proform</i> is a word or
     expression which stands in for (expresses the same content as) another
     word, phrase, clause or sentence where the meaning is recoverable from
     context, <i>pronouns</i> being the best known.
    `,
    
    "CED.WORDS":
    `
    <h5>čəd words: predicate particles</h5>
    <ul>
      <li> čəd: I, me
      <li> čəɬ:  we, us
      <li> čəxʷ: you (singular)
      <li> čəɬəp: you folks
    </ul>
    <h5>additional comments</h5>
    <ul>
       <li> čəɬ<sup>2</sup>: [Skagit (only?)] make or hunt for one's use, go after. LD 63
       <li> <i>ləčəɬ čəd</i>: I am on my way to make something.
       <li> <i>čəɬ ƛ’əlayʔ</i>: make canoe, ’make canoes/a canoe/canoes in general’
       <li> contrast <i>čəɬ ti ƛ’əlayʔ</i> ‘make that canoe/the canoe we were talking about/particular canoes’
       <li> David Beck: this is one of a very few verbs that can be used with a noun without a demonstrative or determiner.
    </ul>
    `,

    "HABITUAL":
    `
    <a href="https://en.wikipedia.org/wiki/Habitual_aspect" target="_top">wikipedia</a>: 
    the aspect of a verb is a grammatical category that defines
    the <b>temporal flow</b> (or lack thereof) in a given action, event, or
    state. 

    <p> While habituals "describe a situation which is characteristic of an
    extended period of time" (Comrie 1985: 27), iteratives consist of "repeated
    occurrences of the same situation".

    <p>The habitual aspect (abbreviated HAB) is not to be confused with iterative 
    aspect or frequentative aspect, specifies an action as occurring habitually: the 
    subject performs the action usually, ordinarily, or customarily. As such, the 
    habitual aspect provides structural information on the nature of the subject referent:
    <ul> 
       <li> "John smokes" being interpretable as "John is a smoker"
       <li> "Enjoh habitually gets up early in the morning" as "Enjoh is an early bird". 
    </ul>

    Some sense of intrinsic, inborn is carried: an event or state is characteristic of a period of time.

     <p>
     <b>iterative aspect</b>: or event-internal pluractionality, expresses the repetition
     of an event observable on a single occasion.  <i>she is drumming</i>
     <b>frequentive aspect</b>: like habitual, this implies multiple occasions.  
      <a href="https://en.wikipedia.org/wiki/Frequentative" target="_top">wikipedia</a>
      describes English <i>-le</i> and <i>-er</i> as frequentive suffixes, (grunt -> gruntle, jig -> jiggle)
       and reduplication (i.e. <i>murmur</i>) and vowel grades (i.e, <i>teeter-totter</i> and <i>pitter-patter</i>).
     English present tense often has a frequentive aspect: <i>I walk to work</i>.  
     <p>

     The habitual aspect is a type of imperfective aspect, which does not depict an event as 
     a single entity viewed only as a whole but instead specifies something about its internal
     temporal structure.
     <p>

    The habitual aspect is a form of expression connoting repetition or continuous existence of a state of 
    affairs. In standard English, present tense, there is no special grammatical marker for the habitual; 
    the simple present is used, as in <i>I go there (every day)</i>.

    <p> However, for past reference English uses the simple past form or either of two alternative
    markers: <b>used to</b> as in <i>we used to go there (every Thursday)</i>, and <b>would</b> as in
    <i>back then we would go there (every Thursday).</i>

   <p>
    <a href="https://en.wikipedia.org/wiki/African-American_Vernacular_English"  target="_top">African-American Vernacular English (<i>AAVE</i>)</a>
     uses <b>be</b> (habitual be) to indicate that  performance of the verb is of a habitual nature:
    <p>
    <i>Habitual be</i> is the use of an uninflected <i>be</i> in African-American Vernacular English (AAVE),
    Caribbean English and Certain dialects of Hiberno-English 
    (<a href="https://en.wikipedia.org/wiki/South-West_Irish_English" target="_top">South-West Irish English</a>)
    to mark habitual or extended actions,  in place of the Standard English inflected forms of be, such as 
    is and are.
     <ul>
       <li> I do be thinking about it 
       <li> she does be late
       <li> separately interesting, non-canonical constituent order: <i>Thinking to steal a few eggs I was</i>
     </ul>

    <p>
    In AAVE, use of <i>be</i> indicates that a subject repeatedly does an action or embodies a trait. In Standard English, the
    use of (an inflection of) <i>be</i> merely conveys that an individual has done an action in a
    particular tense, such as in the statement "She was singing" (the habitual being "she sings").
    <p>
    In South-Western Hiberno-English, the habitual takes a different form, with do being added to
    the sentence as a supplement. Instead of saying "She is late" or "They are always doing that,"
    "She do be late" and "They always be doing that" are used. It is descended from Irish language
    grammar and use of the verb Bí, the habitual tense of the verb "to be".
    <p>
    It is a common misconception that AAVE speakers simply replace <i>is</i> with <i>be</i> across all tenses,
    with no added meaning. In fact, AAVE speakers use <i>be</i> to mark a habitual grammatical aspect not
    explicitly distinguished in Standard English. For example, <i>to be singing</i> means to sing
    habitually, not to presently be singing. In one experiment, children were shown drawings of Elmo
    eating cookies while Cookie Monster looked on. Both black and white subjects agreed that Elmo is
    eating cookies, but the black children said that Cookie Monster be eating cookies.
    `,
    
    "ADDITIVE_vs_SUBORDINATING_STYLE":
    `
    Stanley Fish, How to Write a Sentence, and How to Read One (2011): 

     <blockquote>I want to submit to you that topic sentences and thesis statements 
     are best expressed in the subordinating style rather than in the additive style.
     </blockquote>


    This is thhe first of Walter Ong's characteristics of orally based thought
    and expression, chapter 3 of Orality and Literacy, "Some Psychodynamics of Orality",
    p.37.  He compares the creation narrative in Genesis 1:1-5,
    <h5>King James Version 1604-1611</h5>
    <ol>
      <li>In the beginning God created the heaven and the earth.
      <li>And the earth was without form, and void; and darkness was upon the face of the deep. 
          And the Spirit of God moved upon the face of the waters.
      <li>And God said, Let there be light: and there was light.
      <li>And God saw the light, that it was good: and God divided the light from the darkness.
      <li>And God called the light Day, and the darkness he called Night. 
          And the evening and the morning were the first day.
    </ol>
    <h5> New American Bible 1970</h5>
      <ol>
        <li> In the beginning, when God created the heavens and the earth,
        <li> the earth was a formless wasteland, and darkness covered the abyss, while a mighty wind swept over the waters.
        <li> Then God said, "Let there be light," and there was light.
        <li> God saw how good the light was. God then separated the light from the darkness.
        <li> God called the light "day," and the darkness he called "night." Thus evening came, and morning followed - the first day.
       </ol>
    `,
    "DERIVATIONAL_SUFFIX":
    `
    Derivation can be contrasted with inflection, in that derivation
    can produce a new word (a distinct lexeme) whereas inflection
    produces grammatical variants of the same word.

    <p>
    Ad hoc criterion: a derived word earns it's own entry in a
    dictionary, as in <i>bake</i>, <i>baker</i>, <i>bakery</i>
    vs. <i>bake</i>, <i>baked</i>, <i>baking</i>.

    <p> Inflection applies in more or less regular patterns to all
    members of a part of speech (for example, nearly every English
    verb adds <i>-s</i> for the third person singular present tense),
    while derivation follows less consistent patterns (for example,
    the nominalizing suffix <i>-ity</i> can be used with the
    adjectives <i>modern</i> and <i>dense</i>, but not with open or
    strong). However, it is important to note that derivations and
    inflections can share homonyms, that being, morphemes that have
    the same sound, but not the same meaning. For example, when the
    affix <i>-er</i>, is added to an adjective, as in <i>small-er</i>,
    it acts as an inflection, but when added to a verb, as in
    <i>cook-er</i>, it acts as a derivation.

    <p>
    As mentioned above, a derivation can produce a new word (or new
    part of speech) but is not required to do so. For example, the
    derivation of the word "common" to "uncommon" is a derivational
    morpheme but doesn't change the part of speech (adjective).

    <p> An important distinction between derivational and inflectional
    morphology lies in the content/function of a listeme. Derivational
    morphology changes both the meaning and the content of a listeme,
    while inflectional morphology doesn't change the meaning, but
    changes the function.

    <p>A listeme is a word or phrase (or, according to Steven Pinker,
    "a stretch of sound") that must be memorized because its sound or
    meaning does not conform to some general rule. Also called a
    lexical item. All word roots, irregular forms, and idioms are
    listemes.

    <p>
    A non-exhaustive list of derivational morphemes in English: 
     <ul>
      <li>-ful
      <li>-able
      <li>im-
      <li>un-
      <li>-ing
      <li>-er
     </ul>

    <p>
    A non-exhaustive list of inflectional morphemes in English: 
     <ul>
        <li>-er
        <li>-est
        <li>-ing
        <li>-en
        <li>-ed
        <li>-s
    </ul>
    `,
    
  //------------------------
    "INCH":
    `
    inchoative: or inceptive, indicates a process of beginning or
    becoming.  <p>Most of the Interior Salish languages have an
    important affix which has been called INCHOATIVE. Semantically it
    covers both simple mutative ideas—i.e., shift to a new state of
    affairs—and more specialized notions emphasizing the beginning of
    an action or state or the emergence of a concept.

    <p>Inchoative aspect is a grammatical aspect, referring to the
    beginning of a state. It can be found in conservative
    Indo-European languages such as Latin and Lithuanian, and also in
    Finnic languages or European derived languages with high
    percentage of Latin-based words like Esperanto. It should not be
    confused with the prospective, which denotes actions that are
    about to start. The English language can approximate the
    inchoative aspect through the verbs "to become" or "to get"
    combined with an adjective.

    <p>Inchoative is a term used for verbs whose meanings can be
    paraphrased as '<i>to begin to...</i>' (e.g. inflame and depopulate) or
    verbs which express the beginning of a state or process, like
    <i>harden</i> (become hard), <i>die</i> (become dead) or break. The term is also
    used in explicating the ambiguity of <i>John will eat his lunch in an
    hour</i>: the inchoative reading is the one in which it will take an
    hour before John is to eat his lunch.
    `,
    
    "adjunct":
    `
     An optional, or structurally dispensable part of a sentence, clause, or phrase that, 
     if removed or discarded, will not structurally affect the remainder of the sentence. 
     <p>In the sentence <i>John helped Bill in Central Park</i>, the phrase 
     <i>in Central Park</i> is an adjunct.
     <p>
     An adjunct can be a single word, a phrase, or an entire clause:
     <ul>
       <li> She will leave <i>tomorrow.</i>
       <li> She will leave <i>in the morning.</i>
       <li> She will leave <i>after she has had breakfast.</i>
     </ul>
    `,
  //------------------------
    "reduplication":
    `an account of the varieties of reduplication will appear here.`
     ,

    "TAM":

`Tense-aspect-mood: a group of grammatical categories which are important for the understanding of
spoken or written content and which are marked in different ways by different languages.
   
<ul>
   <li> Tense: location of state or action in time, past, present or future.
   <li> Aspect: extension time, whether it is unitary (perfective), continuous or repeated (imperfective).
   <li> <a href="#Mood">Mood</a> its reality: actual (realis), a possibility,  or a necessity (irrealis).
   <li> From Medieval Latin irrealis, from in- (“not”) + realis (“actual; existing”)
</ul>

<h4 id="Mood">Mood</h4> <h5>Subjunctive</h5> 

The subjunctive indicates the speaker's attitude toward the <i>irrealis</i> state or
action's existance: imagined? wished for?  possible?  not yet occurred?

<p>
The irrealis subjunctive contrasts with the realis moods, whose most common form is the
 <i>indicative</i>, indicating actual or high probability events or states.

<p> Other realis moods: evidential, mirative (surprise).
<p
Subjunctive forms of verbs are typically
used to express various states of <i>unreality</i> such as: wish,
emotion, possibility, judgment, opinion, obligation, or action that
has not yet occurred; the precise situations in which they are used
vary from language to language. The subjunctive is one of the
<i>irrealis</i> moods, which refer to what is not necessarily real. It
is often contrasted with the <i>indicative</i>, a realis mood which is
used principally to indicate that something is a statement of fact.
</p>

<p>

In a sentence, the grammatical mood conveys the speaker’s attitude
about the state of being of what the sentence describes. This may
sound a little complicated, but it’s simple enough: In the indicative
mood, for instance, the speaker is sure that something is the case,
while in the imperative mood the speaker desires that something should
happen.

<p><p>

In English, the subjunctive mood is used to explore conditional or
imaginary situations. It can be tricky to use, which partially
explains why many speakers and writers forgo it.

`,

    "aspect": "how an action, event, or state, denoted by a verb, extends over time",
    "mood":   "express their attitude toward what they are saying (for example, a statement of fact, of desire, of command, etc.)",

    "clitic": `A clitic is a morpheme that has syntactic
               characteristics of a word, but depends phonologically
               on another word or phrase. In this sense, it is
               syntactically independent but phonologically
               dependent—always attached to a host. A clitic is
               pronounced like an affix, but plays a syntactic role at
               the phrase level. In other words, clitics have the form
               of affixes, but the distribution of function words. For
               example, the contracted forms of the auxiliary verbs in
               I'm and we've are clitics.
               <h5>Summary</h5>

               Clitics can be defined as <i>prosodically defective
               function words</i>. They can belong to a number of
               syntactic categories, such as articles, pronouns,
               prepositions, complementizers, negative adverbs, or
               auxiliaries. They do not generally belong to open
               classes, like verbs, nouns, or adjectives. Their
               prosodically defective character is most often
               manifested by the absence of stress, which in turn
               correlates with vowel reduction in those languages that
               have it independently; sometimes the clitic can be just
               a consonant or a consonant cluster, with no vowel. This
               same prosodically defective character forces them to
               attach either to the word that follows them (proclisis)
               or to the word that precedes them (enclisis); in some
               cases they even appear inside a word (mesoclisis or
               endoclisis). The word to which a clitic attaches is
               called the host. In some languages (like some dialects
               of Italian or Catalan) enclitics can surface as
               stressed, but the presence of stress can be argued to
               be the result of assignment of stress to the
               host-clitic complex, not to the clitic itself. One
               consequence of clitics being prosodically defective is
               that they cannot be the sole element of an utterance,
               for instance as an answer to some question; they need
               to always appear with a host.
     
                <p><p>

               A useful distinction is that between simple clitics and
               special clitics. Simple clitics often have a nonclitic
               variant and appear in the expected syntactic position
               for nonclitics of their syntactic category. Much more
               attention has been paid in the literature to special
               clitics. Special clitics appear in a designated
               position within the clause or within the noun phrase
               (or determiner phrase). In several languages certain
               clitics must appear in second position, within the
               clause, as in most South Slavic languages, or within
               the noun phrase, as in Kwakw'ala. The pronominal
               clitics of Romance languages or Greek must have the
               verb as a host and appear in a position different from
               the full noun phrase. A much debated question is
               whether the position of special clitics is the result
               of syntactic movement, or whether other factors,
               morphological or phonological, intervene as well or are
               the sole motivation for their position. Clitics can
               also cluster, with some languages allowing only
               sequences of two clitics, and other languages allowing
               longer sequences. Here one relevant question is what
               determines the order of the clitics, with the main
               avenues of analysis being approaches based on syntactic
               movement, approaches based on the types of
               morphosyntactic features each clitic has, and
               approaches based on templates. An additional issue
               concerning clitic clusters is the incompatibility
               between specific clitics when combined and the changes
               that this incompatibility can provoke in the form of
               one or more of the clitics. Combinations of identical
               or nearly identical clitics are often disallowed, and
               the constraint known as the Person-Case Constraint
               (PCC) disallows combinations of clitics with a first or
               second person accusative clitic (a direct object, DO,
               clitic) and a third person (and sometimes also first or
               second person) dative clitic (an indirect object, IO,
               clitic). In all these cases either one of the clitics
               surfaces with the form of another clitic or one of the
               clitics does not surface; sometimes there is no
               possible output. Here again both syntactic and
               morphological approaches have been proposed.
`
};
