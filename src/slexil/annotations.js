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
    $(".speech-tier, .freeTranslation-tier")
        .mouseenter(function(){
            var currentElement = $(this);
            //console.log("--- mouseenter " + currentElement.html());
            if(showAnno){
                if(timer != null){clearTimeout(timer);}
                timer = setTimeout(function(){
                   //console.log("mouseenter delay");
                   currentElement.addClass("focusedGrammaticalElement")
                   var key = currentElement.html();
                   var annoBox = $("#annoNotesDiv");
                   console.log("speech & translation tier, kb key lookup: " + key);
                   var annoText = lookup(key)
                   console.log("chars retrieved: " + annoText.length);
                   annoBox.html(annoText);
                   }, 1000) // setTimeout function
                } // if showAnno
            }) // mouseenter
        .mouseleave(function(){
            var currentElement = $(this);
            if(timer != null){clearTimeout(timer);}
            timer = null;
            currentElement.removeClass("focusedGrammaticalElement")
            //var infoBox = $(this).parent().siblings(".morphemeInfo");
            //infoBox.hide()
            }) // mouseleave

    $(".morpheme-cell, .grammatical-term, .storyLaunch").on('click', function(e){
        //.click(function(e){
            console.log("morpheme-cell, grammatical-term click!")
            var currentElement = $(this);
            const key = currentElement.text().trim()
            console.log("--- currentElement text:")
            console.log(key)
            currentElement.addClass("focusedGrammaticalElement")
            console.log("morpheme and term, click kb key lookup: '" + key + "'");
            var annoBox = $("#annoNotesDiv");
            var annoText = lookup(key)
            console.log("chars retrieved: " + annoText.length);
            if(annoText.length == 0){
               annoText = "no annotation found"
               }
            if(annoText.length > 0){
              annoBox.html(annoText);
              }
            //e.preventDefault()
            //e.stopPropagation()
            })

  $("#toggleAnnotationsButton").click(function(){
     var annoDivVisible = $("#annoNotesDiv").is(":visible")
     var currentPosition = $("#textDiv").scrollTop();
     console.log("click simple anno toggle, annoDivVisible? " + annoDivVisible +
                "  pos: " + currentPosition)
     console.log
     if (annoDivVisible){
        console.log("hiding annoDiv");
        showAnno = false;
        $("#annoDiv").removeClass("col-4").hide()
        $("#textLeftColumn").removeClass("col-7").addClass("col-12")
        $("#toggleAnnotationsButton").text("Show Annotations")
        $("#linguisticTopicController").css("display", "none")
     } else {
        console.log("showing annoDiv");
        $("#annoDiv").addClass("col-4").show()
        $("#textLeftColumn").removeClass("col-12").addClass("col-8")
        $("#toggleAnnotationsButton").text("Hide Annotations")
        $("#linguisticTopicController").css("display", "inline-block")
        showAnno = true;
        }
     console.log("  --- toggle complete, setting position: " + currentPosition)
     $("#textDiv").scrollTop(currentPosition);
     console.log("     position check after set: " + $("#textDiv").scrollTop())

     }); // toggleAnnotationsButton click
    pshannonSig = '"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/14'  //0.0.0.0 Safari/537.36"'
                  // Version 141.0.7390.108 (Official Build) (arm64)
    console.log("kb defined? " + typeof(kb) == 'object')
    if((JSON.stringify(navigator.userAgent).startsWith(pshannonSig)) & (typeof(kb) == 'object')){
       showAnno = true;
       $("#annoDiv").show()
       $("#toggleAnnotationsButton").text("Hide Annotations")
       // $("#otherControlsDiv").show()
       }
    }); // on ready

//------------------------------------------------------------------------------------------------------------------------
function displayAnnotation(topic)
{
  var annoBox = $("#annoDiv");
  var annoText = lookup(topic)
  annoBox.html(text);
   
} 
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
       return("no annotation available")

   var markup = converter.makeHtml(kb[key]);
   return(markup);

} // lookup
//------------------------------------------------------------------------------------------------------------------------


