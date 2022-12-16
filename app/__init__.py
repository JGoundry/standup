from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
from flask_bcrypt import Bcrypt

# App Setup
app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Flask Migrate
migrate = Migrate(app, db, render_as_batch=True)

# Flask Admin
admin = Admin(app, template_mode='bootstrap4')

from app import views, models

# import logging
# logging.basicConfig(level=logging.DEBUG)
