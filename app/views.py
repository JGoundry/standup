from flask import render_template, flash, request, Flask, redirect, url_for
from app import app, models, db, admin
from .forms import LoginForm
from flask_admin.contrib.sqla import ModelView
from flask_login import login_required, LoginManager, login_user, logout_user, current_user
from flask_bcrypt import Bcrypt
from .models import User

# Bcrypt
bcrypt = Bcrypt(app)

# Admin
admin.add_view(ModelView(models.User, db.session))
admin.add_view(ModelView(models.Post, db.session))

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
@app.route('/home')
@login_required
def home():
    return render_template('home.html')


