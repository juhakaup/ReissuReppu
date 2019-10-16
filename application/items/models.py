from application import db
from application.models import namedCreated
from sqlalchemy.sql import text

class Item(namedCreated):
    __tablename__ = "item"

    user_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    brand = db.Column(db.String(100), nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    volume = db.Column(db.Numeric(5), nullable=False)
    description = db.Column(db.String(500), nullable=False)

    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return self.id != other.id
    
    @staticmethod
    def user_items(user_id):
        stmt = text("SELECT item.id, item.user_id, item.name, item.category, item.brand, item.weight, item.volume, item.description "
                    "FROM item WHERE item.user_id = :user_id;").params(user_id = user_id)
        res = db.engine.execute(stmt)
        response = []
        for row in res:
            response.append ({"id":row[0], "user_id":row[1], "name":row[2], "catogory":row[3], "brand":row[4], "weight":row[5], "volume":row[6], "description":row[7]})
        
        return response
    
    @staticmethod
    def non_user_items(user_id):
        stmt = text("SELECT item.id, item.user_id, item.name, item.category, item.brand, item.weight, item.volume, item.description "
                    "FROM item WHERE NOT item.user_id = :user_id;").params(user_id = user_id)
        res = db.engine.execute(stmt)
        response = []
        for row in res:
            response.append ({"id":row[0], "user_id":row[1], "name":row[2], "category":row[3], "brand":row[4], "weight":row[5], "volume":row[6], "description":row[7]})
        
        return response
