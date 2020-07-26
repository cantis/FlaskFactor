from sqlalchemy import Column, Integer, ForeignKey, String, Boolean

from app.models import db
from app.models.user import User


class Character(db.Model):
    """ Data Model for Character """
    __tablename__ = 'characters'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id))
    character_name = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
