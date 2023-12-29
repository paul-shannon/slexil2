var state = {
   mediaPlayer: null,  // will be either <audio> or <video>
   videoSize: 150      // initial size, adjusted by slider
   }
//var mediaPlayer = document.getElementById("mediaPlayer");
var mediaSegmentEnd;
var mediaContinuousPlay = true;
var currentVideoSize = 150;  // to start
//--------------------------------------------------------------------------------
function refreshLayout(videoRequestedSize)
{
   if(document.getElementById('videoPlayer') != null){
      console.log("requested videoSize: " + videoRequestedSize)
      var oldVideoSize = $("#videoPlayer").height()
      var videoSizeDelta = videoRequestedSize - oldVideoSize;
      $("#videoPlayer").height(videoRequestedSize);
      var hvscd = $("#mediaPlayerAndControlsDiv").height() + videoSizeDelta;
      $("#mediaPlayerAndControlsDiv").height(hvscd)
      }

   var docHeight = $("#mainDiv").outerHeight(true); // $(document).height()
   var textDivHeight = $("#textDiv").outerHeight(true)
   var playerDivHeight = $("#mediaPlayerAndControlsDiv").outerHeight(true)
   var otherControlsDivHeight = 0

   if($("#otherControlsDiv").is(":visible")){
      otherControlsDivHeight = $("#otherControlsDiv").outerHeight(true)
      }
   console.log("otherControlsDivHeight: " + otherControlsDivHeight);
   var margins =  parseInt($("#mainDiv").css("margin-top")) +
	               parseInt($("#mainDiv").css("margin-bottom")) +
	               parseInt($("#mainDiv").css("padding-top")) +
	               parseInt($("#mainDiv").css("padding-bottom")) +
                  parseInt($("#mediaPlayerAndControlsDiv").css("margin-top")) + 
                  parseInt($("#mediaPlayerAndControlsDiv").css("margin-bottom")) +
                  parseInt($("#otherControlsDiv").css("margin-top")) +
                  parseInt($("#otherControlsDiv").css("margin-bottom")) +
                  parseInt($("#textDiv").css("margin-top")) +
                  parseInt($("#textDiv").css("margin-bottom"));
        
   var slop = 0
   var fixedHeights = otherControlsDivHeight + playerDivHeight + margins;
   var newTextHeight = docHeight - (fixedHeights + slop)
	
   console.log("      doc: " + docHeight)
   console.log("   player: " + playerDivHeight);
   console.log("     ctls: " + otherControlsDivHeight)
   console.log("  margins: " + margins)
   console.log(" new tExt: " + newTextHeight)
   $("#textDiv").height(newTextHeight);
   } // refreshLayout

//--------------------------------------------------------------------------------
$(document).ready(function(){
   
   console.log("--- slexilText.js, document ready")
   docHeight =  $(document).height()
   var initialMediaPlayerHeight = 50;
   if(document.getElementById('aboutBoxDialog') != null){
      console.log("--- assigning state.dialogBox")
      state.aboutBoxDialog = document.getElementById("aboutBoxDialog")
      }
   if(document.getElementById('videoPlayer') != null){
      initialMediaPlayerHeight = 150;
      state.mediaPlayer = document.getElementById("videoPlayer")
      }
    else{
      state.mediaPlayer = document.getElementById("audioPlayer")
      }
   slop = 130;
   $("#textDiv").height(docHeight - (50 + 300 + slop))
   refreshLayout(initialMediaPlayerHeight);
    
   $("#aboutBoxButton").on('click', function(){
      console.log("show aboutBox")
      state.aboutBoxDialog.showModal()
      })

   $("#closeAboutBoxButton").on('click', function(){
      state.aboutBoxDialog.close()
      })

	$("#aboutBoxDismissButton").on('click', function(){
	   state.aboutBoxDialog.close()
		})

   $("#showHideOtherControlsButton").on('click', function() {
      console.log("--- showOtherControls")
      visible = $("#otherControlsDiv").is(":visible")
      if(visible){
         $("#otherControlsDiv").hide()
         $("#showHideOtherControlsButton").text("Other Controls ...")
         }
       else{
          state.videoSize = $("#videoPlayer").height();          
          $("#otherControlsDiv").show()
          $("#showHideOtherControlsButton").text("Hide Other Controls")
          }
      refreshLayout(state.videoSize);
      }); // showHideOtherControlsButton
    
   $("#showAnnotationsButton").on('click', function() {
      visible = $("#annoDiv").is(":visible")
      if(visible){
         $("#annoDiv").hide()
         $("#showAnnotationsButton").text("Show Annotations")
         }
       else{
          $("#annoDiv").show()
          $("#showAnnotationsButton").text("Hide Annotations")
          }
       }) // showAnnotationsButton

    $('#videoSizeSelector').on('input', function() {
       var videoRequestedSize = Number($(this).val());
       console.log("videoRequestedSize: " + videoRequestedSize);
       refreshLayout(videoRequestedSize)
       }); // videoSizeSelector

    $('#fontSizeSlider').on('input', function() {
       var v = $(this).val();
       $("#textDiv").css('font-size', (v * 22) + 'px')
       $("#annoDiv").css('font-size', (v * 22) + 'px')
       });

    $('#speedSelector').on('input', function() {
       var v = $(this).val();
       state.mediaPlayer.playbackRate = v;
       $("#playbackSpeedReadout").text(v);
       });

    var $window = $(window);
    var width = $window.width();
    var height = $window.height();

    setInterval(function () {
      if ((width != $window.width()) || (height != $window.height())) {
         width = $window.width();
         height = $window.height();
         console.log("resized!");
         videoSize = $("#videoPlayer").height()
         refreshLayout(videoSize)
         }
       }, 300);

    $("#tierToggle-transcription").on('click', function() {
		  console.log("transcription toggled")
		  $(".speech-tier").toggle(this.checked)
        })

    $("#tierToggle-translation").on('click', function() {
		  console.log("translation toggled")
		  $(".freeTranslation-tier").toggle(this.checked)
        })

    $("#tierToggle-analysis").on('click', function() {
		  console.log("analysis toggled")
		  $(".morpheme-tier").toggle(this.checked)
        })

	 state.mediaPlayer.addEventListener("timeupdate", function (){
		 tCurrent = Math.round(state.mediaPlayer.currentTime * 1000)
		  verbose = true;
		  if(verbose){
           console.log("--- timeupdate " + tCurrent + " continuous? " + mediaContinuousPlay)
			  console.log("    raw: " + state.mediaPlayer.currentTime)
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
              } // if start <=
           } // for lineTimes

      if (!mediaContinuousPlay && mediaSegmentEnd && state.mediaPlayer.currentTime >= mediaSegmentEnd){
         if(verbose){
            console.log("--- stopping play, because currentTime (" + state.mediaPlayer.currentTime.toFixed(2) +
                        ") is >= mediaSegmentEnd (" + mediaSegmentEnd.toFixed(2) + ")");
           }
        state.mediaPlayer.pause();
        mediaContinuousPlay=true;
        }   

    })  // addEventListener timeupdate


    //$(window).resize(function(){
    //   console.log("window resized: " + $(document).height)
    //   })
    //$(window).on( "resize", function(){
    //   console.log("window resize event: " + $(document).height)
    //   })
    
}) // ready

var mediaSegmentEnd;
var mediaContinuousPlay = true;
//--------------------------------------------------------------------------------
function scrollAndHighlight(lineNumber){

   // from here:
   // https://stackoverflow.com/questions/27980084/scrolling-to-a-element-inside-a-scrollable-div-with-pure-javascript
   var scrollingDivTop = document.getElementById("textDiv").offsetTop

   //console.log("--- scrollAndHighlight to line " + lineNumber);
   var lineDivTop = document.getElementById(lineNumber).offsetTop - scrollingDivTop;
    //lineDivTop -= 100;
	 lineDivTop -= 10;

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
    state.mediaPlayer.currentTime = startTime
    //debugger;
    state.mediaPlayer.play();

} // playMediaSegment
//--------------------------------------------------------------------------------


