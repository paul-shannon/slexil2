var DELAY = 750;
var converter = new showdown.Converter()
converter.setOption("simpleLineBreaks", true)
var clickState = {};
var usePopIns = true
var timeoutHandle;
function anyElementClicked(){return(!Object.keys(clickState).every((k) => !clickState[k]))};

$(function() {
    $('body').prepend('<div id="popinControlsDiv">Annotation pop-ins? </div>')
    $('#popinControlsDiv').append('<input id="radio-popin-off" type="radio" name="popins" value="off"> off</input></div>');
    $('#popinControlsDiv').append('<input id="radio-popin-on"  type="radio" name="popins" value="on" checked> on</input></div>');
    $("#radio-popin-off").click(function(){
        usePopIns = false;
        console.log("off clicked, usePopIns is now " + usePopIns)
       })
    $("#radio-popin-on").click(function(){
        usePopIns = true;
        console.log(" on clicked, usePopIns is now " + usePopIns)
       })
    //$('input[name=popins]').click(function(){
    //    usePopIns = $('input[name=popins]:checked').val() == "on";
    //    console.log("usePopIns: " + usePopIns);
    //    }); 
    
    $(".annotationDiv").hide()
    $(".morpheme-cell, .speech-tier, .freeTranslation-tier")
        .mousedown(function(){
           var key = this.innerHTML
           var someOtherElementIsDisplayed = anyElementClicked() && !clickState[key];
           if(someOtherElementIsDisplayed) return;
           if(Object.keys(clickState).indexOf(key) < 0){
              clickState[key] = true;
              }
            else{
              console.log("inverting clickState")
              clickState[key] = !clickState[key]
              }
            console.log("clickState: " + clickState[key]);
            if(clickState[key]){
              $(this).css('background-color', "lightgray");
              $(this).css('border',  "1px solid red");
              }
            else{
              var infoBox; 
              infoBox = $(this).parent().siblings(".annotationDiv");
              if(infoBox.length == 0){ // crude hack to get translation tier access to the infobox
                 infoBox = $(this).siblings(".annotationDiv");
                 }
              infoBox.hide()
              $(this).css('background-color', "white");
              $(this).css('border',  "0px solid red");
              }
           console.log("click");
           console.log(key);
           })
        .mouseenter(function(){
           var thisElement = this;
           if(!usePopIns) return;
           timeoutHandle = window.setTimeout(function() {
             if(!anyElementClicked()){
		 var key = thisElement.innerHTML
                 // use this minimal event to initialize clickState
		 if(Object.keys(clickState).indexOf(key) < 0){
                     clickState[key] = false;
                 }
		 var moreInformation = lookup(thisElement.innerHTML)
                 console.log("moreInformation? " + moreInformation.length);
                 console.log(moreInformation);
		 window.x = moreInformation;
		 var lineCount = moreInformation.split(/\r\n|\r|\n/).length;
                 var infoBox;
		 infoBox = $(thisElement).parent().siblings(".annotationDiv");
                 if(infoBox.length == 0){ // crude hack to get translation tier access to the infobox
                    infoBox = $(thisElement).siblings(".annotationDiv");
                    }
                 console.log("-- infoBox.length: " + infoBox.length);
		 $(thisElement).css('background-color', "lightgray");
		 infoBox.hide()
		 if(moreInformation.length > 0){    
                     var boxHeight = (lineCount * 30) + 50
                     infoBox.css('height', boxHeight);
                     console.log("about to show infoBox: " + boxHeight)
                     infoBox.show();
                     infoBox.html(moreInformation)
                     //infoBox.html(lookup(thisElement.innerHTML));
                     infoBox.focus();
                    }
                } // !anyElementClicked
              }, DELAY) // setTimeout
           }) // mouseEnter
        .mouseleave(function(){
           if(timeoutHandle != null){
             clearTimeout(timeoutHandle); 
             timeoutHandle = null;
             }
           if(!usePopIns) return;
           if(!anyElementClicked()){
               var key = this.innerHTML
               if(!clickState[key]){
                   $(this).css('background-color', "white");
                   var infoBox = $(this).parent().siblings(".annotationDiv");
                   infoBox.hide()
               }
           } // !anyElementClicked
        }) // mouseleave
}); // on ready

//------------------------------------------------------------------------------------------------------------------------
function lookup(morpheme)
{
   var found = Object.keys(kb).indexOf(morpheme) >= 0;
   console.log("---- lookup, using kb: '" + morpheme + "', found? " + found)
    
   if(Object.keys(kb).indexOf(morpheme) < 0)
       return("")

    var markup = converter.makeHtml(kb[morpheme]);
    return(markup);

}
//------------------------------------------------------------------------------------------------------------------------
function ref(key)
{
  console.log("--- entering pshannon.js ref function, with key " + key);
  $("#refPopupTitle").html(key)
  lookupReference(key);
   $("#refPopup").toggle();
};
function lookupReference(key){
   $("#refText").html(linguisticTerms[key]);
    };
//------------------------------------------------------------------------------------------------------------------------


