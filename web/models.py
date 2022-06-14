from decimal import Decimal
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
    first_name = Column(String(40))
    last_name = Column(String(40))
    is_active = Column(Boolean)
    email = Column(String(100))
    characters = relationship('Character', backref='player')


class User(db.Model, UserMixin):
    """ Data model for user accounts. """
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
    ''' Data Model for an Application Setting '''
    __tablename__ = 'settings'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    value = Column(String(100), nullable=False)


class Receiving_Header(db.Model):
    ''' Data Model for the Receiving Header '''
    __tablename__ = 'receiving_header'
    id = Column(Integer, primary_key=True)
    receiving_no = Column(Integer, nullable=False)  # batch number for this receiept
    receiving_date = Column(String(10), nullable=False)  # date of receipt (realtime)
    session_id = Column(Integer, nullable=False)  # session id for this receipt
    party_id = Column(Integer, ForeignKey('parties.id'))  # party id for this receipt
    is_closed = Column(Boolean, default=False)  # is this receipt closed?
    is_complete = Column(Boolean, default=False)  # is this receipt complete?


class Receiving_Detail(db.Model):
    ''' Data Model for the Receiving Detail '''
    __tablename__ = 'receiving_detail'
    id = Column(Integer, primary_key=True)
    header_id = Column(Integer, ForeignKey('receiving_header.id'))
    line_no = Column(Integer, nullable=False)  # line number for this detail
    item_type_id = Column(Integer, ForeignKey('item_types.id'))  # item type id for this detail
    description = Column(String(100), nullable=False)  # description for this detail
    quantity = Column(Integer, nullable=False)  # quantity received
    book_price = Column(Decimal, nullable=False)  # book price for this detail
    notes = Column(String(max))  # notes for this detail
    is_committed = Column(Boolean, default=False)  # is this detail committed to someone/thing
    is_special = Column(Boolean, default=False)  # is this detail a special item 




def init_db():
    db.create_all()
