// ijalUtil.js
//----------------------------------------------------------------------------------------------------

var rec = document.getElementById("audioplayer");
var annotationPlaying = null;
var currentLine = null;
var currentAnnotation = 'none';
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

annotationPlaying = document.getElementById('1');
rec.ontimeupdate = function() {trackAnnotations()};
rec.onended = function() {removeFinalHighlight()};
rec.onplay = function() {recPlay()};
rec.onpause = function() {recPaused()}
//rec.onseeked = function() {moveToSliderPosition()};

function trackAnnotations() {
	if (fullRecIsPlaying) {
		currentAnnotation = findCurrentAnnotation(rec.currentTime);
		halfWindow = (window.innerHeight/4);
		if (currentAnnotation != 'none') {
			if (currentAnnotation != null) {
				currentAnnotationID = currentAnnotation.id;
				currentLineID = currentAnnotationID.replace('a','');
				currentLine = document.getElementById(currentLineID);
				setCurrentAnnotation(currentLine);
				}
			} 	
	}
}
//----------------------------------------------------------------------------------------------------

function setCurrentAnnotation(currentLine) {
        if (annotationPlaying != currentLine) {
            annotationPlaying.className ='line-wrapper';
            if (scrollingOn = true) {
				currentLineOffset = $(annotationPlaying).offset()
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
	fullRecIsPlaying = true;
	if (rec.played.length <= 1) {
		$('html,body').animate({
			scrollTop: 0
			},1000);
		}
}
//----------------------------------------------------------------------------------------------------

function recPaused()
{
	fullRecIsPlaying = false;
}
//----------------------------------------------------------------------------------------------------

//this was supposed to jump the animation to a  point in the recording if the user set
//it with the slider control, but it has all kinds of bizarre knock on effects; it seems
//like the seeked event is triggered during a slide, not when the slide is finished, so 
//you get a long queue of events calling this function(??)

function moveToSliderPosition()
{
	currentAnnotation = findCurrentAnnotation(rec.currentTime);
	if (currentAnnotation) {
		console.log(currentAnnotation.id)
		currentAnnotationID = currentAnnotation.id;
		currentLineID = currentAnnotationID.replace('a','');
		currentLine = document.getElementById(currentLineID);
// 		currentLineOffset = $(currentLine).offset();
// 		$('html,body').animate({
// 			scrollTop: currentLineOffset.top-halfWindow
// 			},1000);
// 		currentLine.className += ' current-line';      
//         annotationPlaying = currentLine;
	}
}
