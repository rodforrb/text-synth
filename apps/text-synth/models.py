from extensions import db, login_manager
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import enum
import datetime

UPLOAD_FOLDER = 'upload/'

class Status(enum.Enum):
    Submitted = 0
    Parsing = 1
    Complete = 2

class Language(enum.Enum):
    English = 0
    Farsi = 1
    Arabic = 2

lang_to_enum = {'en': Language.English,
                'fa': Language.Farsi,
                'ar': Language.Arabic
}


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(40), nullable=False, unique=True)
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('Reading password not allowed')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class File(db.Model):
    file_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    status = db.Column(db.Enum(Status), default=Status.Submitted)
    language = db.Column(db.Enum(Language), nullable=False)
    text = db.Column(db.Text)

def create_test_db():
    try:
        db.create_all()
        u = User(name="bentest", email="ben@example.com")
        u.password = "test"
        db.session.add(u)


        db.session.commit()
    except Exception as e:
        print('test db already exists')
        db.session.rollback()

    try:
        f1 = File(user_id=1, name='filename1', language=Language.English)
        f2 = File(user_id=1, name='filename2', language=Language.English)
        db.session.add(f1)
        db.session.add(f2)
        db.session.commit()
    except Exception as e:
        print('files already exist')
        db.session.rollback()

def authenticate_user(useremail, password):
    u = User.query.filter_by(email=useremail).first()
    if u.check_password(password):
        return u
    else:
        print('incorrect password')
        return None

def get_user_files(user_id):
    files = File.query.filter_by(user_id=user_id).all()
    return files
    
@login_manager.user_loader
def load_user(userid):
    return User.query.filter_by(id=userid).first()


def save_file(user_id, file, lang_code):
    '''
    Save a given file to disk with given user id and language
    Return the file_id of the stored file
    '''
    language = lang_to_enum[lang_code]

    try:
        # save file info to database
        fileinfo = File(user_id=user_id, name=file.filename, language=language)
        db.session.add(fileinfo)
        db.session.commit()
        file_id = fileinfo.file_id

        # save file contents to disk
        file.save(UPLOAD_FOLDER + str(file_id))
        # with open(UPLOAD_FOLDER + str(file_id), 'wb') as fileout:
        #     fileout.write(file)
        return file_id

    except Exception:
        db.session.rollback()
        raise

def load_file(file_id):
    '''
    Load a file from disk given its file id
    Return the File object and language
    '''

    filecontents = ''
    language = None
    
    with open(UPLOAD_FOLDER + str(file_id), 'rb') as filein:
        filecontents = filein.read()

    file = File.query.filter_by(file_id=file_id).first()
    language = file.language

    try:
        file.status = Status.Parsing
        db.session.commit()
    except:
        db.session.rollback()
        raise

    return filecontents, language

def update_text(file_id, text):
    '''Update the text field for a given file id'''
    try:
        file = File.query.filter_by(file_id=file_id).first()
        file.text = text
        file.status = Status.Complete
        db.session.commit()
    except:
        db.session.rollback()
        raise