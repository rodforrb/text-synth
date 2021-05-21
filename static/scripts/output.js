/*  Dynamically creates the file outputs for result.html.
    The page is pre-filled with the text output. This script then attaches
    the 'save' button for each file result to a function todownload a text
    file with its contents.
*/
$(document).ready(function() {

  // iterate each entry element to attach download button
  var entries = document.getElementsByClassName("file-result");
  for (let entry of entries) {

    // attach function to download button
    var downloadButton = entry.querySelector(".save");
    downloadButton.onclick = function () {
          // get input filename
          const in_filename = entry.querySelector(".filename").innerText;
          // create output textfile name
          const txt_filename = in_filename.split('.').slice(0, -1).join('.') + ".txt";
          // get output text from entry
          const text = entry.querySelector(".filecontents").innerText;

          // set up download element
          var element = document.createElement('a');
          element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
          element.setAttribute('download', txt_filename);
          element.style.display = 'none';

          // trigger download
          document.body.appendChild(element);
          element.click();
          document.body.removeChild(element);
        }
    }
});