from secrets import token_urlsafe
import os
basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
class ProjectDevelopmentConfig():
    SQLITE_DB_DIR = basedir
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(SQLITE_DB_DIR,'database','projectDB.db')
    DEBUG = False
    SECRET_KEY = token_urlsafe()
    UPLOAD_FOLDER = 'static/uploads'
