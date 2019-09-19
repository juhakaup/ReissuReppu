from application import db

class GearList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    name = db.Column(db.String(60))
    description = db.Column(db.String(300))

    def __init__(self, name):
        self.name = name