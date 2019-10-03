from application import db
from sqlalchemy.sql import text

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('account.id'))
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100))
    brand = db.Column(db.String(100))
    weight = db.Column(db.Integer)
    volume = db.Column(db.Numeric(5))
    description = db.Column(db.String(500))

    def __init__(self, name):
        self.name = name
    
    @staticmethod
    def user_items(user_id):
        stmt = text("SELECT * FROM item WHERE item.user = :user_id;").params(user_id = user_id)
        res = db.engine.execute(stmt)
        response = []
        for row in res:
            response.append ({"id":row[0], "user":row[1], "name":row[2], "catogory":row[3], "brand":row[4], "weight":row[5], "volume":row[6], "description":row[7]})
        
        return response
    
    @staticmethod
    def non_user_items(user_id):
        stmt = text("SELECT * FROM item WHERE NOT item.user = :user_id;").params(user_id = user_id)
        res = db.engine.execute(stmt)
        response = []
        for row in res:
            response.append ({"id":row[0], "user":row[1], "name":row[2], "category":row[3], "brand":row[4], "weight":row[5], "volume":row[6], "description":row[7]})
        
        return response

    @staticmethod
    def gearlist_available_items(gearlist_id, user_id):
        stmt = text("SELECT * FROM item "
                    "LEFT JOIN list_items ON item.id = list_items.item_id "
                    "WHERE item.user = :user_id "
                    "AND list_items.list_id IS null "
                    "OR NOT list_items.list_id = :gearlist_id;").params(user_id = user_id, gearlist_id = gearlist_id)
        res = db.engine.execute(stmt)
        response = []
        for row in res:
            response.append ({"id":row[0], "user":row[1], "name":row[2], "category":row[3], "brand":row[4], "weight":row[5], "volume":row[6], "description":row[7]})
        
        return response