var player, recorder, wavesurfer;

import WaveSurfer from 'https://unpkg.com/wavesurfer.js@7/dist/wavesurfer.esm.js'
import RecordPlugin from 'https://unpkg.com/wavesurfer.js@7/dist/plugins/record.esm.js'

var recorder, wavesurfer;
var sourceLineWaveSurfer = null;

//--------------------------------------------------------------------------------
function loadURL(url)
{
   player.load(url)

} // loadURL
//--------------------------------------------------------------------------------
function createRecorder(containerID, buttonID, endOfRecordingFunction)
{
   console.log("--- entering recorderModule.createRecorder")
   wavesurfer = WaveSurfer.create({
      container: containerID,
      waveColor: 'darkGray',
      progressColor: 'gray',
      height: 160,
      })
  
  recorder = wavesurfer.registerPlugin(
    RecordPlugin.create({
       renderRecordedAudio: false,
       audioRate: 1, // Don't modify playback rate
       bufferSize: 512, // Try smaller values (1024, 512)
       scrollingWaveform: true,
       audioBitsPerSecond: 12800,       
       continuousWaveform: false,
       height: 160,
       }),
       ) // registerPlugin

  recorder.on('record-end', (blob) => {
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

    return(recorder);
    
 } //createRecorder
//--------------------------------------------------------------------------------
function recordingEndHandler(recordedUrl)
{
   console.log(" ---- recording ended, seen by recorderModuleTest.html")
   console.log(" ---- url: " + recordedUrl)
   console.log("children: " +    $("#waveRecorderDiv").children().length)
   // $("#recorderDiv").children()[0].remove()
   $("#waveRecorderDiv").hide()
   $("#wavePlayerDiv").show()
   $("#playRecordingButton").css("display", "inline-block")    
   $("#playRecordingButton").show()
   if(player == undefined){
      player = createPlayer(recordedUrl, "#wavePlayerDiv", "#playRecordingButton")
      window.player = player
      console.log("player")
      console.log(player)
      }
   else{
      loadURL(recordedUrl)
      }

} // recordingEndHandler
//--------------------------------------------------------------------------------
function createPlayer(url, containerID, buttonID)
{
  if(player){
     console.log("--- destroying player")
     player.destroy();
     }

   player = WaveSurfer.create({
      container: containerID,
      waveColor: 'darkGray',
      progressColor: 'gray',
      url: url
      })

    window.player = player;
    player.on('finish', function() {
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
          //console.log(player)           
          player.play();
          }
       else{
          console.log("--- pausing play");
          player.pause()
          $(buttonID).text("Play")
          }
       }) // on button click

  return(player)

} // createPlayer
//--------------------------------------------------------------------------------
$(document).ready(function() {

    console.log(" ******* recordPopup.js, ready function")
        
   $('#waveformPopup').dialog({autoOpen: false,
                               title: 'Audio Waveform',
                               width: 800,
                               height: 800,
                               closeText: " close "
                               });
   $('#recordingNotAvailablePopup').dialog({autoOpen: false,
                                            title: 'Record your voice not available',
                                            width: 800,
                                            height: 400,
                                            closeText: "&times;"
                                            });
    let errorText = `
        The 'record your voice' capability only works in Chrome browsers.
        <br>Safari and FireFox support for recording is currently broken.
        <br><br>Note that you can install Chrome on most computers
        and devices: Windows computers, Android phones and tablets,
        as well as Apple desktops, laptops, iPads and iPhones.
        `;
         
   $('#recordingNotAvailablePopup').html(errorText)

   $("#openRecordDialogButton").on('click', function(){
       console.log("--- mic button clicked")
       const chromeBrowserDetected = true;
             // navigator.userAgent.toLowerCase().search("chrome") >= 0;
       if(!chromeBrowserDetected){
          $('#recordingNotAvailablePopup').dialog('open')
          }
       else{       
          let newStatus = 'open'
          if($("#waveformPopup").is(":visible")){
             newStatus = 'close'
             }
          $("#waveformPopup").dialog(newStatus);
           if(newStatus == 'open'){
              displaySourceLine()
              }
          } // else
       }); // on click

   if (typeof(recorder) == "undefined"){
        recorder = createRecorder("#waveRecorderDiv", "#recordButton",
                                  recordingEndHandler);
      }

   $("#recordButton").on("click", function(){
       console.log("--- record button clicked")
       let incomingState = $("#recordButton").text()
       console.log(" incomingState: " + incomingState);
       if(incomingState == "Record Your Voice"){
          $("#waveRecorderDiv").show()
          $("#wavePlayerDiv").hide()
          $("#recordButton").text("Stop Recording")
          if (typeof(recorder) == "undefined"){
             //recorder = createRecorder("#waveRecorderDiv", "#recordButton",
             //                          recordingEndHandler);   
             let deviceId = "default"; // $('#microphone-selector').find(":selected").val()
             console.log("mic deviceId: " + deviceId)
             window.recorder = recorder;
             }
          recorder.startRecording("default").then(() => {
             console.log("recording started, from promise")
             });
          }
       else{
          recorder.stopRecording()
          $("#recordButton").text("Record Your Voice")
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
      if(sourceLineWaveSurfer != null)
         $("#showPlaySourceLineDetailsWidget").removeAttr('open');
         sourceLineWaveSurfer.destroy()
      });

  async function displaySourceLine(){
    console.log("--- entering displaySourceLine");
    const url = state.mediaPlayer.currentSrc
    const startMs = appState.get("startTime")
    const endMs = appState.get("endTime")
    //const startMs = Number($("#outStart").text())
    //const endMs = Number($("#outEnd").text())
    const clip = new RemoteWavClip(url, startMs, endMs);
    const header = await clip.getMetadata()
    await clip.retrieve()
    console.log("--- clip retrieved")
    const blobUrl = clip.getObjectUrl()
    const audioEl = document.getElementById('clipAudioPlayer');
    audioEl.src = blobUrl;
    console.log("--- about to create sourceLineWaveSurfer")
    if(sourceLineWaveSurfer){
       sourceLineWaveSurfer.destroy()
       }
    sourceLineWaveSurfer = WaveSurfer.create({
        container: '#sourceLineWaveform',
        media: audioEl,
        url: blobUrl,
        waveColor: 'darkGray',
        progressColor: 'gray',
        height: 160,
        });
    } // async function displaySourceLine

   }); // document ready


