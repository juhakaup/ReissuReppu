from application import db
from sqlalchemy.sql import text

# gearlist items table
listItems = db.Table('list_items',
    db.Column('list_id',db.Integer, db.ForeignKey('gear_list.id')),
    db.Column('item_id',db.Integer, db.ForeignKey('item.id'))
)

class GearList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    user = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    description = db.Column(db.String(500))
    items = db.relationship('Item', secondary=listItems, backref=db.backref('items'), lazy = 'dynamic') # gearlist <-> items reference

    def __init__(self, name, user, description):
        self.name = name
        self.user = user
        self.description = description
    
    @staticmethod
    def not_user_lists(user_id):
        stmt = text("SELECT gear_list.id, gear_list.name, gear_list.description, account.name, SUM(item.weight), SUM(item.volume) "
                    "FROM gear_list "
                    "LEFT JOIN account ON gear_list.user = account.id "
                    "LEFT JOIN list_items ON gear_list.id = list_items.list_id "
                    "LEFT JOIN item ON list_items.item_id = item.id "
                    "WHERE NOT account.id = :user_id "
                    "GROUP BY gear_list.id").params(user_id=user_id)
    
        res = db.engine.execute(stmt)
        response = []
        for row in res:
            response.append ({"list_id":row[0], "name":row[1], "description":row[2], "username":row[3], "weight":row[4], "volume":row[5]})
        
        return response

    @staticmethod
    def user_lists(user_id):
        stmt = text("SELECT gear_list.id, gear_list.name, gear_list.description, account.name, SUM(item.weight), SUM(item.volume) "
                    "FROM gear_list "
                    "LEFT JOIN account ON gear_list.user = account.id "
                    "LEFT JOIN list_items ON gear_list.id = list_items.list_id "
                    "LEFT JOIN item ON list_items.item_id = item.id "
                    "WHERE account.id = :user_id "
                    "GROUP BY gear_list.id").params(user_id=user_id)
    
        res = db.engine.execute(stmt)
        response = []
        for row in res:
            response.append ({"list_id":row[0], "name":row[1], "description":row[2], "username":row[3], "weight":row[4], "volume":row[5]})
        
        return response

    def available_items(self, user_id):
        stmt = text("SELECT * FROM item "
                    "LEFT JOIN list_items ON item.id = list_items.item_id "
                    "WHERE item.user = :user_id "
                    "AND list_items.list_id IS null "
                    "OR NOT list_items.list_id = :gearlist_id;").params(user_id = user_id, gearlist_id = self.id)
        res = db.engine.execute(stmt)
        response = []
        for row in res:
            response.append ({"id":row[0], "user":row[1], "name":row[2], "category":row[3], "brand":row[4], "weight":row[5], "volume":row[6], "description":row[7]})
        
        return response

    def weight(self):
        weight = 0
        for item in self.items:
            weight += item.weight
        return weight

    def volume(self):
        volume = 0
        for item in self.items:
            volume += item.volume
        return volume

    def username(self):
        stmt = text("SELECT account.name FROM gear_list "
                    "LEFT JOIN account ON gear_list.user = account.id "
                    "WHERE account.id = :user_id").params(user_id = self.user)
        res = db.engine.execute(stmt)
        response = res.first()
        return response[0]
