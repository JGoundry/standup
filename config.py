import os

# Enables Cross-Site Request Forgery prevention
WTF_CSRF_ENABLED = True
SECRET_KEY = 'lovelace'

# Tells SQLite where to put the database file
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = True