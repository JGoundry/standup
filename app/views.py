from flask import render_template, flash, request, Flask, redirect, url_for
from app import app, models, db, admin
from .forms import LoginForm
from flask_admin.contrib.sqla import ModelView
from flask_login import login_required, LoginManager, login_user, logout_user, current_user
from flask_bcrypt import Bcrypt
from .models import User, Post, Like

# Jijna do
app.jinja_env.add_extension('jinja2.ext.do')

# Bcrypt
bcrypt = Bcrypt(app)

# Admin
admin.add_view(ModelView(models.User, db.session))
admin.add_view(ModelView(models.Post, db.session))
admin.add_view(ModelView(models.Like, db.session))

# Login Manager: try put in init
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = LoginForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', title='Create Account', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('home'))

    return render_template('login.html', title='Login', form=form)

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    return render_template('profile.html', title=current_user.username + ' - Profile')

@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    posts = Post.query.order_by(Post.date_created.desc())
    return render_template('home.html', posts=posts)


@app.route('/like/<int:post>/', methods=['GET', 'POST'])
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

