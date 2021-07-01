from flask import Blueprint
from flask import render_template, flash, redirect, request
from flask_session import Session
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.utils import secure_filename
from extensions import db, login_manager
import time

from .parser import Parser
from .sockets import *
from .models import *

app = Blueprint('text-synth', __name__, template_folder='templates')
ALLOWED_EXTENSIONS = {'wav', 'ogg', 'mp3', 'm4a'}

LANGUAGES = [
    # 'en',
    'fa'
    #,'ar'
]

parser = Parser(LANGUAGES)

@app.route('/')
def index():
    #TODO: check if logged in
    # db.drop_all()
    # db.metadata.clear()
    # create_test_db()
    user = authenticate_user('ben@example.com', 'test')
    login_user(user)
    if current_user.is_authenticated:
        return dashboard()
    else:
        return redirect('/login')

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
                start_time = time.time()
                filecontents = parser.parse_file(file, language)
                elapsed_time = time.time() - start_time
                print(f'File transcribed in {elapsed_time} seconds')
                # store text to send to result page
                entries.append({"filename" : filename, "filecontents" : filecontents})

        return render_template('result.html', entries=entries)
    return render_template('upload.html', languages=LANGUAGES)

# check if file has valid extension
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def dashboard():
    '''Render the dashboard for a logged in user'''
    print(f'logged in as: {current_user}')
    files = get_user_files(current_user.id)
    file_list = []
    for f in files:
        print(f'file {f.file_id}: {str(f)}')
        file_list.append({'date': f.date,
                          'name': f.name,
                          'status': f.status.name,
                          'language': f.language.name,
                          'text': f.text
        })

    return render_template('dashboard.html', username=current_user.name, entries=file_list)

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/register')
def register_page():
    return render_template('register.html')

@app.route('/recover')
def recover_page():
    return render_template('password.html')