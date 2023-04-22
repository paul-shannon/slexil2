var showAnno = false;
converter = new showdown.Converter()

$(function() {
    $(".morpheme-cell, .speech-tier, .freeTranslation-tier")
        .mouseenter(function(){
            if(showAnno){
               var thisElement = this;
               var key = thisElement.innerHTML
               var annoBox = $("#annoDiv");
               console.log("--- looking up " + key);
               var annoText = lookup(key)
               //console.log(annoText)
               annoBox.html(annoText);
               }
            })
        .mouseleave(function(){
            var infoBox = $(this).parent().siblings(".morphemeInfo");
            infoBox.hide()
            })

  $("#toggleAnnotationsButton").click(function(){
	  var annoDivVisible = $("#annoDiv").is(":visible")
	  //console.log("click simple anno toggle, annoDivVisible?" + annoDivVisible)
	  if (annoDivVisible){
		  console.log("hiding annoDiv");
		  showAnno = false;
		  $("#annoDiv").removeClass("col-4").hide()
		  $("#textLeftColumn").removeClass("col-7").addClass("col-12")
		  $("#toggleAnnotationsButton").text("Show Annotations")
	  } else {
		  console.log("showing annoDiv");
		  $("#annoDiv").addClass("col-4").show()
		  $("#textLeftColumn").removeClass("col-12").addClass("col-8")
		  $("#toggleAnnotationsButton").text("Hide Annotations")
		  showAnno = true;
	     }
     }); // toggleAnnotationsButton click


    }); // on ready

//------------------------------------------------------------------------------------------------------------------------
function lookup(morpheme)
{
   var index = Object.keys(kb).indexOf(morpheme);
   var found = index >= 0
   console.log("---- lookup, using kb: '" + morpheme + "', found? " + found)
   console.log("    index: " + index);

   if(index < 0)
       return("")

    var markup = converter.makeHtml(kb[morpheme]);
    return(markup);

} // lookup
//------------------------------------------------------------------------------------------------------------------------


