from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin

# App Setup
app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

# Flask Migrate
migrate = Migrate(app, db, render_as_batch=True)

# Flask Admion
admin = Admin(app, template_mode='bootstrap4')

from app import views, models

