from hsbot import db


class Observatory(db.Model):
    __tablename__ = 'observatories'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), index=True, unique=True)
    pref = db.Column(db.String(10))
    name = db.Column(db.String(50))
    name_kana = db.Column(db.String(50))
    location = db.Column(db.String(255))
    lat_deg = db.Column(db.Integer)
    lat_min = db.Column(db.Float)
    lon_deg = db.Column(db.Integer)
    lon_min = db.Column(db.Float)

    def __init__(self, code, pref, name, name_kana, location,
                 lat_deg, lat_min, lon_deg, lon_min):
        self.code = code
        self.pref = pref
        self.name = name
        self.name_kana = name_kana
        self.location = location
        self.lat_deg = lat_deg
        self.lat_min = lat_min
        self.lon_deg = lon_deg
        self.lon_min = lon_min

    def __repr__(self):
        return f'<Observatory id:{self.id} code:{self.code} name:{self.name}>'
