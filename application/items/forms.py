from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, SelectField, validators

class ItemForm(FlaskForm):
    name = StringField("Name", [validators.Length(min=2, max=100), validators.Regexp(r'^[a-zA-Z0-9 öäå!@#$%^&*(),.?":{}|<>]*$')])
    user = IntegerField("User")
    brand = StringField("Brand", [validators.Length(min=2, max=100), validators.Regexp(r'^[a-zA-Z0-9 öäå!@#$%^&*(),.?":{}|<>]*$')])
    category = SelectField("Category", 
                    choices=[('other', 'Other'), ('shelter', 'Shelter'), ('cooking', 'Cooking'), ('clothing', 'Clothing'), 
                            ('hygene', 'Hygene'), ('elec', 'Electronics'), ('sleeping', 'Sleeping'), 
                            ('nav', 'Navigation'), ('survival', 'Survival'), ('luxury', 'Luxury')])
    weight = IntegerField("Weight in grams", [validators.NumberRange(min=0, max=100000)])
    volume = FloatField("Volume in liters", [validators.NumberRange(min=0, max=99)])
    description = StringField("Description", [validators.Length(min=2, max=500)])
    id = IntegerField("id")

    class Meta:
        csrf = False