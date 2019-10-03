from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators

class LoginForm(FlaskForm):
    email = StringField("Email", [validators.Length(min=2, max=100, message=("Please provide a valid email address."))])
    password = PasswordField("Password", [validators.Length(min=2, max=144), validators.data_required()])

    class Meta:
        csrf = False

class RegisterForm(FlaskForm):
    email = StringField("Email", [validators.Length(min=2, max=100, message=("Email must be between 4 and 100 characters long.")), validators.Email()])
    password = PasswordField("Password", [validators.Length(min=4, max=100, message=("Password must be between 4 and 100 characters long.")), validators.DataRequired()])
    name = StringField("Name", [validators.Length(min=2, max=144, message=("Name must be between 4 and 100 characters long.")), validators.Regexp(r'^[a-zA-Z0-9 öäå!@#$%^&*(),.?":{}|<>]*$')])

    class Meta:
        csrf = False