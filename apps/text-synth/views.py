from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request
from flask_socketio import SocketIO, emit
from flask_session import Session
from extensions import io

import json
import os
from io import BytesIO
from werkzeug.utils import secure_filename

from .parser import Parser

app = Blueprint('text-synth', __name__, template_folder='templates')
ALLOWED_EXTENSIONS = {'wav'}
LANGUAGES = ['en', 'fa']

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
        # verify a language is submitted
        if 'language' not in request.values.keys():
            flash('No language selected')
            return redirect(request.url)
        # verify a valid language is passed
        if request.values['language'] not in LANGUAGES:
            flash('No language selected')
            return redirect(request.url)
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        language = request.values['language']
        # grab list of files
        files = request.files.getlist('file')
        # list of {filename, text} objects for result page
        entries = []
        for file in files:
            # if user does not select any file
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            # if file is valid, parse file
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # synthesize text from audio file
                filecontents = parser.parse_file(file, language)
                # store text to send to result page
                entries.append({"filename" : filename, "filecontents" : filecontents})

        return render_template('result.html', entries=entries)
    return render_template('upload.html')

@io.on('connect')
def test_connect():
    print('Connected!')
    stream.flush()

@io.on('Audio sent')
def data_received(data):
    stream.write(data['data'])

@io.on('stop')
def stop_recording():
    result = parser.parse_audio(stream)
    emit('Text received', result)

# check if file has valid extension
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS