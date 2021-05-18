# keep this file even if you don't need traditional views
# as it holds the blueprint app instance
from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request
from flask_socketio import SocketIO, emit
from flask_session import Session
from extensions import io
app = Blueprint('text-synth', __name__, template_folder='templates')


from vosk import Model, KaldiRecognizer
import sys
import json
import os
import subprocess
import queue
from io import BytesIO
from werkzeug.utils import secure_filename


APP_ROOT = os.path.dirname(os.path.realpath(__file__))
ALLOWED_EXTENSIONS = {'wav'}


stream = BytesIO()

# language models
model_fa = Model(APP_ROOT + "/models/model-fa")
rec = KaldiRecognizer(model_fa, 16000)

@app.route('/')
def index():
    return redirect('/upload')

@app.route('/record')
def record():
    return render_template('record.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        # grab list of files
        files = request.files.getlist('file')

        # list of {filename, text} objects for output page
        entries = []

        for file in files:
            # if user does not select any file
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)

            # if file is valid
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)

                # synthesize text from audio file
                filecontents = parse_file(file)

                entries.append({"filename" : filename, "filecontents" : filecontents})
        return render_template('result.html', entries=entries)

    return render_template('upload.html')


@io.on('connect')
def test_connect():
    print('Connected!')
    stream.flush()


@io.on('Audio sent')
def data_received(data):
    nBytes = stream.write(data['data'])

@io.on('stop')
def stop_recording():
    print("Stopped")
    parse_audio()

@io.on('language selected')
def lang_select(data):
    global rec
    if (data['lang'] == 'fa'):
        rec = rec_fa
    elif (data['lang'] == 'en'):
        # rec = rec_en
        pass


# check if file has valid extension
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# parse microphone audio from input stream
def parse_audio():
    stream.seek(0)
    process = subprocess.Popen(['ffmpeg', '-loglevel', 'quiet',
                                '-i', '-',
                                '-ar', "16000", '-ac', '1', '-f', 's16le', '-'],
                               stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE)

    p_out, err = process.communicate(input=stream.getvalue(), timeout=None)

    data_bytes = BytesIO(p_out)

    while True:
        data = data_bytes.read(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            print(rec.Result())
        else:
            print(rec.PartialResult())
        # emit('Text received', res['text'])

    res = json.loads(rec.FinalResult())

    emit('Text received', res['text'])

    stream.flush()

# parse audio file from upload
def parse_file(file_in):
    file_data = file_in.read()

    process = subprocess.Popen(['ffmpeg', '-loglevel', 'quiet',
                                '-i', '-',
                                '-ar', "16000", '-ac', '1', '-f', 's16le', '-'],
                               stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE)

    p_out, err = process.communicate(input=file_data, timeout=None)

    data_bytes = BytesIO(p_out)

    while True:
        data = data_bytes.read(4000)
        if len(data) == 0:
            break
        rec.AcceptWaveform(data)

    res = json.loads(rec.FinalResult())

    return res['text']
