from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DecimalField, validators

class ArticleForm(FlaskForm):
    name = StringField("Name", [validators.Length(min=2)])
    user = IntegerField("User")
    brand = StringField("Brand", [validators.Length(min=2)])
    category = StringField("Category")
    weight = IntegerField("Weight", [validators.NumberRange(min=0)])
    volume = DecimalField("Volume", [validators.NumberRange(min=0)],  places=2, )
    description = StringField("Description")
    id = IntegerField("id")

    class Meta:
        csrf = False