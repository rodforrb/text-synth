from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request
from flask_socketio import SocketIO, emit
from flask_session import Session
from extensions import socketio

import json
import os
from io import BytesIO
from werkzeug.utils import secure_filename

from .parser import Parser

app = Blueprint('text-synth', __name__, template_folder='templates')
APP_ROOT = os.path.dirname(os.path.realpath(__file__))
ALLOWED_EXTENSIONS = {'wav'}


stream = BytesIO()

parser = Parser()

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
                filecontents = parser.parse_file(file)

                entries.append({"filename" : filename, "filecontents" : filecontents})
        return render_template('result.html', entries=entries)

    return render_template('upload.html')


@socketio.on('connect')
def test_connect():
    print('Connected!')
    stream.flush()


@socketio.on('Audio sent')
def data_received(data):
    nBytes = stream.write(data['data'])

@socketio.on('stop')
def stop_recording():
    print("Stopped")
    result = parser.parse_audio(stream)
    emit('Text received', result)

@socketio.on('language selected')
def lang_select(data):
    pass


# check if file has valid extension
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS