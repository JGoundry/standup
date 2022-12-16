from app import app, db
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy import MetaData

meta = MetaData()

followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    profile_img = db.Column(db.String(), nullable=True)
    title = db.Column(db.String(50), nullable=True)
    bio = db.Column(db.String(150), nullable=True)
    posts = db.relationship('Post', backref='user', lazy='dynamic')

    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    def followers_count(self):
        statement = followers.select().where(followers.c.followed_id == self.id)
        count = len(db.engine.execute(statement).all())
        return count
        
    def following_count(self):
        return self.followed.count()

    def __repr__(self):
        return str(self.username)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    op = db.Column(db.String(50), db.ForeignKey('user.username'))
    title = db.Column(db.String(100))
    text = db.Column(db.String(500))
    image = db.Column(db.String(), nullable=True)
    date_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    __tablename__ = 'post'

    def like_count(self):
        return Like.query.filter(Like.post_id==self.id).count()

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

with app.app_context():
    db.create_all()