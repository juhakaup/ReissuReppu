from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField

class LoginForm(FlaskForm):
    email = StringField("Email")
    password = PasswordField("Password")

    class Meta:
        csrf = False