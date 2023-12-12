function refreshLayout(videoRequestedSize){
   console.log("requested videoSize: " + videoRequestedSize)
   var oldVideoSize = $("#mediaPlayer").height()
   var videoSizeDelta = videoRequestedSize - oldVideoSize;
	$("#mediaPlayer").height(videoRequestedSize);
   var hvscd = $("#mediaPlayerAndControlsDiv").height() + videoSizeDelta;
   $("#mediaPlayerAndControlsDiv").height(hvscd)

   var docHeight = $(document).height()
   var textDivHeight = $("#textDiv").height()
   var videoDivHeight = $("#mediaPlayerAndControlsDiv").height()
   var controlsDivHeight = 0
   if($("#controlsDiv").is(":visible")){
      controlsDivHeight = $("#controlsDiv").height()
      }
   console.log("controlsDivHeight: " + controlsDivHeight);
   var margins =  parseInt($("#mainDiv").css("margin-top")) +
                  parseInt($("#mediaPlayerAndControlsDiv").css("margin-top")) + 
                  parseInt($("#mediaPlayerAndControlsDiv").css("margin-bottom")) +
                  parseInt($("#controlsDiv").css("margin-top")) +
                  parseInt($("#controlsDiv").css("margin-bottom")) +
                  parseInt($("#textDiv").css("margin-top")) +
                  parseInt($("#textDiv").css("margin-bottom"));
        
   // margins = 130;
   var newTextHeight = docHeight - (controlsDivHeight + videoDivHeight + margins)
   console.log("  doc: " + docHeight)
   console.log("video: " + videoDivHeight);
   console.log(" ctls: " + controlsDivHeight)
   console.log(" margins: " + margins)
   console.log(" new text: " + newTextHeight)
   $("#textDiv").height(newTextHeight);
   } // refreshLayout

$(document).ready(function(){
   
   docHeight =  $(document).height()
  // $("#mediaPlayerAndControlsDiv").height(100)
   var initialMediaPlayerHeight = 100;
   $("#mediaPlayer").height(initialMediaPlayerHeight)
   slop = 130;
   $("#textDiv").height(docHeight - (50 + 300 + slop))
   refreshLayout(initialMediaPlayerHeight);
    
   $("#showHideOtherControlsButton").on('click', function() {
      console.log("--- showOtherControls")
      visible = $("#controlsDiv").is(":visible")
      if(visible){
         $("#controlsDiv").hide()
         $("#showHideOtherControlsButton").text("Show Other Controls")
         }
       else{
          $("#controlsDiv").show()
          $("#showHideOtherControlsButton").text("Hide Other Controls")
          }
      }); // showHideOtherControlsButton
    
    $('#videoSizeSelector').on('input', function() {
       var videoRequestedSize = Number($(this).val());
       console.log("videoRequestedSize: " + videoRequestedSize);
       refreshLayout(videoRequestedSize)
       }); // videoSizeSelector

    var $window = $(window);
    var width = $window.width();
    var height = $window.height();

    setInterval(function () {
      if ((width != $window.width()) || (height != $window.height())) {
         width = $window.width();
         height = $window.height();
         console.log("resized!");
         videoSize = $("#mediaPlayer").height()
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

