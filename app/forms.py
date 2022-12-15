from flask_wtf import FlaskForm
from wtforms import IntegerField, PasswordField, StringField, SubmitField, TextAreaField
from flask_wtf.file import FileField
from wtforms.validators import InputRequired, Length, ValidationError

class RegisterForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=4)])

    submit = SubmitField("Register")

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired()])
    password = PasswordField('password', validators=[InputRequired()])

class PostForm(FlaskForm):
    title =  StringField('title', validators=[InputRequired()])
    text = TextAreaField('text')
    file = FileField()

class ProfileForm(FlaskForm):
    title = StringField('title')
    bio = TextAreaField('bio')
    file = FileField()
    old_password = PasswordField('old_password')
    password = PasswordField('password')