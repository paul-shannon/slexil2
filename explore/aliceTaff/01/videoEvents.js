<script>
    
console.log("--- executing videoEvents.js");

vp = $("#videoPlayer");

vp.on("timeupdate", function(e){
   tCurrent = Math.round(vp.get(0).currentTime * 1000)
   //console.log("timeupdate");
   for(lineTimes of timeStamps){
       if(lineTimes.start <= tCurrent && lineTimes.end >= tCurrent){
           //console.log("playing line " + lineTimes.id);
           var lineNumber = parseInt(lineTimes.id)
           scrollAndHighlight(lineNumber)
          }
      } // for lineTimes
   })

//--------------------------------------------------------------------------------
function scrollAndHighlight(lineNumber){

   //var newTop = Math.round($('#' + lineNumber).position().top) - 100;
   //var options = {top: newTop, left: 0, behavior: "smooth"}
   //$(".line-wrapper").removeClass("current-line")
   //$('#' + lineNumber).addClass("current-line")

   // from here:
   // https://stackoverflow.com/questions/27980084/scrolling-to-a-element-inside-a-scrollable-div-with-pure-javascript
   var scrollingDivTop = document.getElementById("textDiv").offsetTop
   //console.log("texDiv top: " + scrollingDivTop);

   var lineDivTop = document.getElementById(lineNumber).offsetTop - scrollingDivTop;
   lineDivTop -= 100;
   //console.log("line top for " + lineNumber + ": " + lineDivTop);

   var options = {top: lineDivTop, left: 0, behavior: "smooth"}
   document.getElementById("textDiv").scrollTo(options)

   $(".line-wrapper").removeClass("current-line")
   $('#' + lineNumber).addClass("current-line")

}  // scrollAndHighlight
//--------------------------------------------------------------------------------
</script>
