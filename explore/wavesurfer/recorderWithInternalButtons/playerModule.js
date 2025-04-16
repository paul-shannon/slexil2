import WaveSurfer from 'https://unpkg.com/wavesurfer.js@7/dist/wavesurfer.esm.js'

var player;
//--------------------------------------------------------------------------------
export function createPlayer(url, containerID, buttonID)
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

    player.pid = Date.now()
    
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
          console.log("--- asking player.play, player: " + player.pid)
          //console.log(player)           
          player.play();
          }
       else{
          console.log("--- pausing play");
          player.pause()
          $(buttonID).text("Play")
          }
       }) // on button click

} // createPlayer
//--------------------------------------------------------------------------------
export function loadURL(url)
{
   player.load(url)

} // loadURL
//--------------------------------------------------------------------------------
// export default createPlayer; 
