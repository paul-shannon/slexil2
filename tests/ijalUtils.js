// ijalUtil.js
//----------------------------------------------------------------------------------------------------

var rec = document.getElementById("audioplayer");
var annotationPlaying = null;
var currentLine = null;
var currentAnnotation = 'none';
var scrollingOn = false;
var halfWindow = window.innerHeight/3;
var fullRecIsPlaying = false;

//----------------------------------------------------------------------------------------------------
function playSample(audioID)
{
   if (currentLine != null) {currentLine.className ='line-wrapper';}
   console.log(audioID);
   document.getElementById(audioID).play();
}
//----------------------------------------------------------------------------------------------------

//annotationPlaying = document.getElementById('1');
rec.ontimeupdate = function() {trackAnnotations()};
rec.onended = function() {removeFinalHighlight()};
rec.onplay = function() {recPlay()};
rec.onpause = function() {recPaused()}
rec.onseeked = function() {moveToSliderPosition()};
// rec.addEventListener("seeked",moveToSliderPosition());

function trackAnnotations() {
	if (fullRecIsPlaying) {
		currentAnnotation = findCurrentAnnotation(rec.currentTime);
    findAnnotations(currentAnnotation);
	}
}
//----------------------------------------------------------------------------------------------------

function findAnnotations(currentAnnotation) {
		halfWindow = (window.innerHeight/4);
		if (currentAnnotation != 'none') {
			if (currentAnnotation != null) {
				currentLine = document.getElementById(currentAnnotation.id);
				selectCurrentAnnotation(currentLine);
				}
			}
}
//----------------------------------------------------------------------------------------------------
function selectCurrentAnnotation(currentLine) {
        if (annotationPlaying != currentLine) {
            annotationPlaying.className ='line-wrapper';
            if (scrollingOn = true) {
				          currentLineOffset = $(annotationPlaying).offset();
				          $('html,body').animate({
					                   scrollTop: currentLineOffset.top-halfWindow
					                   },1000);
			           }
            }
        currentLine.className += ' current-line';
        annotationPlaying = currentLine;
        if (! scrollingOn) {isScrolledIntoView(annotationPlaying)}
}

//----------------------------------------------------------------------------------------------------
// Returns the annotation in which this time (in milliseconds) occurs, or
// null if this time is not associated with an annotation.

function findCurrentAnnotation(time_ms) {
        for (var i = 0; i < window.annotations.length; i++) {
            annotation = window.annotations[i];
            if ((time_ms >= annotation.start/1000) && (time_ms <= annotation.end/1000)) {
                return annotation;
            }
        }
        return null;
}

//----------------------------------------------------------------------------------------------------

function removeFinalHighlight() {
	annotationPlaying.className ='line-wrapper';
}
//----------------------------------------------------------------------------------------------------

function isScrolledIntoView(elem)
{
    var docViewTop = $(window).scrollTop();
    var docViewBottom = docViewTop + $(window).height();

    var elemTop = $(elem).offset().top;
    var elemBottom = elemTop + $(elem).height()+23;
    if ((elemBottom <= docViewBottom) && (elemTop >= docViewTop)) {
    	scrollingOn = false;
    	} else {
    	scrollingOn = true;
    	}

//     return ((elemBottom <= docViewBottom) && (elemTop >= docViewTop));
}
//----------------------------------------------------------------------------------------------------

function recPlay()
{
  if (annotationPlaying == null) {
    annotationPlaying = document.getElementById('1');
  }
  currentLineOffset = $(annotationPlaying).offset();
  $('html,body').animate({
            scrollTop: currentLineOffset.top-halfWindow
            },1000);
  findAnnotations(annotationPlaying);
  fullRecIsPlaying = true;
}
//----------------------------------------------------------------------------------------------------

function recPaused()
{
	fullRecIsPlaying = false;
}
//----------------------------------------------------------------------------------------------------

//jump the animation to a point in the recording the user sets with slider control

function moveToSliderPosition()
{
  if (fullRecIsPlaying) {
    annotationPlaying.className ='line-wrapper';
  	lineIDNumber = slideToAnnotation()
    currentLine = document.getElementById(lineIDNumber);
    currentLineOffset = $(currentLine).offset();
    $('html,body').stop(true).animate({
   			scrollTop: currentLineOffset.top-halfWindow
      },1000);
    currentLine.className += ' current-line';
    annotationPlaying = currentLine;
	}
}

function slideToAnnotation()
{
    time_ms = rec.currentTime;
    for (var i = 0; i < window.annotations.length; i++) {
      annotation = window.annotations[i];
      if ((time_ms <= annotation.end/1000)) {
          return annotation.id;
      }
  }
}
