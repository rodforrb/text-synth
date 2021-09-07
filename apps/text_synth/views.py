from flask import Blueprint, current_app
from flask import render_template, flash, redirect, request
from flask_session import Session
from flask_login import current_user, login_required, login_user, logout_user
from extensions import db, login_manager
from datetime import datetime
import time

from .parser import Parser
from .sockets import *
from .models import *
from .filehandler import FileHandler, queue_task

app = Blueprint('text_synth', __name__, template_folder='templates')
ALLOWED_EXTENSIONS = {'wav', 'ogg', 'mp3', 'm4a', 'amr'}

filequeue = FileHandler()

LANGUAGES = [
    'en',
    'fa'
    #,'ar'
]

@app.before_app_first_request
def app_final_setup():
    create_test_db()

@app.route('/', methods=['GET', 'POST'])
def index():
    '''Decide and render action for home page'''
    # Dashboard page if logged in
    if current_user.is_authenticated:
        if request.method == 'POST':
            # Submit new file(s) and refresh
            dashboard_post()
            return redirect('/')
        return dashboard()

    # User is not logged in
    else:
        return redirect('/login')

def dashboard_post():
    '''Process dashboard actions from POST request'''
    if request.method == 'POST':
        # if user deletes a file
        if 'delete' in request.values.keys():
            if not current_user.is_authenticated:
                return redirect('/login')
            file_id = request.values['delete']
            delete_file(file_id)
            return dashboard()
        # else process file upload
        upload()
        

def upload():
    '''Verify and process file upload'''
    # verify a language is submitted
    if 'language' not in request.values.keys():
        flash('No language selected')
        return redirect(request.url)
    # verify the language is valid
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
    for file in files:
        # if user does not select any file
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        # if file is valid, send file for parsing
        if file and allowed_file(file.filename):
            # file handler requires app context for database use
            if filequeue.appcontext == None:
                filequeue.set_app_context(current_app.app_context())
            # enqueue valid file
            id = filequeue.put(file, language)

            queue_task(id)

def allowed_file(filename):
    '''Check if file has valid extension'''
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def dashboard():
    '''Render the dashboard for a logged in user'''
    if not current_user.is_authenticated:
        # in case method is somehow called when not logged in
        return redirect('/login')

    # collect and format user's files
    files = get_user_files(current_user.id)
    file_list = []
    for f in files:
        file_list.append({'id': f.file_id,
                          'date': f.date.strftime('%Y-%m-%d %H:%M'),
                          'name': f.name,
                          'status': f.status.name,
                          'language': f.language.name,
                          'text': f.text
        })

    return render_template('dashboard.html', username=current_user.name, entries=file_list)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        if 'inputEmail' in request.values.keys() and 'inputPassword' in request.values.keys():
            email = request.values['inputEmail']
            password = request.values['inputPassword']
            return login_attempt(email, password)
    return render_template('login.html')

@app.route('/register')
def register_page():
    return render_template('register.html')

@app.route('/recover')
def recover_page():
    return render_template('password.html')

def login_attempt(email, password):
    user = authenticate_user(email, password)
    if user is not None:
        login_user(user)
        return redirect('/')
    else:
        # incorrect login
        return redirect('/login')

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')
