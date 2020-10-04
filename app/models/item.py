from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.sql.schema import ForeignKey

from app.models import db


class Item(db.Model):
    """ Data model for teasure Item """
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    level = Column(Integer)
    quantity = Column(Integer, nullable=False)
    purchase_price = Column(Float)
    item_type_id = Column(Integer, ForeignKey('item_types.id'))