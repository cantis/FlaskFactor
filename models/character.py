from . import db


class Character(db.Model):
    """ Data Model for Character """
    __tablename__ = 'characters'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    character_name = db.Column(db.String, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
