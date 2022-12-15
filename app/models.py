from app import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    profile_img = db.Column(db.String(), nullable=True)
    title = db.Column(db.String(50), nullable=True)
    bio = db.Column(db.String(150), nullable=True)
    no_of_followers = db.Column(db.Integer, default=0)
    no_of_followed = db.Column(db.Integer, default=0)
    posts = db.relationship('Post', backref='user', lazy='dynamic')

    def __repr__(self):
        return str(self.username)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    op = db.Column(db.String(50), db.ForeignKey('user.username'))
    title = db.Column(db.String(100))
    text = db.Column(db.String(500))
    image = db.Column(db.String(), nullable=True)
    no_of_likes = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    __tablename__ = 'post'

    def __repr__(self):
        return str(self.user) + ' - ' + str(self.title)

class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('like', lazy='dynamic'), uselist=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    post = db.relationship('Post', backref=db.backref('like', lazy='dynamic'), uselist=False)
    __tablename__ = 'like'

    def __repr__(self):
        return str(self.user)

class Follower(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    follower = db.relationship('User', foreign_keys=[follower_id], uselist=False)
    followed_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    followed = db.relationship('User', foreign_keys=[followed_id], uselist=False)
    __tablename__ = 'follower'

    def __repr__(self):
        return str(self.followed)