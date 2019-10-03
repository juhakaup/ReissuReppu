from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, validators

class ListsForm(FlaskForm):
    name = StringField("Name", [validators.Length(min=2, max=100), validators.Regexp(r'^\w+$')])
    description = StringField("Description", [validators.Length(min=2, max=500), validators.Regexp(r'^\w+$')])

    class Meta:
        csrf = False