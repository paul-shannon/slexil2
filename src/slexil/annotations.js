var annoState = {
  annotationDivVisble: false,
  }

var showAnno = false;
converter = new showdown.Converter()
converter.setOption("tables", true);

var timer = null;

$(function() {
   console.log("--- executing src/slexil/annotations.js")
   if (typeof(kb) == 'object'){
      console.log("--- kb entries: " + Object.keys(kb).length);
      if(typeof(linguistics) == 'object'){
         console.log("--- adding linguistic term entries: " + Object.keys(linguistics).length);
         kb = {...kb, ...linguistics};
         }
       console.log("kb entries: " + Object.keys(kb).length)
       } // if at least kb dictionary is defined


    //$(".morpheme-cell, .speech-tier, .freeTranslation-tier, .grammatical-term")
    //$(".morpheme-cell", ".grammatical-term", ".speech-tier",
    //   ".freeTranslation-tier")
    $(".morpheme-cell, .grammatical-term, .speech-tier").mouseenter(function(){
        if(annoState.annotationDivVisible){
           var currentElement = $(this);
           console.log("--- mouseenter " + currentElement.html());
           var key = currentElement.html();
           console.log("speech & translation tier, kb key lookup: " + key);
           if(lookup(key).length > 0)
              currentElement.addClass("has-annotation")
           } //  if annotationDivVisible
        }) // mouseenter
      .mouseleave(function(){
         if(annoState.annotationDivVisible){
            var currentElement = $(this);
            currentElement.removeClass("has-annotation")
            }
         }) // mouseleave

    $(".morpheme-cell, .grammatical-term, .speech-tier").on('click', function(e){
        console.log("morpheme-cell, grammatical-term, speech-tier click!")
        if(annoState.annotationDivVisible){
           var currentElement = $(this);
           const key = currentElement.text().trim()
           console.log("--- currentElement text:")
           console.log(key)
           currentElement.addClass("focusedGrammaticalElement")
           console.log("morpheme and term, click kb key lookup: '" + key + "'");
           displayAnnotationByString(key)
           }
        }) // on click

  $("#toggleAnnotationsButton").click(function(){
     var annoDivVisible = $("#annoDiv").is(":visible")
     var currentPosition = $("#textDiv").scrollTop();
     console.log("click simple anno toggle, annoDivVisible? " + annoDivVisible +
                "  pos: " + currentPosition)
     if (annoDivVisible){
        console.log("hiding annoDiv");
        showAnno = false;
        $("#annoDiv").removeClass("col-4").hide()
        $("#textLeftColumn").removeClass("col-7").addClass("col-12")
        $("#toggleAnnotationsButton").text("Show Annotations")
        $("#linguisticTopicController").css("display", "none")
        annoState.annotationDivVisible = false;
     } else {
        console.log("showing annoDiv");
        $("#annoDiv").addClass("col-4").show()
        $("#textLeftColumn").removeClass("col-12").addClass("col-8")
        $("#toggleAnnotationsButton").text("Hide Annotations")
        $("#linguisticTopicController").css("display", "inline-block")
        showAnno = true;
        annoState.annotationDivVisible = true;
        }
     console.log("  --- toggle complete, setting position: " + currentPosition)
     $("#textDiv").scrollTop(currentPosition);
     console.log("     position check after set: " + $("#textDiv").scrollTop())

     }); // toggleAnnotationsButton click

    const pshannonSig = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/1'
    //console.log("pshannonSig: " + pshannonSig)
    //console.log("userAgent:   " + navigator.userAgent)
    //console.log("kb defined? " + typeof(kb) == 'object')
    if((navigator.userAgent).startsWith(pshannonSig) & (typeof(kb) == 'object')){
       showAnno = true;
       $("#annoDiv").show()
       annoState.annotationDivVisible = true;                
       $("#toggleAnnotationsButton").text("Hide Annotations")
       // $("#otherControlsDiv").show()
       }
    }); // on ready

//------------------------------------------------------------------------------------------------------------------------
function displayAnnotationByString(topic)
{
  var annoBox = $("#annoNotesDiv");
  var annoText = lookup(topic)
  console.log("--- displayAnnotation, annoText: '" + annoText + "'");
  console.log("     length: " + annoText.length);
  annoBox.html(annoText);

} // displayAnnotationByString
//------------------------------------------------------------------------------------------------------------------------
function lookup(key)
{
   if(typeof kb == 'undefined'){
      return("")
      }

   var index = Object.keys(kb).indexOf(key);
   var found = index >= 0
   console.log("---- annotations.js, lookup, using kb: '" + key + "', found? " + found)
   console.log("    index: " + index);

   if(index < 0)
      return("")
      //return("no annotation available")

   var markup = converter.makeHtml(kb[key]);
   return(markup);

} // lookup
//------------------------------------------------------------------------------------------------------------------------


