var state = {
   mediaPlayer: null,          // will be either <audio> or <video>
   videoHeight: 250,           // initial size, adjusted by slider
   mediaPlayerInterval: 100,   // query media current time this often, msecs
   currentLine: 0,
   practiceLists: null
   }

var mediaSegmentEnd;
var mediaContinuousPlay = true;
var currentVideoSize = state.videoHeight;
var slexilJSdate = "2024-jan-02"
//--------------------------------------------------------------------------------
function getRandomInt(min, max)
{
   min = Math.ceil(min);
   max = Math.floor(max);
   return Math.floor(Math.random() * (max - min + 1)) + min;

} // getRandomInt
//--------------------------------------------------------------------------------
function refreshLayout(videoRequestedSize)
{
   if(document.getElementById('videoPlayer') != null){
      var oldVideoSize = $("#videoPlayer").height()
      if(videoRequestedSize > 350){
         return
         }
      var videoSizeDelta = videoRequestedSize - oldVideoSize;
      $("#videoPlayer").height(videoRequestedSize);
      var hvscd = $("#mediaPlayerAndControlsDiv").height() + videoSizeDelta;
      $("#mediaPlayerAndControlsDiv").height(hvscd)
      }

   //var docHeight = $("#mainDiv").outerHeight(true) - 10;
   var docHeight = document.body.scrollHeight;
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
        
   var fixedHeights = otherControlsDivHeight + playerDivHeight + margins;
   var newTextHeight = docHeight - (fixedHeights) - 50;
   
   console.log("      doc: " + docHeight)
   console.log("   player: " + playerDivHeight);
   console.log("     ctls: " + otherControlsDivHeight)
   console.log("  margins: " + margins)
   console.log(" new text: " + newTextHeight)
   $("#textDiv").height(newTextHeight);
   $("#annoDiv").height(newTextHeight-20);
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
   //if(document.getElementById('practiceDialog') != null){
   //   console.log("--- assigning state.practicDialog")
   //   state.practiceDialog = document.getElementById("practiceDialog")
   //   }

   if(document.getElementById('videoPlayer') != null){
      initialMediaPlayerHeight = state.videoHeight;
      $("#videoPlayer").height(initialMediaPlayerHeight)
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

   $("#showPracticeDialogButton").on('click', function(){
      console.log("show showPracticeDialog")
      state.practiceDialog.showModal()
      })

    $(".practiceButton").on('click', function(event){
       var button = $(this);
       var buttonLabel = $(this).text(); 
       console.log(buttonLabel);
       console.log(practiceLists);
       list = practiceLists[buttonLabel]
       if(list.length > 0){
          let lineNumber = list[0];
          scrollAndHighlight(lineNumber);
          practiceLists[buttonLabel] = practiceLists[buttonLabel].filter(item => item !== lineNumber)
          } // if length
       else{
          button.attr("disabled", true)
          }
      })

   $("#configurePracticeButton").on('click', function(event){
      const lineCount = $(".line-content").length;
      console.log("configure practice, lines: " + lineCount)
      var arr = []
      while(arr.length < lineCount){
         var randomnumber=Math.ceil(Math.random()*lineCount)
         if(arr.indexOf(randomnumber) === -1){arr.push(randomnumber)}  
         }
      console.log(arr)
      i = arr[2]
      playSample(i, timeStamps[i-1].start, timeStamps[i-1].end)
      event.preventDefault();
      event.stopPropagation();
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
          state.videoHeight = $("#videoPlayer").height();          
          $("#otherControlsDiv").show()
          $("#showHideOtherControlsButton").text("Hide Other Controls")
          }
      refreshLayout(state.videoHeight);
      }); // showHideOtherControlsButton
    
   $("#fasterPlaybackButton").on('click', function(){
       var currentSpeed = parseFloat($("#speedSelector").val())
      console.log("faster")
      if(currentSpeed <= 1.75){
         currentSpeed = currentSpeed + 0.25
         }
      $("#speedSelector").val(currentSpeed)
      $("#playbackSpeedReadout").text(currentSpeed)
      state.mediaPlayer.playbackRate = currentSpeed;
      })

   $("#slowerPlaybackButton").on('click', function(){
      console.log("slower")
      var currentSpeed = parseFloat($("#speedSelector").val())
      console.log("faster")
      if(currentSpeed >  0.25){
         currentSpeed = currentSpeed - 0.25
         }
      $("#speedSelector").val(currentSpeed)
      $("#playbackSpeedReadout").text(currentSpeed)
      state.mediaPlayer.playbackRate = currentSpeed;
      })


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
         state.videoHeight = $("#videoPlayer").height()
         refreshLayout(state.videoHeight)
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

    /**************
    function checkPlaybackTime(){
       var verbose = true;
       tCurrent = Math.round(state.mediaPlayer.currentTime * 1000)
       console.log("   " + tCurrent)
       if(tCurrent != state.tCurrent){
          state.tCurrent = tCurrent;
          for(lineTimes of timeStamps){
             if(lineTimes.start <= tCurrent && lineTimes.end >= tCurrent){
                var lineNumber = parseInt(lineTimes.id)
                scrollAndHighlight(lineNumber)
                break;
                } // if start <=
             } // for lineTimes
          if (!mediaContinuousPlay && mediaSegmentEnd && state.mediaPlayer.currentTime >= mediaSegmentEnd){
             state.mediaPlayer.pause();
             mediaContinuousPlay=true;
             } // reached end of segment
          } // if new time reported by player
      } // checkPlaybackTime

	 setInterval(checkPlaybackTime, state.mediaPlayerInterval);
    ************/

    state.mediaPlayer.addEventListener("timeupdate", function (){
       tCurrent = Math.round(state.mediaPlayer.currentTime * 1000)
       //console.log("    " + state.mediaPlayer.currentTime)
       //console.log("     tCurrent: " + tCurrent)
       //console.log("    state.currentLine: " + state.currentLine)
       for(lineTimes of timeStamps){
          if(lineTimes.start <= tCurrent && lineTimes.end >= tCurrent){
              var lineNumber = parseInt(lineTimes.id)
              //console.log("         currentLine: " + lineNumber)
              //console.log("         lineNumber: " + lineNumber)
             if (lineNumber != state.currentLine){ // only if new line
                 state.currentLine = lineNumber;
                 scrollAndHighlight(lineNumber)
					  break;
                 }
              } // if start <=
           } // for lineTimes
        if (!mediaContinuousPlay &&
               mediaSegmentEnd &&
               state.mediaPlayer.currentTime >= mediaSegmentEnd){
          //console.log("stop: "  + state.mediaPlayer.currentTime.toFixed(4) +
          //             " >= " + mediaSegmentEnd.toFixed(4))
          state.mediaPlayer.pause();
          mediaContinuousPlay=true;
          } // reached end
       })  // addEventListener timeupdate

}) // ready

var mediaSegmentEnd;
var mediaContinuousPlay = true;
//--------------------------------------------------------------------------------
function scrollAndHighlight(lineNumber){

   // from here:
   // https://stackoverflow.com/questions/27980084/scrolling-to-a-element-inside-a-scrollable-div-with-pure-javascript
   var scrollingDivTop = document.getElementById("textDiv").offsetTop

   console.log("--- scrollAndHighlight to line " + lineNumber);
   var lineDivTop = document.getElementById(lineNumber).offsetTop - scrollingDivTop;
    //lineDivTop -= 100;
    //lineDivTop -= 10;
    lineDivTop -= 80;

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
   // state.mediaPlayer = document.getElementById("audioPlayer")
   console.log("playSample: " + mediaID);
   playMediaSegment(mediaID, startTime, endTime)
   //console.log("currentLine: " + state.currentLine)
   let lineNumber = mediaID - 1;
   //console.log("lineNumber: " + lineNumber)
   let spokenText = ""
   if(lineNumber >= 0){
      spokenText = $(".speech-tier").get(lineNumber).innerHTML
      //console.log("spokenText: " + spokenText)
      noteText = lookup(spokenText)
      $("#annoNotesDiv").html(noteText)
      }


} // playSample
//--------------------------------------------------------------------------------
function playMediaSegment(mediaID, startTime, endTime)
{
   state.mediaPlayer.pause()
   //state.mediaPlayer.currentTime = 0;
   state.mediaPlayer.currentTime = null
   mediaContinuousPlay = false;
   startTime = startTime/1000;

      // subtract "earlyCatch" seconds so playback does not run over
      // this is dodgy, works only if the supplied intervals (stop and
      // start times) have the expected padding.  which are the elan 
      // user's choices
   earlyCatch = 0.1
   endTime = (endTime/1000) - earlyCatch
                
   console.log("play " + mediaID + ": " + startTime.toFixed(4) + ", " + endTime.toFixed(4))

   mediaSegmentEnd = endTime;
    if (!!navigator.userAgent.match(/Version\/[\d\.]+.*Safari/)){
       //console.log(" *** safari using fastSeek")
       state.mediaPlayer.fastSeek(startTime)
    	 }
	 else{
       //console.log(" *** NOT safari, using currentTime")
       state.mediaPlayer.currentTime = startTime
       }
   state.mediaPlayer.play();

} // playMediaSegment
//--------------------------------------------------------------------------------


