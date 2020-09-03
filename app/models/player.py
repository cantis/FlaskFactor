from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from app.models import db


class Player(db.Model):
    """ Data model for a player

    :param int id: Player Identity
    :param string firstname: Firstname
    :param string lastname: Lastname
    :param list characters: List of Characters - not implimented
    :param list parties: List of Parties for Player - not implimented

    """
    __tablename__ = 'players'
    id = Column(Integer, primary_key=True)
    firstname = Column(String(20))
    lastname = Column(String(20))
    is_active = Column(Boolean)
    characters = relationship('Character', backref='player')
