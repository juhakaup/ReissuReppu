from application import db, bcrypt
from application.models import namedCreated

userRoles = db.Table('user_roles',
    db.Column('user_id', db.Integer, db.ForeignKey('account.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
)

class Role(db.Model):
    __tablename__ = "role"
    id = db.Column(db.Integer, primary_key = True)
    role = db.Column(db.String(50), nullable = False)

    def __init__(self, role):
        self.role = role

class User(namedCreated):
    __tablename__ = "account"

    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(60), nullable=False)

    items = db.relationship("Item", backref='item', lazy=True)
    gearlists = db.relationship("GearList", backref='gearlist', lazy=True)
    roles = db.relationship("Role", secondary=userRoles, backref=db.backref('roles'), lazy='dynamic')

    def __init__(self, name, email, password):
        self.name = name
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

