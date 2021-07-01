from extensions import db
from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import enum
import datetime

class Status(enum.Enum):
    submitted = 0
    active = 1
    complete = 2

class User(db.Model, UserMixin):
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
    status = db.Column(db.Enum(Status), default=Status.submitted)
    text = db.Column(db.Text)

def create_test_db():
    try:
        db.create_all()
        u = User(name="bentest", email="ben@example.com")
        u.password = "test"
        db.session.add(u)

        f1 = File(user_id=1, name='filename1')
        f2 = File(user_id=1, name='filename2')
        db.session.add(f1)
        db.session.add(f2)

        db.session.commit()
    except:
        print('test db already exists')
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