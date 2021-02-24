from flask_login import UserMixin
from sqlalchemy import ForeignKey, Column, Integer, String, Boolean, Float
from sqlalchemy.orm import relationship


from web import db, login_manager


class Character(db.Model):
    """ db Model for Character """
    __tablename__ = 'characters'
    id = Column(Integer, primary_key=True)
    character_name = Column(String, nullable=False)
    character_class = Column(String)
    is_active = Column(Boolean, default=True)
    is_dead = Column(Boolean, default=False)
    player_id = Column(Integer, ForeignKey('players.id'))
    party_id = Column(Integer, ForeignKey('parties.id'))


class Item_Type(db.Model):
    """ db model for Treasure Item Types """
    __tablename__ = 'item_types'
    id = Column(Integer, primary_key=True)
    item_type = Column(String, nullable=False)
    items = relationship('Item')


class Item(db.Model):
    """ db model for a Teasure Item """
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    level = Column(Integer)
    quantity = Column(Integer, nullable=False)
    purchase_price = Column(Float)
    item_type_id = Column(Integer, ForeignKey('item_types.id'))


class Party(db.Model):
    """ Data mode for an adventuring Party """
    __tablename__ = 'parties'
    id = Column(Integer, primary_key=True)
    party_name = Column(String(50), nullable=False)
    is_active = Column(Boolean)
    characters = relationship('Character', backref='party')


class Player(db.Model):
    """ Data model for a player """
    __tablename__ = 'players'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(20))
    last_name = Column(String(20))
    is_active = Column(Boolean)
    characters = relationship('Character', backref='player')


class User(db.Model, UserMixin):
    """ Data model for user accounts. """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(40))
    last_name = Column(String(40))
    email = Column(String(100), nullable=False)
    password = Column(String(20), index=False)
    extend_existing = True

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(id)


def init_db():
    db.create_all()
