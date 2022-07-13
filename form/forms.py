import re
from flask import current_app as app
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, SearchField, EmailField
from wtforms.validators import InputRequired, Length, DataRequired, EqualTo, ValidationError

from data import User


class AuthForm(FlaskForm):
    """

    Inherits:
        `FlaskForm`
    """
    username = StringField("Username",  validators=[
                           InputRequired(), Length(min=1, max=20)])
    password = PasswordField("Password", validators=[
        DataRequired()], name="password")


class LoginForm(AuthForm):
    """Form that is used in `/login` route.

    Inherits:
        `AuthForm`
    """
    submit = SubmitField("Login")


class RegisterForm(AuthForm):
    firstname = StringField("First Name", validators=[
                            DataRequired(), Length(min=1, max=20)], name="firstname")
    lastname = StringField("Last Name", validators=[
        DataRequired(), Length(min=1, max=20)], name="lastname")

    password_confirm = PasswordField("Password Confirm", validators=[
                                     DataRequired(), EqualTo("password", "The password confirm field must be equal to password.")], name="password_confirm")

    submit = SubmitField("Register")

    def validate_username(self, field):

        if User.query(un=field.data):
            raise ValidationError("The username already exists.")

    def validate_password(self, field):
        pwd = field.data

        # validate with length
        if len(pwd) < 12:
            raise ValidationError(
                "The password must be at least 12 characters long.")

        # validate with requirements
        if not re.match("^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{12,}$", pwd):
            raise ValidationError(
                "Password must be at least 12 characters, 1 lowercase, 1 uppercase, 1 number, and 1 special character.")


class SearchForm(FlaskForm):
    cat_select = SelectField("category", choices=[
                             "category", "housing", "recipe", "weather"], name="category")
    search = SearchField(
        validators=[InputRequired(), Length(min=2)], name="search_value")
    web_select = SelectField(
        "website", choices=["website"], name="website_name")
    submit = SubmitField("Search")


class EmailForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired()], name="email")
    submit = SubmitField("Send")


class ResetForm(FlaskForm):
    password = PasswordField("Password", validators=[
        DataRequired()], name="password")
    password_confirm = PasswordField("Password Confirm", validators=[
                                     DataRequired(), EqualTo("password", "The password confirm field must be equal to password.")], name="password_confirm")
    submit = SubmitField("Reset")

    def validate_password(self, field):
        pwd = field.data

        # validate with length
        if len(pwd) < 12:
            raise ValidationError(
                "The password must be at least 12 characters long.")

        # validate with requirements
        if not re.match("^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{12,}$", pwd):
            raise ValidationError(
                "Password must be at least 12 characters, 1 lowercase, 1 uppercase, 1 number, and 1 special character.")
