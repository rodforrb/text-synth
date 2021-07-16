$(document).ready(function() {
  var socket = io.connect();

  socket.on("progress", function(raw) {
    const data = JSON.parse(raw);
    if(data.size > 0) {
      Array.prototype.forEach.call(data.updates, entry => {
        var entry_id = "status_" + String(entry.file_id);
        var percent = String(entry.percent)
        if (percent == 100) {
          percent = 'Complete';
        } else {
          percent += '%';
        }
        document.getElementById(entry_id).innerText = percent;
      });
    }
  });
  
  socket.on("complete", function(data) {
    console.log(data);
    var entry_id = "status_" + String(data.file_id);
    document.getElementById(entry_id).innerText = 'Complete';
  });

  function getText(entry_id) {
    // get modal holding text
    var modal = document.getElementById(entry_id);
    const text = modal.querySelector('.text').innerText;
    return text;
  }

  setInterval(function() {
    socket.emit('update');
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
