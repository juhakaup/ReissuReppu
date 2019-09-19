from application import db

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('account.id'))
    name = db.Column(db.String(60), nullable=False)
    category = db.Column(db.String(60))
    brand = db.Column(db.String(60))
    weight = db.Column(db.Integer)
    volume = db.Column(db.Numeric(5))
    description = db.Column(db.String(255))

    def __init__(self, name):
        self.name = name