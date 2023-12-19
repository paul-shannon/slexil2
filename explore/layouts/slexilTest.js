var mediaPlayer = document.getElementById("mediaPlayer");
var mediaSegmentEnd;
var mediaContinuousPlay = true;
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
   console.log(" new text: " + newTextHeight)
   $("#textDiv").height(newTextHeight);
   } // refreshLayout

$(document).ready(function(){
   
   docHeight =  $(document).height()
   var initialMediaPlayerHeight = 50;
   if(document.getElementById('videoPlayer') != null){
      initialMediaPlayerHeight = 150;
      mediaPlayer = document.getElementById("videoPlayer")
      }
    else{
      mediaPlayer = document.getElementById("audioPlayer")
      }
   slop = 130;
   $("#textDiv").height(docHeight - (50 + 300 + slop))
   refreshLayout(initialMediaPlayerHeight);
    
   $("#showHideOtherControlsButton").on('click', function() {
      console.log("--- showOtherControls")
      visible = $("#otherControlsDiv").is(":visible")
      if(visible){
         $("#otherControlsDiv").hide()
         $("#showHideOtherControlsButton").text("Show Other Controls")
         }
       else{
          $("#otherControlsDiv").show()
          $("#showHideOtherControlsButton").text("Hide Other Controls")
          }
      }); // showHideOtherControlsButton
    
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
       mediaPlayer.playbackRate = v;
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


    //$(window).resize(function(){
    //   console.log("window resized: " + $(document).height)
    //   })
    //$(window).on( "resize", function(){
    //   console.log("window resize event: " + $(document).height)
    //   })
    
}) // ready

