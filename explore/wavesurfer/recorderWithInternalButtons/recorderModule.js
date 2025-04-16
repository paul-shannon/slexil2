import WaveSurfer from 'https://unpkg.com/wavesurfer.js@7/dist/wavesurfer.esm.js'
import RecordPlugin from 'https://unpkg.com/wavesurfer.js/dist/plugins/record.esm.js'

var recorder, wavesurfer;
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
       scrollingWaveform: false,
       continuousWaveform: true,
       continuousWaveformDuration: 30, // optional
       }),
       ) // registerPlugin

  /************
  $(buttonID).on("click", function() {
    let incomingState = $("#recordButton").text()
    if(incomingState == "Record"){
       //$(containerID).show()
       $("#recordButton").text("Stop")
       let deviceId = "default"; // $('#microphone-selector').find(":selected").val()
       console.log("mic deviceId: " + deviceId)
       recorder.startRecording("default").then(() => {
          console.log("recording started, from promise")
          });
       } // if "Record"
    else{  // must be "Stop"
       recorder.stopRecording()
       $("#recordButton").text("Record")
       }
     }) // recordButton click
   ************/

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
export default createRecorder;
