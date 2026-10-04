
import WaveSurfer from 'https://unpkg.com/wavesurfer.js@7/dist/wavesurfer.esm.js'
import RecordPlugin from 'https://unpkg.com/wavesurfer.js@7/dist/plugins/record.esm.js'
import RegionsPlugin from 'https://unpkg.com/wavesurfer.js@7/dist/plugins/regions.esm.js'

var myVoicePlayer, myVoiceRecorder, myVoiceWavesurfer;
var sourceLineWavesurfer = null;
var sourceLineRegions = null;
var activeRegion = null;
// let regionDragStartX = null;
let regionRemovedForThisGesture = false;

//--------------------------------------------------------------------------------
function loadURL(url)
{
   myVoicePlayer.load(url)

} // loadURL
//--------------------------------------------------------------------------------
function createMyVoiceRecorder(containerID, buttonID, endOfRecordingFunction)
{
   console.log("--- entering recorderModule.createMyVoiceRecorder")
   console.log("    continainerID: " + containerID);
   myVoiceWavesurfer = WaveSurfer.create({
      container: containerID,
      waveColor: 'darkGray',
      progressColor: 'gray',
      height: 'auto',  // 160
      })
  
  myVoiceRecorder = myVoiceWavesurfer.registerPlugin(
    RecordPlugin.create({
       renderRecordedAudio: false,
       audioRate: 1, // Don't modify playback rate
       bufferSize: 512, // Try smaller values (1024, 512)
       scrollingWaveform: true,
       audioBitsPerSecond: 12800,       
       continuousWaveform: false,
       height: 'auto', // 160,
       }),
       ) // registerPlugin

  myVoiceRecorder.on('record-end', (blob) => {
     const recordedUrl = URL.createObjectURL(blob)
     console.log("record-end event handler")
     console.log("url: " + recordedUrl)
     endOfRecordingFunction(recordedUrl)
     })

  RecordPlugin.getAvailableAudioDevices().then((devices) => {
      console.log("audio device promise fulfilled");
      devices.forEach((device) => {
          console.log("device id: " + device.deviceId)
      })})

    return(myVoiceRecorder);
    
 } //createMyVoiceRecorder
//--------------------------------------------------------------------------------
function recordingEndHandler(recordedUrl)
{
   console.log(" ---- recording ended, seen by recorderModuleTest.html")
   console.log(" ---- url: " + recordedUrl)
   console.log("children: " +    $("#waveRecorderDiv").children().length)
   // $("#recorderDiv").children()[0].remove()
   $("#waveRecorderDiv").hide()
   $("#wavePlayerDiv").show()
   // $("#playRecordingButton").css("display", "inline-block")    
   $("#playRecordingButton").show()
   if(myVoicePlayer == undefined){
      myVoicePlayer = createMyVoicePlayer(recordedUrl, "#wavePlayerDiv", "#playRecordingButton")
      window.myVoicePlayer = myVoicePlayer
      console.log("myVoicePlayer")
      console.log(myVoicePlayer)
      }
   else{
      loadURL(recordedUrl)
      }

} // recordingEndHandler
//--------------------------------------------------------------------------------
function createMyVoicePlayer(url, containerID, buttonID)
{
  if(myVoicePlayer){
     console.log("--- destroying myVoicePlayer")
     myVoicePlayer.destroy();
     }

   myVoicePlayer = WaveSurfer.create({
      container: containerID,
      waveColor: 'darkGray',
      progressColor: 'gray',
      url: url
      })

    window.myVoicePlayer = myVoicePlayer;
    myVoicePlayer.on('finish', function() {
       console.log("playback finished");
       console.log("changing text to Play: " + buttonID)
       $(buttonID).text("Play")
       })

   $(buttonID).on("click", function(e){
       e.stopImmediatePropagation(); // not sure why this is needed
       let buttonLabel = $(buttonID).text()
       console.log("--- play/pause button click, current label: " + buttonLabel)
       if(buttonLabel == "Play"){
          $(buttonID).text("Pause")
          //console.log(myVoicePlayer)           
          myVoicePlayer.play();
          }
       else{
          console.log("--- pausing play");
          myVoicePlayer.pause()
          $(buttonID).text("Play")
          }
       }) // on button click

  return(myVoicePlayer)

} // createMyVoicePlayer
//--------------------------------------------------------------------------------
$(document).ready(function() {

    console.log(" ******* recordPopup.js, ready function")
        
   $('#waveformPopup').dialog({autoOpen: false,
                               title: 'Audio Waveform',
                               width: 'auto',
                               height: 'auto',
                               resizable: false,
                               closeText: " close ",
                               open: function(event, ui) {
                                  console.log("Dialog is visible. Safe to calculate sizes or focus elements.");
                                  }
                               });
    let errorText = `
        slexil offers a 'record your voice' option, but it works only in Chrome browsers.
        <br><br>Safari and FireFox support for recording is currently broken.
        <br><br>Note that you can install Chrome on most computers
        and devices: Windows computers, Android phones and tablets,
        as well as Apple desktops, laptops, iPads and iPhones.
        `;
         
   $('#recordingNotAvailablePopup').html(errorText)

   $("#openRecordDialogButton").on('click', function(){
       console.log("--- mic button clicked")
       const navString = navigator.userAgent.toLowerCase();
       const chromeBrowserDetected = navString.search("chrome") >= 0 |
             navString.search("crios") >= 0;
       console.log("chromeBrowserDetected? " + chromeBrowserDetected);
       if(!chromeBrowserDetected){
          $('#recorderAndPlayerDiv').hide()
          $('#recordingNotAvailablePopup').show()
          }
       else{
          $('#recorderAndPlayerDiv').show()
          $('#recordingNotAvailablePopup').hide()
          myVoiceRecorder = createMyVoiceRecorder("#waveRecorderDiv", "#recordButton",
                                    recordingEndHandler)
          }
       let newStatus = 'open'
       if($("#waveformPopup").is(":visible")){
          newStatus = 'close'
          }
       $("#waveformPopup").dialog(newStatus);
       if(newStatus == 'open'){
          displaySourceLine()
          }
       //if(typeof(recorder) == "undefined"){
       
      }); // on click

   $("#recordButton").on("click", function(){
       console.log("--- record button clicked")
       let incomingState = $("#recordButton").text()
       console.log(" incomingState: " + incomingState);
       if(incomingState == "Record"){
          $("#waveRecorderDiv").show()
          $("#wavePlayerDiv").hide()
          $("#recordButton").text("Stop Recording")
          if (typeof(myVoiceRecorder) == "undefined"){
             let deviceId = "default"; // $('#microphone-selector').find(":selected").val()
             console.log("mic deviceId: " + deviceId)
             }
          myVoiceRecorder.startRecording("default").then(() => {
             console.log("recording started, from promise")
             });
          }
       else{
          myVoiceRecorder.stopRecording()
          $("#recordButton").text("Record")
          }
       }) // if "Record"

    $("#showPlaySourceLineDetailsWidget").on('toggle', function(){
       console.log("*** details widget toggled")
       if($(this).prop('open')){
          console.log("load RWC");
          displaySourceLine()
          }
       }) // showPlaySourceLineDetailsWidget

   $("#waveformPopup").on("dialogclose", function(event, ui) {  // cleanup
       console.log("recordingPopup dialog closed via event listener.");
       if(sourceLineWavesurfer != null){
         $("#showPlaySourceLineDetailsWidget").removeAttr('open');
         console.log("--- destroying sourceLineWaveSurver")
         sourceLineWavesurfer.destroy()
         }
       myVoiceWavesurfer.destroy();
       sourceLineWavesurfer.destroy();
       if(myVoiceRecorder != undefined){
          myVoiceRecorder.destroy()
          }
       if(myVoicePlayer != undefined){
          myVoicePlayer.destroy()
          }
       myVoiceWavesurfer = undefined;
       sourceLineWavesurfer = undefined;
       myVoiceRecorder = undefined;
       myVoicePlayer = undefined;
       //if(myVoiceRecorder != null){
       //   console.log("--- destorying voice myVoiceRecorder");
          //recorder.stopMic()
          //recorder.destroy()
          //}
       }); // on dialogclose

  async function displaySourceLine(){
    console.log("--- entering displaySourceLine");
    const url = state.mediaPlayer.currentSrc
    const startMs = appState.get("startTime")
    const endMs = appState.get("endTime")
    const clip = new RemoteWavClip(url, startMs, endMs);
    const header = await clip.getMetadata()
    await clip.retrieve()
    console.log("--- clip retrieved")
    const blobUrl = clip.getObjectUrl()
    const audioEl = document.getElementById('clipAudioPlayer');
    audioEl.src = blobUrl;
    console.log("--- about to create sourceLineWavesurfer")

    function pixelXToSeconds(clientX) {
       let container = document.querySelector('#sourceLineWaveform')
       const rect = container.getBoundingClientRect()
       const relativeX = clientX - rect.left;
       const ratio = relativeX / rect.width;
       return ratio * sourceLineWavesurfer.getDuration();
       }

    if(sourceLineWavesurfer){
       sourceLineWavesurfer.destroy()
       }
    sourceLineWavesurfer = WaveSurfer.create({
        container: '#sourceLineWaveform',
        media: audioEl,
        url: blobUrl,
        waveColor: 'darkGray',
        progressColor: 'gray',
        height: 'auto', // 160,
        });
    window.xx = sourceLineWavesurfer;

    sourceLineRegions = sourceLineWavesurfer.registerPlugin(RegionsPlugin.create());
    sourceLineRegions.enableDragSelection({
       color: 'rgba(255, 0, 0, 0.15)',
      });

       // Keep only one region at a time -- a new drag replaces the old one
    sourceLineRegions.on('region-created', (region) => {
       console.log("region created")
       if (activeRegion && activeRegion !== region){
         activeRegion.remove();
         }
       activeRegion = region;
       sourceLineWavesurfer.play(region.start, region.end);
       });
      
    sourceLineRegions.on('region-clicked', (region, e) => {
       console.log("region-clicked");
       e.stopPropagation(); // prevent the click from also seeking/resetting via the waveform's own click handler
       sourceLineWavesurfer.play(region.start, region.end);
       });

   $("#sourceLineWaveform").on("pointerdown", function(e){
      console.log("pointerdown: " + e.clientX);
      //regionDragStartX = e.clientX;
      const clickedTime = pixelXToSeconds(e.clientX);
      if(!activeRegion) return;
      const insideActiveRegion =
         activeRegion &&
         clickedTime >= activeRegion.start &&
         clickedTime <= activeRegion.end;
      console.log("pointerdown, insideActiveRegion: " + insideActiveRegion)
      if(!insideActiveRegion){
         console.log("pointer down outside the active region")
         activeRegion.remove();
         activeRegion = null;
         regionRemovedForThisGesture = true;
         console.log(" seekTo(0)");
         setTimeout(() => {
            sourceLineWavesurfer.seekTo(0);          
            }, 100);
         }          
      //console.log("    startx: " + regionDragStartX);
      regionRemovedForThisGesture = false;
      });  // pointerdown

   $("#sourceLineWaveform").on("pointerup", function(e){
      const clickedTime = pixelXToSeconds(e.clientX);
      const insideActiveRegion =
          activeRegion &&
          clickedTime >= activeRegion.start &&
          clickedTime <= activeRegion.end;
      console.log("in active region: "+ insideActiveRegion)
      if(!insideActiveRegion && activeRegion){
         console.log("removing activeRegion");
         activeRegion.remove();
         activeRegion = null;
         regionRemovedForThisGesture = true;
         console.log(" setting time to 0");
         setTimeout(() => {
            sourceLineWavesurfer.seekTo(0);          
            }, 100);
         }
      }); // pointerup

    } // async function displaySourceLine

   }); // document ready

//--------------------------------------------------------------------------------
