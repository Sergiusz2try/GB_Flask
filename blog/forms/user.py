from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators


class UserRegisterForm(FlaskForm):
    username = StringField("Username", [validators.DataRequired()])
    email = StringField("Email", [validators.DataRequired(), validators.Email()])
    password = PasswordField("Password", [validators.DataRequired(), validators.EqualTo("confirm_password")])
    confirm_password = PasswordField("Confirm Password", [validators.DataRequired()])
    submit = SubmitField("Register")

