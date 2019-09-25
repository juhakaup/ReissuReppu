from application import db

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
