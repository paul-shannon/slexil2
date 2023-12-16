function refreshLayout(videoRequestedSize){

   console.log("requested videoSize: " + videoRequestedSize)

   if(document.getElementById('videoPlayer') != null){
      var oldVideoSize = $("#videoPlayer").height()
      var videoSizeDelta = videoRequestedSize - oldVideoSize;
   	$("#videoPlayer").height(videoRequestedSize);
      var hvscd = $("#mediaPlayerAndControlsDiv").height() + videoSizeDelta;
      $("#mediaPlayerAndControlsDiv").height(hvscd)
    	}

   var docHeight = $(document).height()
   var textDivHeight = $("#textDiv").height()
   var videoDivHeight = $("#mediaPlayerAndControlsDiv").height()
   var otherControlsDivHeight = 0
   if($("#otherControlsDiv").is(":visible")){
      otherControlsDivHeight = $("#otherControlsDiv").height()
      }
   console.log("otherControlsDivHeight: " + otherControlsDivHeight);
   var margins =  parseInt($("#mainDiv").css("margin-top")) +
                  parseInt($("#mediaPlayerAndControlsDiv").css("margin-top")) + 
                  parseInt($("#mediaPlayerAndControlsDiv").css("margin-bottom")) +
                  parseInt($("#otherControlsDiv").css("margin-top")) +
                  parseInt($("#otherControlsDiv").css("margin-bottom")) +
                  parseInt($("#textDiv").css("margin-top")) +
                  parseInt($("#textDiv").css("margin-bottom"));
        
   // margins = 130;
   var newTextHeight = docHeight - (otherControlsDivHeight + videoDivHeight + margins)
   console.log("  doc: " + docHeight)
   console.log("video: " + videoDivHeight);
   console.log(" ctls: " + otherControlsDivHeight)
   console.log(" margins: " + margins)
   console.log(" new text: " + newTextHeight)
   $("#textDiv").height(newTextHeight);
   } // refreshLayout

$(document).ready(function(){
   
   docHeight =  $(document).height()
   var initialMediaPlayerHeight = 50;
   if(document.getElementById('videoPlayer') != null){
      initialMediaPlayerHeight = 150;
      }
   $("#mediaPlayer").height(initialMediaPlayerHeight)
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

