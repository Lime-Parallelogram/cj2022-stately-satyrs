// Audio settings
const BUFFER_SIZE = 80  // Max length of outgoing_queue
const BLOCK_SIZE = 4096  // Number of bytes per websocket message
const SAMPLE_RATE = 12000
const CHANNELS = 1  // Audio recording channels
const DEVICE = "default"

var btArray = new Float32Array(100);
var pos = 0;

function connect() {
    const SELECTOR = document.getElementById("select_client")
    let connection_url = `ws://localhost:8000/stream/${SELECTOR.value}`
    let socket = new WebSocket(connection_url);
    socket.onopen = function(e) {
        alert(`[open] Connection established to: ${connection_url}`);
    };

    socket.onmessage = function(event) {
        if (pos < 100) {
            var reader = new FileReader();
            reader.readAsArrayBuffer(event.data);
            reader.addEventListener("loadend", function(e)
            {
                playByteArray(new Float32Array(e.target.result));  // arraybuffer object
            });
        }
    };
}




// Stereo
// Create an empty two second stereo buffer at the
// sample rate of the AudioContext
var audioCtx = new (window.AudioContext || window.webkitAudioContext)();

var myArrayBuffer = audioCtx.createBuffer(CHANNELS, BLOCK_SIZE, SAMPLE_RATE);

function playByteArray(btArray) {
    const nowBuffering = myArrayBuffer.getChannelData(0);
    for (let i = 0; i < myArrayBuffer.length; i++) {
        // Math.random() is in [0; 1.0]
        // audio needs to be in [-1.0; 1.0]
        nowBuffering[i] = btArray[i];
    }

  // Get an AudioBufferSourceNode.
  // This is the AudioNode to use when we want to play an AudioBuffer
  var source = audioCtx.createBufferSource();

  // set the buffer in the AudioBufferSourceNode
  source.buffer = myArrayBuffer;

  // connect the AudioBufferSourceNode to the
  // destination so we can hear the sound
  source.connect(audioCtx.destination);

  // start the source playing
  source.start();

}
