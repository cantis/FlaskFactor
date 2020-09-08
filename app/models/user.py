from flask_login import UserMixin
from sqlalchemy import Column, String
from sqlalchemy.sql.sqltypes import Unicode

from app.models import db


class User(db.Model, UserMixin):
    """ Data model for user accounts. """
    __tablename__ = 'users'
    user_id = Column(Unicode(35), primary_key=True)
    password = Column(String(32), index=False)
    firstname = Column(String(20))
    lastname = Column(String(20))
    extend_existing = True

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.user_id
