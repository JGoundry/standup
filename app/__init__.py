from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
from flask_bcrypt import Bcrypt
from flask_basicauth import BasicAuth

# App Setup
app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Flask Migrate
migrate = Migrate(app, db, render_as_batch=True)

# Flask Admin
admin = Admin(app, template_mode='bootstrap4')

# Basic Auth
app.config['BASIC_AUTH_USERNAME'] = 'admin'
app.config['BASIC_AUTH_PASSWORD'] = 'admin'
app.config['BASIC_AUTH_FORCE'] = True
basic_auth = BasicAuth(app)


from app import views, models
