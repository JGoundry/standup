from flask_wtf import FlaskForm
from wtforms import IntegerField, PasswordField, StringField, SubmitField
from wtforms.validators import InputRequired, Length

# class RegisterForm(FlaskForm):
#     username = StringField('username', validators=[InputRequired(), Length(min=4, max=20)])
#     password = PasswordField('password', validators=[InputRequired(), Length(min=4)])

#     submit = SubmitField("Register")

#     def validate_username(self, username):
#         existing_user_username = User.query.fileter_by

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired()])
    password = PasswordField('password', validators=[InputRequired()])