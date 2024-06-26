console.log("--- executing mediaPlayerEvents.js");

var mediaPlayer = document.getElementById("mediaPlayer");
var mediaSegmentEnd;
var mediaContinuousPlay = true;
//--------------------------------------------------------------------------------
mediaPlayer.addEventListener("timeupdate", function (){

   tCurrent = Math.round(mediaPlayer.currentTime * 1000)
   //console.log("timeupdate " + tCurrent + " continuous? " + mediaContinuousPlay)
   for(lineTimes of timeStamps){
      if(lineTimes.start <= tCurrent && lineTimes.end >= tCurrent){
         var lineNumber = parseInt(lineTimes.id)
         scrollAndHighlight(lineNumber)
         }
      } // for lineTimes

   if (!mediaContinuousPlay && mediaSegmentEnd && mediaPlayer.currentTime >= mediaSegmentEnd){
      mediaPlayer.pause();
      mediaContinuousPlay=true;
      }   

})  // addEventListener timeupdate
//--------------------------------------------------------------------------------
function scrollAndHighlight(lineNumber){

   // from here:
   // https://stackoverflow.com/questions/27980084/scrolling-to-a-element-inside-a-scrollable-div-with-pure-javascript
   var scrollingDivTop = document.getElementById("textDiv").offsetTop

   var lineDivTop = document.getElementById(lineNumber).offsetTop - scrollingDivTop;
   lineDivTop -= 100;

   var options = {top: lineDivTop, left: 0, behavior: "smooth"}
   document.getElementById("textDiv").scrollTo(options)

   $(".line-wrapper").removeClass("current-line")
   $('#' + lineNumber).addClass("current-line")

}  // scrollAndHighlight
//--------------------------------------------------------------------------------
function playSample(mediaID, startTime, endTime)
{
    console.log("medium-agnostic playSample: " + mediaID + ", " +
		startTime + ", " + endTime)
    playMediaSegment(mediaID, startTime, endTime)

} // playSample
//--------------------------------------------------------------------------------
function playMediaSegment(mediaID, startTime, endTime)
{
    mediaContinuousPlay = false;
    startTime = startTime/1000;

      // subtract half a second so playback does not run over
      // this is dodgy, works only if the supplied intervals (stop and
      // start times) have the expected padding.  which are the elan 
      // user's choices
    endTime = (endTime/1000) - 0.3  
				    
    console.log("medium-agnostic playMediaSegment: " + mediaID + ", " +
				startTime + ", " + endTime)

    mediaSegmentEnd = endTime;
    mediaPlayer.currentTime = startTime
    //debugger;
    mediaPlayer.play();

} // playMediaSegment
//--------------------------------------------------------------------------------
