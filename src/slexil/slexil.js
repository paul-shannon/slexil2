var mediaPlayer = document.getElementById("mediaPlayer");
var mediaSegmentEnd;
var mediaContinuousPlay = true;
//--------------------------------------------------------------------------------
mediaPlayer.addEventListener("timeupdate", function (){

   tCurrent = Math.round(mediaPlayer.currentTime * 1000)
   verbose = true;
   if(verbose){
       console.log("--- timeupdate " + tCurrent + " continuous? " + mediaContinuousPlay)
       console.log("    raw: " + mediaPlayer.currentTime)
       }

   for(lineTimes of timeStamps){
      if(lineTimes.start <= tCurrent && lineTimes.end >= tCurrent){
         var lineNumber = parseInt(lineTimes.id)
         if(verbose){
            console.log("   line " + lineNumber + "  start: " + lineTimes.start.toFixed(2) +
                        "  lineTimes.end: " + lineTimes.end.toFixed(2));
            }
         scrollAndHighlight(lineNumber)
         break;
         }
      } // for lineTimes

   if (!mediaContinuousPlay && mediaSegmentEnd && mediaPlayer.currentTime >= mediaSegmentEnd){
      if(verbose){
         console.log("--- stopping play, because currentTime (" + mediaPlayer.currentTime.toFixed(2) +
                      ") is >= mediaSegmentEnd (" + mediaSegmentEnd.toFixed(2) + ")");
         }
      mediaPlayer.pause();
      mediaContinuousPlay=true;
      }   

})  // addEventListener timeupdate
//--------------------------------------------------------------------------------
function scrollAndHighlight(lineNumber){

   // from here:
   // https://stackoverflow.com/questions/27980084/scrolling-to-a-element-inside-a-scrollable-div-with-pure-javascript
   var scrollingDivTop = document.getElementById("textDiv").offsetTop

   //console.log("--- scrollAndHighlight to line " + lineNumber);
   var lineDivTop = document.getElementById(lineNumber).offsetTop - scrollingDivTop;
   lineDivTop -= 100;

   var options = {top: lineDivTop, left: 0, behavior: "smooth"}
   document.getElementById("textDiv").scrollTo(options)

   //$(".line-wrapper").removeClass("current-line")
   $(".line-content > .line").removeClass("current-line")
   //qt = "#" + lineNumber + " .line-content"
   qt = "#" + lineNumber + " .line"
   $(qt).addClass("current-line")
   //$('#' + lineNumber).addClass("current-line")

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
$('#fontSizeSlider').on('input', function() {
    var v = $(this).val();
    console.log(v)
    $("#textDiv").css('font-size', (v * 22) + 'px')
    $("#annoDiv").css('font-size', (v * 22) + 'px')
    });

$('#videoSizeSelector').on('input', function() {
    var v = $(this).val();
    console.log(v);
    $("#mediaPlayer").width(v);
    });

$('#speedSelector').on('input', function() {
    var v = $(this).val();
    console.log(v)
    mediaPlayer.playbackRate = v;
	$("#playbackSpeedReadout").text(v);
    });



