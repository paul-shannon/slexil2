var DELAY = 750;
var converter = new showdown.Converter()
converter.setOption("simpleLineBreaks", true)
var clickState = {};
var usePopIns = true
var timeoutHandle;
function anyElementClicked(){return(!Object.keys(clickState).every((k) => !clickState[k]))};

$(function() {
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
           $(this).css('background-color', "lightgray");
           var key = thisElement.innerHTML
           console.log("mouseenter: " + key)
           var annoBox = $("#kbDiv");
           annoBox.html(lookup(key));
           }) // mouseEnter
        .mouseleave(function(){
           $(this).css('background-color', "white");
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


