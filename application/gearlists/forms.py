from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, validators

class ListsForm(FlaskForm):
    name = StringField("Name", [validators.Length(min=2, max=100), validators.Regexp(r'^[a-zA-Z0-9 öäå!@#$%^&*(),.?":{}|<>]*$')])
    description = TextAreaField("Description", [validators.Length(min=2, max=500), validators.Regexp(r'^[a-zA-Z0-9 öäå!@#$%^&*(),.?":{}|<>]*$')])

    class Meta:
        csrf = False