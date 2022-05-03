from flask_login import UserMixin
from sqlalchemy import ForeignKey, Column, Integer, String, Boolean, Float, Numeric
from sqlalchemy.orm import relationship


from web import db, login_manager


class Character(db.Model):
    """Data Model for Character"""

    __tablename__ = 'characters'
    id = Column(Integer, primary_key=True)
    character_name = Column(String, nullable=False)
    character_class = Column(String)
    is_active = Column(Boolean, default=True)
    is_dead = Column(Boolean, default=False)
    player_id = Column(Integer, ForeignKey('players.id'))
    party_id = Column(Integer, ForeignKey('parties.id'))


class Item_Type(db.Model):
    """Data model for Treasure Item Types"""

    __tablename__ = 'item_types'
    id = Column(Integer, primary_key=True)
    item_type = Column(String, nullable=False)
    items = relationship('Item')


class Item(db.Model):
    """Data model for a Teasure Item"""

    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    level = Column(Integer)
    quantity = Column(Integer, nullable=False)
    purchase_price = Column(Float)
    item_type_id = Column(Integer, ForeignKey('item_types.id'))


class Party(db.Model):
    """Data mode for an adventuring Party"""

    __tablename__ = 'parties'
    id = Column(Integer, primary_key=True)
    party_name = Column(String(50), nullable=False)
    is_active = Column(Boolean)
    characters = relationship('Character', backref='party')


class Player(db.Model):
    """Data model for a player"""

    __tablename__ = 'players'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(40))
    last_name = Column(String(40))
    is_active = Column(Boolean)
    email = Column(String(100))
    characters = relationship('Character', backref='player')


class User(db.Model, UserMixin):
    """Data model for user accounts."""

    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(40))
    last_name = Column(String(40))
    email = Column(String(100), nullable=False)
    password = Column(String(300), index=False)
    is_active = Column(Boolean, default=True)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(id)


class Setting(db.Model):
    '''Data Model for an Application Setting'''

    __tablename__ = 'settings'
    id = Column(Integer, primary_key=True)
    party_id = Column(Integer, ForeignKey('parties.id'))
    name = Column(String(50), nullable=False)
    value = Column(String(100), nullable=False)


class Receiving(db.Model):
    '''Data model for receiving items from adventurers'''

    __tablename__ = 'receiving'
    id = Column(Integer, primary_key=True)  # Receiving ID, unique identifier
    receipt_id = Column(Integer)  # Receipt ID, the batch number of this receipt
    session_id = Column(Integer)  # Session ID, the session number for the item
    party_id = Column(Integer, ForeignKey('parties.id'))
    Item_Type_id = Column(Integer, ForeignKey('item_types.id'))
    quantity = Column(Integer, nullable=False)
    isCommitted = Column(Boolean, default=False)  # player this item is committed to
    item = Column(String(50), nullable=False)  # Item Description
    purchase_price = Column(Numeric, nullable=False)


def init_db():
    db.create_all()
