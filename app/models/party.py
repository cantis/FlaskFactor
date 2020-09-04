from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from app.models import db


class Party(db.Model):
    """ Data mode for an adventuring Party

    :param int id: Party Identity
    :param string party_name: Name of the party
    :param list characters: list of party Characters - not implimented

     """
    __tablename__ = 'parties'
    id = Column(Integer, primary_key=True)
    party_name = Column(String(50), nullable=False)
    is_active = Column(Boolean)
    characters = relationship('Character', backref='party')
