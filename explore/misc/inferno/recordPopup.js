<div id="recordingPopup" style="display: none"></div>

<script type="module">
import WaveSurfer from 'https://unpkg.com/wavesurfer.js@7/dist/wavesurfer.esm.js'
import RecordPlugin from 'https://unpkg.com/wavesurfer.js/dist/plugins/record.esm.js'

var recorder, wavesurfer;
wavesurfer = WaveSurfer.create({container: "#recorderDiv"})
recorder = wavesurfer.registerPlugin(
    RecordPlugin.create({
       renderRecordedAudio: true,
       scrollingWaveform: true,
       continuousWaveform: true,
       continuousWaveformDuration: 30, // optional
    }))


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
       renderRecordedAudio: true,
       scrollingWaveform: true,
       continuousWaveform: true,
       continuousWaveformDuration: 30, // optional
       }),
       ) // registerPlugin

  recorder.on('record-end', (blob) => {
     const recordedUrl = URL.createObjectURL(blob)
     console.log("record-end event handler")
     console.log("url: " + recordedUrl)
     endOfRecordingFunction(recordedUrl)
     })

  RecordPlugin.getAvailableAudioDevices().then((devices) => {
      console.log("device promise fulfilled");
      devices.forEach((device) => {
          console.log(device.deviceId)
      })})

    return(recorder);
    
 } //createRecorder
//--------------------------------------------------------------------------------
function recordingEndHandler(recordedUrl)
{
   console.log(" ---- recording ended, seen by recorderModuleTest.html")
   console.log(" ---- url: " + recordedUrl)
}
//--------------------------------------------------------------------------------
$(document).ready(function() {
   $('#buttonsAndRecorderDiv').dialog({autoOpen: false,
                                       title: 'Record Your Voice',
                                       width: 800
                                       });
   $("#openRecordDialogButton").on('click', function(){
       let newStatus = 'open'
       if($("#buttonsAndRecorderDiv").is(":visible")){
          newStatus = 'close'
          }
       $("#buttonsAndRecorderDiv").dialog(newStatus);
       });

    $("#recordButton").on("click", function(){
       console.log("record!")
       let incomingState = $("#recordButton").text()
       console.log(" incomingState: " + incomingState);
       if(incomingState == "Record"){
          $("#recorderDiv").show()
          $("#playerDiv").hide()
          $("#recordButton").text("Stop")
          recorder = createRecorder("#recorderDiv", "#recordButton",
                                    recordingEndHandler);   
          let deviceId = "default"; // $('#microphone-selector').find(":selected").val()
          console.log("mic deviceId: " + deviceId)
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

</script>



