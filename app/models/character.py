from sqlalchemy import Column, Integer, ForeignKey, String, Boolean

from app.models import db
from app.models.user import User


class Character(db.Model):
    """ Data Model for Character
    :param int id: Character Identity
    :param int user_id: id of owning user - replace with player!
    :param string character_name: Character Name
    :param string character_class: Character Class
    :param boolean is_active: is the the character active?
    :param bookean is_dead: is the character dead?

     """
    __tablename__ = 'characters'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.user_id))
    character_name = Column(String, nullable=False)
    character_class = Column(String)
    is_active = Column(Boolean, default=True)
    is_dead = Column(Boolean, default=False)
