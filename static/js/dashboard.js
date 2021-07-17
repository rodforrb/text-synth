$(document).ready(function() {
  var socket = io.connect();

  var waiting = true;
  var refreshTimer;

  socket.on("progress", function(raw) {
    clearTimeout(refreshTimer);
    waiting = false;

    const data = JSON.parse(raw);
    if(data.size > 0) {
      Array.prototype.forEach.call(data.updates, entry => {
        var id = String(entry.file_id);
        var entry_id = "status_" + id;
        var text_id = "text_" + id;

        var percent = String(entry.percent);
        var text = entry.text;

        document.getElementById(entry_id).innerText = percent;
        document.getElementById(text_id).innerText = text;
      });
    } else {
      // stop calling for updates when no files to update
      clearInterval(statusUpdater);
    }
  });

  function getText(entry_id) {
    // get modal holding text
    var modal = document.getElementById(entry_id);
    const text = modal.querySelector('.text').innerText;
    return text;
  }

  var statusUpdater = setInterval(function() {
    socket.emit('update');
    // if not exists, create a timeout to refresh the page if the socket is not responding to update requests
    if (!waiting) {
      refreshTimer = setTimeout(function() {
        socket = io.connect();
      }, 3000);
      waiting = true;
    }

  }, 2000);
  
  // global scope function for onclick download button
  download = function(filename, entry_id) {
    // get text for file
    const text = getText(entry_id);

    // create output textfile name
    const txt_filename = filename.split('.').slice(0, -1).join('.') + ".txt";
    // set up download element
    var element = document.createElement('a');
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
    element.setAttribute('download', txt_filename);
    element.style.display = 'none';

    // trigger download
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
  };
});
