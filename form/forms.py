import re
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, SearchField
from wtforms.validators import InputRequired, Length, DataRequired, EqualTo, ValidationError
from app import users_repo

class AuthForm(FlaskForm) :
    username = StringField("Username",  validators=[
                           InputRequired(), Length(min=1, max=20)])
    password = PasswordField("Password", validators=[
        DataRequired(), Length(min=12)], name ="password")


class LoginForm(AuthForm):
    submit = SubmitField("Login")


class RegisterForm(AuthForm):
    firstname = StringField("First Name", validators=[
                            DataRequired(), Length(min=1, max=20)], name="firstname" )
    lastname = StringField("Last Name", validators=[
        DataRequired(), Length(min=1, max=20)], name="lastname")
    
    password_confirm = PasswordField("Password Confirm", validators=[DataRequired(), EqualTo(
        "password", "The confirming password does not match with the password above.")], name="password_confirm")
    
    submit = SubmitField("Register")
    
    def validate_username(self, pwd_field):
        if users_repo.query(un = self.username.data):
            raise ValidationError("The username already exists.")
        
    def validate_password(self, pwd_field):
        pwd = pwd_field.data
        if not re.match("^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{12,}$", pwd):
            raise ValidationError(
                "Password must be at least 12 characters, 1 lowercase, 1 uppercase, 1 number, and 1 special character.")
            
            
class SearchForm(FlaskForm):
    cat_select = SelectField("category", choices=["category","housing","recipe","weather"], name="category")
    search = SearchField(
        validators=[InputRequired(), Length(min=2)], name="search_value")
    web_select = SelectField("website", choices =["website"], name = "website_name")
    submit = SubmitField("Search")

    
    
    
    