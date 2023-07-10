body, html {
	font-family: "New York Times-Roman";
	font-size: 22px;
	height: 100%;
	}

#controlsDiv{
	height: 30vh;
	overflow-y: scroll;
	}

#textAndAnnoDiv{
	margin-top: 5px;
	margin-left: 5px;
	margin-right: 5px;
	height: 65vh;
	}
#textDiv{
	overflow-y: scroll;
	margin-left: 0px;
	margin-right: 0px;
	margin-top: 0px;
	height: 65vh;
	outline-color: gray;
	outline-style: solid;
	outline-offset: 0px;
	outline-width: 1px;

}

#annoDiv{
	display: none;
	overflow-y: scroll;
	outline-color: gray;
	outline-style: solid;
	outline-offset: 0px;
	outline-width: 1px;
	margin-right: 0px;
	margin-top: 0px;
	height: 65vh;
	}


.sliderControlDiv{
	margin: 10px;
	margin-left: 100px;
}

#infoDiv{
	margin-top: 15px;
	margin-left: 40px;
	font-size: 24px;
	}

	#mediaPlayer{
	width: 400px;
	}
#mediaPlayerDiv{
	margin-top: 10px;
	margin-left: 100px;
}

#playbackSpeedReadout{
	width: 35px;
	height: 24px;
	padding-left: 5px;
	margin: 5px;
	border: 1px solid green;
	font-size: 14px;
	display: inline-block;
}

#h3Title{
	display: inline-block;
	}

.line-wrapper {
	display: grid;
	grid-template-columns: 1fr 20fr;
	margin: 20px;
	background: white;
}

.line-sidebar{
	background: white;
	padding: 10px;
	padding-top: 4px;
	width: 40px;
	margin-top: 0px;
	margin-right: 10px;
	font-size: 24px;
	}
	
	.line-content{
	height: 100%;
	margin: 0px;
	margin-bottom: 2px;
	overflow-wrap: word-wrap;
	}
	
	
	.line {
	background-color: transparent;
	font-weight: bold;
	padding-left: 20px;
	padding: 0px;
	margin-top:  0px;
	margin-bottom:  10px;
	}
	
	.speech-tier{
	background-color: transparent;
	grid-template-columns: none;
	padding: 0px;
	text-align: left;
	vertical-align: bottom;
	margin-left: 5px;
	word-spacing: 20px;
	}
	
	.freeTranslation-tier{
	grid-template-columns: auto;
	padding: 0px;
	text-align: left;
	margin-left: 5px;
	}
	
	.secondTranscription-tier{
	padding: 0px;
	text-align: left;
	margin-left: 5px;
	word-spacing: 20px;
	}
	
	.gloss-tier{
	background-color: transparent;
	grid-template-columns: auto;
	padding: 10px;
	text-align: left;
	margin-left: 30px;
	word-spacing: 20px;
	}
	
	.morpheme-tier {
	display: grid;
	border: 0px solid rgba(0, 0, 0, 0.8);
	grid-template-columns: 4ch 5ch 5ch 4ch 5ch 12ch 7ch 5ch 16ch;
	grid-column-gap: 2%;
	margin: 5px;
	width: 95%;
	justify-content: flex-start;
	overflow-wrap: word-wrap;
	}
	
	.morpheme-cell {
	margin-bottom: 2px;
	padding: 3px;
	text-align: left;
	}
	
	.focusedGrammaticalElement{
	background-color: lightgray;
	}
	
	#annoButtonsDiv{
	margin-left: 80px;
	margin-bottom: 10px;
	}
	
	#toggleAnnotationsButton{
	margin-top: 10px;
	}
	
	
	#linguisticTopicController{
	   margin-top: 10px;
	   display: none; 
       }
	
	#linguisticTopicSelectorLabel{
	margin: 20px;
	}
	
	.dropdown{
	display: inline-block;
	}
	
	
	button{
	background-color: white;
	border: 0px;
	}
	
	.grammatical-term {
	font-variant: small-caps;
	color: blue;
	}
	
	sup {
	vertical-align:text-top; 
	font-size:75%; 
	}
	sub {
	vertical-align:text-middle; 
	font-size:75%; 
	}
	
	.playerxx {
	width: 100%;
	height: 22px;
	background: #0101DF;
	border-bottom: 4px solid;
	border-top: 4px solid;
	border-left: 4px solid;
	border-right: 4px solid;
	z-index: 1;
	position: fixed;
	bottom: 0px;
	left: -5px;
	}
	
	.current-line {
	background: #B6E8FF;
	-moz-border-radius: 5px;
	-webkit-border-radius: 5px;
	border-radius: 5px;
	}
	
	.mouseEntered{
	background: lightgrey;
	}
	
	.audio-wrapper {
	position: relative;
	margin: 0 auto;
	width: 100%;
	}
	
	.audio-wrapper audio {
	position: absolute;
	top:4px;
	left:0px;
	}

.spacer {
	height: 32px;
	}
