from flask import render_template, flash, request, Flask, redirect, url_for, send_from_directory
from app import app, models, db, admin
from .forms import LoginForm, RegisterForm, PostForm, ProfileForm
from flask_admin.contrib.sqla import ModelView
from flask_login import login_required, LoginManager, login_user, logout_user, current_user
from flask_bcrypt import Bcrypt
from .models import User, Post, Like, Follower
from werkzeug.utils import secure_filename
import logging

# Info Logger
logging.basicConfig(filename = 'info.log', level=logging.INFO, format = f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

# File Upload
UPLOAD_FOLDER_POST = 'app/static/posts/'
UPLOAD_FOLDER_USER = 'app/static/users/'

# Jijna do
app.jinja_env.add_extension('jinja2.ext.do')

# Bcrypt
bcrypt = Bcrypt(app)

# Admin
admin.add_view(ModelView(models.User, db.session))
admin.add_view(ModelView(models.Post, db.session))
admin.add_view(ModelView(models.Like, db.session))
admin.add_view(ModelView(models.Follower, db.session))

# Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    app.logger.info("user " + str(current_user) + " logged out")
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = User(username=form.username.data, password=hashed_password, profile_img="static/default.png", bio="")
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        app.logger.info("user " + str(current_user) + " registered")
        return redirect(url_for('home'))

    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            app.logger.info("user " + str(current_user) + " logged in")
            return redirect(url_for('home'))
        else:
            app.logger.info("user " + str(user) + " failed to log in")

    return render_template('login.html', title='Login', form=form)

@app.route('/<user>', methods=['GET', 'POST'])
@login_required
def profile(user):
    user = User.query.filter_by(username=user).first()
    post = Post.query.filter_by(user=user).first()
    following = Follower.query.filter_by(followed=user, follower=current_user).first()
    return render_template('profile.html', user=user, post=post, following=following, title=str(user) + ' - Profile')

@app.route('/<user>/posts', methods=['GET', 'POST'])
@login_required
def profile_posts(user):
    posts = Post.query.filter_by(op=user).order_by(Post.date_created)
    return render_template('home.html', posts=posts, title=str(user) + ' - Posts')


@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    posts = Post.query.order_by(Post.date_created)
    return render_template('home.html', posts=posts, title='Home')

@app.route('/like/<int:post>', methods=['GET', 'POST'])
@login_required
def like(post):
    post = Post.query.filter(Post.id == post).first()
    like_filter = Like.query.filter(Like.user == current_user and Like.post_id == post.id).first()
    if like_filter == None:
        new_like = Like(post_id=post.id, user=current_user)
        db.session.add(new_like)
        post.no_of_likes += 1
        db.session.commit()
    else:
        db.session.delete(like_filter)
        post.no_of_likes -= 1
        db.session.commit()

    return redirect(url_for('home'))

@app.route('/follow/<user>', methods=['GET', 'POST'])
@login_required
def follow(user):
    user = User.query.filter(User.username == user).first()

    if (user == current_user):
        return redirect(url_for('profile', user=user))
        
    follow_filter = Follower.query.filter(Follower.follower == current_user and Follower.followed == user).first()
    if follow_filter == None:
        new_follow = Follower(follower=current_user, followed=user)
        db.session.add(new_follow)
        user.no_of_followers += 1
        current_user.no_of_followed += 1
        db.session.commit()
    else:
        db.session.delete(follow_filter)
        user.no_of_followers -= 1
        current_user.no_of_followed -= 1
        db.session.commit()

    return redirect(url_for('profile', user=user))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/post', methods=['GET', 'POST'])
@login_required
def post():
    form = PostForm()

    if form.validate_on_submit():
        if form.file.data:
            filename = secure_filename(form.file.data.filename)
            form.file.data.save(UPLOAD_FOLDER_POST + filename)
            new_post = Post(title=form.title.data, text=form.text.data, user=current_user, image='/static/posts/' + filename)
        else:
            new_post = Post(title=form.title.data, text=form.text.data, user=current_user)

        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('home'))

    return render_template("create_post.html", form=form, title='Create Post')

@app.route('/edit', methods=['GET', 'POST'])
@login_required
def profile_edit():
    form = ProfileForm()
    if form.validate_on_submit():
        print(form.title.data + "YEAHAHHASH")
        if form.title.data:
            current_user.title = form.title.data

        if form.bio.data:
            current_user.bio = form.bio.data

        if form.old_password.data and form.password.data:
            if bcrypt.check_password_hash(current_user.password, form.old_password.data):
                hashed_password = bcrypt.generate_password_hash(form.old_password.data).decode('utf-8')
                current_user.password = hashed_password

        if form.file.data:
            filename = secure_filename(form.file.data.filename)
            form.file.data.save(UPLOAD_FOLDER_USER + filename)
            current_user.profile_img = '/static/users/' + filename

        db.session.commit()

        return redirect(url_for('profile', user=current_user))

    return render_template("edit_profile.html", form=form, title=str(current_user) + "- Edit Profile")