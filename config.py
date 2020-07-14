"""Flask config."""
from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config:
    """ SET Flask config variables. """
    FLASK_APP = 'app.py'
    SECRET_KEY = environ.get('SECRET_KEY')

    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'

    # Database
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(Config):
    FLASK_ENV = 'development'
    FLASK_DEBUG = True
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = environ.get('DEV_DATABASE_URI')


class ProdConfig(Config):
    FLASK_ENV = 'production'
    TESTING = False
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = environ.get('PROD_DATABASE_URI')
