from application import db
from sqlalchemy.sql import text

# gearlist articles table
listItems = db.Table('list_items',
    db.Column('list_id',db.Integer, db.ForeignKey('gear_list.id')),
    db.Column('article_id',db.Integer, db.ForeignKey('article.id'))
)

class GearList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    name = db.Column(db.String(60))
    description = db.Column(db.String(300))

    # gearlist <-> articles reference
    articles = db.relationship('Article', secondary=listItems, 
            backref=db.backref('items'), lazy = 'dynamic')

    def __init__(self, name):
        self.name = name

    @staticmethod
    def items_weight_volume(list_id):
        stmt = text("SELECT SUM(weight), SUM(volume) "
        "FROM article LEFT JOIN list_items ON article.id = list_items.article_id "
        "WHERE list_id = :list_id;").params(list_id=list_id)
    
        res = db.engine.execute(stmt)

        response = {}

        for row in res:
            response = ({"weight":row[0], "volume":row[1]})
        
        return response
        