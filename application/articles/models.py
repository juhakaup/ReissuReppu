from application import db

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(255))
    brand = db.Column(db.String(64))
    weight = db.Column(db.Integer)
    volume = db.Column(db.Numeric(5))

    def __init__(self, name, brand, weight, volume, description):
        self.name = name
        self.brand = brand
        self.weight = weight
        self.volume = volume
        self.description = description