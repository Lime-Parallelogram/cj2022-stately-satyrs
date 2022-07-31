// Audio settings
const BUFFER_SIZE = 80  // Max length of outgoing_queue
const BLOCK_SIZE = 4096  // Number of bytes per websocket message
const SAMPLE_RATE = 12000
const CHANNELS = 1  // Audio recording channels

const SELECTOR = document.getElementById("select_client")

let jsonDATA = {}
var btArray = new Float32Array(100);
var pos = 0;

var audioCtx = new (window.AudioContext || window.webkitAudioContext)();
var myArrayBuffer = audioCtx.createBuffer(CHANNELS, BLOCK_SIZE, SAMPLE_RATE);

let initialSocket = new WebSocket(`ws://sjlcc.limeparallelogram.uk/data`);

initialSocket.onopen = function(event) {
    initialSocket.send("CLIENT LIST");
}

initialSocket.onmessage = function(event) {
    if (typeof(event.data) == "string") {
        let jsonDATA = JSON.parse(event.data)

        // If the data includes the users tag, add it to the option selector
        if (jsonDATA["users"]) {
            let dataDisplay = "<option value=''>-- select --</option>"
            let prevValue = SELECTOR.value
            jsonDATA["users"].forEach((name) => {
                console.log(jsonDATA["users"])
                dataDisplay += `<option value="${name}">${name}</option>`
            });
            SELECTOR.innerHTML = dataDisplay
            if (prevValue) { SELECTOR.value = prevValue } // Ensure that same value is selected after refresh

        } else {updateInfo(jsonDATA)} // Otherwise use the information to update the data
    }

};

// Runs when the user changes what is selected on the drop-down
function selectChanged(event) {
    if (event.target.value) {
        initialSocket.send('DATA:' + event.target.value)
    } else { // If no value is selected, clear info
        updateInfo("")
    }
}

// Update the information displayed about the client
function updateInfo(selectionData) {
    let dataDisplay = ""
    for (const key in selectionData) {
        dataDisplay += `<label for="${key}" class="col-sm-4 col-form-label fw-bold text-end">${key.toUpperCase()} :</label>
        <div class="col-sm-8">
            <input type="text" readonly class="form-control-plaintext" id="${key}" value="${selectionData[key]}">
        </div>`
    }
    document.getElementById("props_container").innerHTML = dataDisplay
}

// Called when connect button is clicked
function connect() {
    initialSocket.close()

    let connection_url = `ws://sjlcc.limeparallelogram.uk/listen/${SELECTOR.value}`
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

// Handle audio playback
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
