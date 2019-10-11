from application import db, bcrypt
from application.models import namedCreated

class User(namedCreated):
    __tablename__ = "account"

    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(60), nullable=False)

    items = db.relationship("Item", backref='item', lazy=True)
    gearlists = db.relationship("GearList", backref='gearlist', lazy=True)

    def __init__(self, email, password):
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def get_id(self):
        return self.id

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    def roles(self):
        return ["ADMIN"]
