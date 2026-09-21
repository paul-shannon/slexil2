var player, recorder, wavesurfer;

import WaveSurfer from 'https://unpkg.com/wavesurfer.js@7/dist/wavesurfer.esm.js'
import RecordPlugin from 'https://unpkg.com/wavesurfer.js@7/dist/plugins/record.esm.js'

var recorder, wavesurfer;
var sourceLineWaveSurfer = null;

$(document).ready(function() {

   console.log(" ******* waveformPopup.js, ready function")

    $("#openRecordDialogButton").on('click', function(){
        console.log("open recordDialogButton click")
    })

})

