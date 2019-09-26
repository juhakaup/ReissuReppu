from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators

class LoginForm(FlaskForm):
    email = StringField("Email", [validators.Length(min=2, max=60)])
    password = PasswordField("Password", [validators.Length(min=2, max=60)])

    class Meta:
        csrf = False

class RegisterForm(FlaskForm):
    email = StringField("Email", [validators.Length(min=2, max=60)])
    password = PasswordField("Password", [validators.Length(min=2, max=60)])
    name = StringField("Name", [validators.Length(min=2, max=60)])

    class Meta:
        csrf = False