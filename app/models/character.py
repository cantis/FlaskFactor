from sqlalchemy import Column, Integer, ForeignKey, String, Boolean

from app.models import db


class Character(db.Model):
    """ Data Model for Character """
    __tablename__ = 'characters'
    id = Column(Integer, primary_key=True)
    character_name = Column(String, nullable=False)
    character_class = Column(String)
    is_active = Column(Boolean, default=True)
    is_dead = Column(Boolean, default=False)
    player_id = Column(Integer, ForeignKey('players.id'))
    party_id = Column(Integer, ForeignKey('parties.id'))
