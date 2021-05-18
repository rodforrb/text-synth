 
$(document).ready(function() {
         
  // sending a connect request to the server.
  var socket = io.connect('127.0.0.1:5000');
 
  // handler for receiving text from server
  socket.on('Text received', function(data) {
      var output_fa = document.getElementById('output_fa')
      output_fa.textContent = data;
      copyText();
  });

  // copy the current text to the clipboard
  function copyText() {

    output_fa.focus();
    output_fa.select();
    document.execCommand('copy');

    document.getElementById('rec').focus();
  }
  
  // recording toggle button
  const recButton = document.getElementById('rec');
  var recording = false;

  // setup upon acquiring microphone permission
  const handleSuccess = function(stream) {
    const options = {
      mimeType: 'audio/webm',
      audioBitsPerSecond: 16000
    };

    const mediaRecorder = new MediaRecorder(stream, options);
    var recordedChunks = [];

    // send chunks of data to server when available
    mediaRecorder.addEventListener('dataavailable', function(e) {
      if (e.data.size > 0) {
        // mediaRecorder.stop();
        // recordedChunks.push(e);
        // console.log(mediaRecorder.requestData());
        socket.emit("Audio sent", {data: e.data});
        // mediaRecorder.start();

      }
    });
    
    // signal server when stopped
    mediaRecorder.addEventListener('stop', function() {
      socket.emit("stop")
    });

    // toggle button for start/stop
    recButton.addEventListener('click', function() {
      // pressed stop button
      if (recording) {
        recording = false;
        mediaRecorder.stop();
        recButton.textContent = "Start";
      } else {
        // pressed start button
        recording = true;
        recordedChunks = [];
        mediaRecorder.start(1000);
        recButton.textContent = "Stop";
      }
    });
  };

  // acquire microphone permission
  navigator.mediaDevices.getUserMedia({ audio: true, video: false })
    .then(handleSuccess);
  
  
  // // handle language radiobuttons
  // const btn_fa = document.getElementById('btn_fa');
  // const btn_en = document.getElementById('btn_en');

  // btn_fa.checked = true;
  
  // btn_fa.onclick =  function() {
  //   socket.emit('language selected', {lang: 'fa'})
  // };

  // btn_en.onclick = function() {
  //   socket.emit('language selected', {lang: 'en'})
  // };

});