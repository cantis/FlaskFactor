from . import db


class User(db.Model):
    """ Data model for user account """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(20), index=False, unique=True, nullable=False)
    password = db.Column(db.String(32), index=False)
    firstname = db.Column(db.String(20))
    lastname = db.Column(db.String(20))
    characters = db.Relationship('Character')
