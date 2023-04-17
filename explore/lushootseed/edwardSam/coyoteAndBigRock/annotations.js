$(function() {
    $(".morpheme-cell, .speech-tier, .freeTranslation-tier")
        .mouseenter(function(){
            if(showAnno){
               var thisElement = this;
               var key = thisElement.innerHTML)
               var annoBox = $("#kbDiv");
               annoBox.html(key);
               }
            })
        .mouseleave(function(){
            var infoBox = $(this).parent().siblings(".morphemeInfo");
            infoBox.hide()
            })
    }); // on ready

//------------------------------------------------------------------------------------------------------------------------
kb = {

   "tu=t’əd•al•gʷiɬ":
        [
        ], 

   "gʷәl":
        ["<b>gʷәl</b>: &nbsp; and, but, or, then, next, as if, because.",
         "<br>",
         "Sentential adverb, conjunction; used especially to introduce sentences in long narratives.",
         "<br>",
         "Can also mark topicalization, in effect treating the topic as an entire clause and using gʷәl", 
         "<br>",
         "to introduce the following clause."],

    "tux̌ʷ": ["<b>tux̌ʷ</b>: &nbsp; merely, just (in contrast to the usual or expected), simply, contrary to expectation; instead, conversely, but.", 
             "<br>",
             "The distribution and significance of tux̌ʷ give it sometimes the characteristics of a sentential adverb",
             "<br>",
             "and sometimes the attributes of a sentential adverb.",
             "<br>",
             "In the latter capacity, note how it often enters into construction with gʷәl and huy:",
             "<br>",
             "'gʷәl tux̌ʷ': but, and yet, as, while, and as, and while.",
             "<br>",
             "'tux̌ʷ huy': but then instead.  'gʷәl tux̌ʷ huy' also occurs." 
             ]
     };

//------------------------------------------------------------------------------------------------------------------------
function lookup(morpheme)
{
   var found = Object.keys(kb).indexOf(morpheme) >= 0;
   console.log("---- lookup, using kb: '" + morpheme + "', found? " + found)
    
   if(Object.keys(kb).indexOf(morpheme) < 0)
       return("")

    var markup = converter.makeHtml(kb[morpheme]);
    return(markup);

} // lookup
//------------------------------------------------------------------------------------------------------------------------

function old_lookup(morpheme)
{
   console.log("---- lookup: " + morpheme)

   if(Object.keys(kb).indexOf(morpheme) < 0)
       return(morpheme)

    return(kb[morpheme]);

}
//------------------------------------------------------------------------------------------------------------------------


