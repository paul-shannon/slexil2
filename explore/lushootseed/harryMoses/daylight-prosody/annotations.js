var showAnno = false;
converter = new showdown.Converter()

$(function() {
    $(".morpheme-cell, .speech-tier, .freeTranslation-tier")
        .mouseenter(function(){
            if(showAnno){
               $(this).addClass("focusedGrammaticalElement")
               var key = this.innerHTML
               var annoBox = $("#annoDiv");
               var annoText = lookup(key)
               annoBox.html(annoText);
               }
            })
        .mouseleave(function(){
            $(this).removeClass("focusedGrammaticalElement")
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
    	  $("#linguisticTopicController").css("display", "none")
	  } else {
		  console.log("showing annoDiv");
		  $("#annoDiv").addClass("col-4").show()
		  $("#textLeftColumn").removeClass("col-12").addClass("col-8")
		  $("#toggleAnnotationsButton").text("Hide Annotations")
    	  $("#linguisticTopicController").css("display", "inline-block")
		  showAnno = true;
	     }
     }); // toggleAnnotationsButton click

	 $("#languageTopicsSelector").on("change", function(){
		  var key = this.value;
		  if(key != "Linguistic Topic?"){ // the title
			  var annoBox = $("#annoDiv");
			  var annoText = lookup(key)
			  annoBox.html(annoText);
           }
           // show the blank (first) option in the selector
		  $("#languageTopicsSelector option")[0].selected = true;
      }); // languageTopicsSelector change
        

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


