from sqlalchemy import Column, Integer, String

from app.models import db


class Item_Type(db.Model):
    """ db model for Item Types """
    __tablename__ = 'item_types'
    id = Column(Integer, primary_key=True)
    item_type = Column(String, nullable=False)