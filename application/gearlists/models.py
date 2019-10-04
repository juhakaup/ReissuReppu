from application import db
from application.models import namedCreated
from sqlalchemy.sql import text

# gearlist items table
listItems = db.Table('list_items',
    db.Column('list_id',db.Integer, db.ForeignKey('gearlist.id')),
    db.Column('item_id',db.Integer, db.ForeignKey('item.id'))
)

class GearList(namedCreated):
    __tablename__ = "gearlist"

    user_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    items = db.relationship('Item', secondary=listItems, backref=db.backref('items'), lazy = 'dynamic') # gearlist <-> items reference

    def __init__(self, name, user_id, description):
        self.name = name
        self.user_id = user_id
        self.description = description
    
    @staticmethod
    def not_user_lists(user_id):
        stmt = text("SELECT gearlist.id, gearlist.name, gearlist.description, account.name, SUM(item.weight), SUM(item.volume) "
                    "FROM gearlist "
                    "LEFT JOIN account ON gearlist.user_id = account.id "
                    "LEFT JOIN list_items ON gearlist.id = list_items.list_id "
                    "LEFT JOIN item ON list_items.item_id = item.id "
                    "WHERE NOT account.id = :user_id "
                    "GROUP BY gearlist.id").params(user_id=user_id)
    
        res = db.engine.execute(stmt)
        response = []
        for row in res:
            response.append ({"list_id":row[0], "name":row[1], "description":row[2], "username":row[3], "weight":row[4], "volume":row[5]})
        return response

    @staticmethod
    def user_lists(user_id):
        stmt = text("SELECT gearlist.id, gearlist.name, gearlist.description, account.name, SUM(item.weight), SUM(item.volume) "
                    "FROM gearlist "
                    "LEFT JOIN account ON gearlist.user_id = account.id "
                    "LEFT JOIN list_items ON gearlist.id = list_items.list_id "
                    "LEFT JOIN item ON list_items.item_id = item.id "
                    "WHERE account.id = :user_id "
                    "GROUP BY gearlist.id").params(user_id=user_id)
    
        res = db.engine.execute(stmt)
        response = []
        for row in res:
            response.append ({"list_id":row[0], "name":row[1], "description":row[2], "username":row[3], "weight":row[4], "volume":row[5]})    
        return response

    def available_items(self, user_id):
        stmt = text("SELECT item.id, item.user_id, item.name, item.category, item.brand, item.weight, item.volume, item.description FROM item "
                    "LEFT JOIN list_items ON item.id = list_items.item_id "
                    "WHERE item.user_id = :user_id "
                    "AND list_items.list_id IS null "
                    "OR NOT list_items.list_id = :gearlist_id;").params(user_id = user_id, gearlist_id = self.id)
        res = db.engine.execute(stmt)
        response = []
        for row in res:
            response.append ({"id":row[0], "user_id":row[1], "name":row[2], "category":row[3], "brand":row[4], "weight":row[5], "volume":row[6], "description":row[7]})  
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
        stmt = text("SELECT account.name FROM gearlist "
                    "LEFT JOIN account ON gearlist.user_id = account.id "
                    "WHERE account.id = :user_id").params(user_id = self.user_id)
        res = db.engine.execute(stmt)
        response = res.first()
        return response[0]
