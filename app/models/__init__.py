# Following the flask recomendations in https://flask.palletsprojects.com/en/1.1.x/patterns/appfactories/ the
# db object is declared here, imported and used in the application __init__.py file.

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
