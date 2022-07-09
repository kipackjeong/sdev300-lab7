from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, SearchField
from wtforms.validators import InputRequired, Length, DataRequired

class AuthForm(FlaskForm) :
    username = StringField("Username",  validators=[
                           InputRequired(), Length(min=1, max=20)])
    password = PasswordField("Password", validators=[
        InputRequired(), Length(min=12)])

class LoginForm(AuthForm):
    submit = SubmitField("Login")



class RegisterForm(AuthForm):
    firstname = StringField("First Name", validators=[
                            DataRequired(), Length(min=1, max=20)], name="firstname" )
    lastname = StringField("Last Name", validators=[
        DataRequired(), Length(min=1, max=20)], name="lastname")
    submit = SubmitField("Register")
    

class SearchForm(FlaskForm):
    cat_select = SelectField("category", choices=["category","housing","recipe","weather"], name="category")
    search = SearchField(
        validators=[InputRequired(), Length(min=2)], name="search_value")
    web_select = SelectField("website", choices =["website"], name = "website_name")
    submit = SubmitField("Search")

    
    
    
    