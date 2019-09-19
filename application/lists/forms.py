from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, validators

class ListsForm(FlaskForm):
    name = StringField("Name", [validators.Length(min=2, max=60)])
    description = StringField("Description")

    class Meta:
        csrf = False