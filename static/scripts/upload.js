
$(document).ready(function() {

  // sending a connect request to the server.
  var socket = io.connect('127.0.0.1:5000');

  socket.on("progress", function(data) {
    console.log(data);
  });

  socket.on("complete", function(data) {
    
  });

});