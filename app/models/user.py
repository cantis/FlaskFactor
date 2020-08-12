from sqlalchemy import Column, Integer, String

from app.models import db


class User(db.Model):
    """ Data model for user account """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(20), index=False, unique=True, nullable=False)
    password = Column(String(32), index=False)
    firstname = Column(String(20))
    lastname = Column(String(20))
