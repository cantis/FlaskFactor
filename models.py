from app import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    username = db.Column(
        db.String(64),
        index=False,
        unique=True,
        nullable=False
    )
    password = db.Column(
        db.string(32),
        index=False
    )

    # def __repr__(self):
    #     return '<User []>'.format(self.username)
