from flask_login import UserMixin
from sqlalchemy import Column, String
from sqlalchemy.sql.sqltypes import Unicode

from app.models import db


class User(db.Model, UserMixin):
    """ Data model for user accounts.
    :param str user_id: email address of user
    :param str password: user's password hash
    :param str firstname: user's first name
    :param str lastname: users's last name
    """
    __tablename__ = 'users'
    user_id = Column(Unicode(35), primary_key=True)
    password = Column(String(32), index=False)
    firstname = Column(String(20))
    lastname = Column(String(20))
    extend_existing = True


