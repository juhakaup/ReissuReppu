from application import db
from sqlalchemy.sql import text

# gearlist items table
listItems = db.Table('list_items',
    db.Column('list_id',db.Integer, db.ForeignKey('gear_list.id')),
    db.Column('item_id',db.Integer, db.ForeignKey('item.id'))
)

class GearList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    name = db.Column(db.String(60))
    description = db.Column(db.String(300))

    # gearlist <-> items reference
    items = db.relationship('Item', secondary=listItems, 
            backref=db.backref('items'), lazy = 'dynamic')

    def __init__(self, name):
        self.name = name

    @staticmethod
    def items_weight_volume(list_id):
        stmt = text("SELECT SUM(weight), SUM(volume) "
        "FROM item LEFT JOIN list_items ON item.id = list_items.item_id "
        "WHERE list_id = :list_id;").params(list_id=list_id)
    
        res = db.engine.execute(stmt)

        response = {}

        for row in res:
            response = ({"weight":row[0], "volume":row[1]})
        
        return response
    
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