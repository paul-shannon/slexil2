var mediaPlayer = document.getElementById("mediaPlayer");
var mediaSegmentEnd;
var mediaContinuousPlay = true;
var autoPlay = true;
var lastTimeUpdate = 0;
//--------------------------------------------------------------------------------
mediaPlayer.addEventListener("play", function (){
	console.log("--- play event, autoPlay? " + autoPlay);
    if(!autoPlay){
	   lastTimeUpdate = 0;  // reset this, so that continuous play is possible
	   }
    })

mediaPlayer.addEventListener("timeupdate", function (){

   tCurrent = Math.round(mediaPlayer.currentTime * 1000)
   precision = 2;
   console.log("timeupdate " + tCurrent + " autoPlay? " + autoPlay)
   var lastTime = parseFloat(lastTimeUpdate.toFixed(precision));
   var currentTime = parseFloat(mediaPlayer.currentTime.toFixed(precision));
   console.log("--- lastTime:    " + lastTime);
   console.log("--- currentTime:  " + currentTime);
   var delta = currentTime - lastTime;
   if(lastTime > 0 && (delta < 0.02)){
      console.log("--- redundant timeupdate");
      mediaPlayer.pause();
      return
	  }
   else{
     lastTimeUpdate = parseFloat(mediaPlayer.currentTime)
	 }

   if (!autoPlay && mediaSegmentEnd && mediaPlayer.currentTime >= mediaSegmentEnd){
      mediaPlayer.pause();
      autoPlay = true;     // restore the default
      console.log("--- resetting autoPlay = true");
      return;
      }   

   if(autoPlay){
      for(lineTimes of timeStamps){
         if(lineTimes.start <= tCurrent && lineTimes.end >= tCurrent){
            var lineNumber = parseInt(lineTimes.id)
            console.log("matching lineNumber: " + lineNumber)
            scrollAndHighlight(lineNumber)
            break;
            }
         } // for lineTimes
	 } // if autoPlay

   //if (!mediaContinuousPlay && mediaSegmentEnd && mediaPlayer.currentTime >= mediaSegmentEnd){
   //   mediaPlayer.pause();
   //   mediaContinuousPlay=true;
   //   }   

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

   //$(".line-wrapper").removeClass("current-line")
   $(".line-content > .line").removeClass("current-line")
   //qt = "#" + lineNumber + " .line-content"
   qt = "#" + lineNumber + " .line"
   $(qt).addClass("current-line")
   //$('#' + lineNumber).addClass("current-line")

}  // scrollAndHighlight
//--------------------------------------------------------------------------------
function playSample(lineNumber, startTime, endTime)
{
    console.log("button press: " + lineNumber + ", " + startTime + ", " + endTime)
    lastTimeUpdate = (startTime/1000) * 0.95;
    autoPlay = false;
    scrollAndHighlight(lineNumber)
    playMediaSegment(lineNumber, startTime, endTime)

} // playSample
//--------------------------------------------------------------------------------
function playMediaSegment(lineNumber, startTime, endTime)
{
    mediaContinuousPlay = false;
    autoPlay = false
    startTime = startTime/1000;

      // subtract half a second so playback does not run over
      // this is dodgy, works only if the supplied intervals (stop and
      // start times) have the expected padding.  which are the elan 
      // user's choices
    endTime = (endTime/1000) - 0.3  
				    
    console.log("medium-agnostic playMediaSegment, line " + lineNumber + ", " +
				startTime + ", " + endTime)

    mediaSegmentEnd = endTime;
    mediaPlayer.currentTime = startTime
    //debugger;
    mediaPlayer.play();

} // playMediaSegment
//--------------------------------------------------------------------------------
$('#fontSizeSlider').on('input', function() {
    var v = $(this).val();
    //console.log(v)
    $("#textDiv").css('font-size', v + 'em')
    });

$('#videoSizeSelector').on('input', function() {
    var v = $(this).val();
    //console.log(v);
    $("#mediaPlayer").width(v);
    });

$('#speedSelector').on('input', function() {
    var v = $(this).val();
    //console.log(v)
    mediaPlayer.playbackRate = v;
	$("#playbackSpeedReadout").text(v);
    });



