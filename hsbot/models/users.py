from hsbot import db
from datetime import datetime


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), index=True, unique=True)
    name = db.Column(db.String(255))
    nearest_observatory = db.Column(db.String(10))
    registered_date = db.Column(db.DateTime)
    notified = db.Column(db.Boolean)

    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name
        self.nearest_observatory = '46106'
        self.registered_date = datetime.now()
        self.notified = False

    def __repr__(self):
        return f'<User id:{self.user_id} name:{self.name} nearest:{self.nearest_observatory}>'
