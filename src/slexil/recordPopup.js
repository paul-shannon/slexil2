var player, recorder, wavesurfer;

import WaveSurfer from 'https://unpkg.com/wavesurfer.js@7/dist/wavesurfer.esm.js'
import RecordPlugin from 'https://unpkg.com/wavesurfer.js@7/dist/plugins/record.esm.js'

var recorder, wavesurfer;

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
      waveColor: '#4F4A85',
      progressColor: '#383351',
      })

  
  recorder = wavesurfer.registerPlugin(
    RecordPlugin.create({
       renderRecordedAudio: false,
       audioRate: 1, // Don't modify playback rate
       bufferSize: 512, // Try smaller values (1024, 512)
       scrollingWaveform: true,
       audioBitsPerSecond: 12800,       
       continuousWaveform: false,
      // continuousWaveformDuration: 30, // optional
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
   console.log("children: " +    $("#recorderDiv").children().length)
   // $("#recorderDiv").children()[0].remove()
   $("#recorderDiv").hide()
   $("#playerDiv").show()
   $("#playRecordingButton").show()
   if(player == undefined){
      player = createPlayer(recordedUrl, "#playerDiv","#playRecordingButton")
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
      waveColor: '#4F4A85',
      progressColor: '#383351',
      url: url
      })

    window.player = player;
    player.on('finish', function() {
       console.log("playback finished");
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

        
   $('#recordingPopup').dialog({autoOpen: false,
                               title: 'Record Your Voice',
                               width: 800,
                               height: 400,
                               closeText: "&times;"
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
       const chromeBrowserDetected =
             navigator.userAgent.toLowerCase().search("chrome") >= 0;
       if(!chromeBrowserDetected){
          $('#recordingNotAvailablePopup').dialog('open')
          }
       else{       
          let newStatus = 'open'
          if($("#recordingPopup").is(":visible")){
             newStatus = 'close'
             }
           $("#recordingPopup").dialog(newStatus);
          } // else
       }); // on click

   $("#recordButton").on("click", function(){
       console.log("--- record button clicked")
       let incomingState = $("#recordButton").text()
       console.log(" incomingState: " + incomingState);
       if(incomingState == "Record"){
          $("#recorderDiv").show()
          $("#playerDiv").hide()
          $("#recordButton").text("Stop")
          if (typeof(recorder) == "undefined"){
             recorder = createRecorder("#recorderDiv", "#recordButton",
                                       recordingEndHandler);   
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
          $("#recordButton").text("Record")
          }
       }) // if "Record"


   }); // document ready


