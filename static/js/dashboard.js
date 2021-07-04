$(document).ready(function() {
    var socket = io.connect();

    socket.on("progress", function(data) {
        console.log(data);
      });
    
      socket.on("complete", function(data) {
        console.log(data);
      });




    function getText(entry_id) {
        // get modal holding text
        var modal = document.getElementById(entry_id);
        const text = modal.querySelector('.text').innerText;
        return text;
    }

    const download = function(filename, entry_id) {
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
