from app import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(64), nullable=False)
    profile_img = db.Column(db.String(), nullable=True)
    bio = db.Column(db.String(150), nullable=True)
    posts = db.relationship('Post', backref='user', lazy='dynamic')
    __tablename__ = 'user'

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    op = db.Column(db.String(50), db.ForeignKey('user.username'))
    caption = db.Column(db.String(500))
    no_of_likes = (db.Integer)
    __tablename__ = 'post'

