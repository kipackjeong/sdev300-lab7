from crypt import methods
from functools import reduce
from colorama import Fore
from flask import Flask, flash, redirect, render_template, request, url_for
from flask_login import LoginManager
from form.forms import LoginForm, RegisterForm, SearchForm
from utils import exception_handler, zipcode_lookup, populate_loc_url
from passlib.hash import sha256_crypt

from data.usersrepo import User, UsersRepo
from data.websitesrepo import load_data   

app = Flask(__name__)
app.secret_key = "session1"
users_repo = UsersRepo()

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in on every page load."""
    if user_id is not None:
        return User.query.get(user_id)
    return None


@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash('You must be logged in to view that page.')
    return redirect(url_for('auth_bp.login'))





CATEGORIES = ["housing", "food", "weather"]

DB = load_data()

RECIPE_WEBS = DB["recipe_websites"]

WEATHER_WEBS = DB["weather_websites"]

HOUSING_WEBS = DB["housing_websites"]

users = []

@app.route("/", methods=["GET"])
def index():

    if not users:
        return redirect("/login")
    
    search_form = SearchForm()
    
    
    return render_template("index.html", house_webs=HOUSING_WEBS, RECIPE_WEBS=RECIPE_WEBS, weather_webs=WEATHER_WEBS, form=search_form)


@app.route("/result", methods=["POST"])
def result():
    """ redirects to corresponding website based on user's inputs.
    """
    try:

        # retrieve from request form
        category = request.form["category"]
        search_value = request.form["search_value"]
        
        if not search_value:
            flash("The input is missing")

        web_name = request.form["website_name"]

        # user chose to search for recipe
        if category == "recipe":

            website = RECIPE_WEBS[web_name]

            extended_url = website["search_url"].replace(
                "{food}", search_value)

        # user chose to search for housing
        elif category == "housing":
            website = HOUSING_WEBS[web_name]

            zip_result = zipcode_lookup(search_value)            

            if not zip_result:
                flash("The Zip-code is not a valid zipcode.")
                return redirect(url_for("index"))
            else:
                state, city = zip_result

            extended_url = populate_loc_url(
                website["search_url"], city=city, state=state, zipcode=search_value)

        # user chose to search for weather
        elif category == "weather":

            website = WEATHER_WEBS[web_name]

            zip_result = zipcode_lookup(search_value)

            if not zip_result:
                flash("The Zip-code is not a valid zipcode.")
                return redirect(url_for("index"))
            else:
                state, city = zip_result
            
            extended_url = populate_loc_url(
                website["search_url"], city=city, state=state, zipcode=search_value)

        search_url = website["url"] + extended_url

        return redirect(search_url)

    except Exception as e:
        print(e)

    return redirect("/")


@exception_handler
@app.route("/register", methods=["GET", "POST"])
def register():
    
    reg_form = RegisterForm()
    
    if reg_form.validate_on_submit():


        # create user
        new_user: User = users_repo.create(
            reg_form.firstname.data, reg_form.lastname.data, reg_form.username.data, reg_form.password.data)
        
        return redirect(url_for("index"))
    
    return render_template("auth.html", form_for="register", form=reg_form)


@exception_handler
@app.route("/login", methods=["GET", "POST"])
def login():

    login_form = LoginForm()
    
    
    if login_form.validate_on_submit():

        # find user from db
        foundUser: User = users_repo.query(username = login_form.username.data)
        
        
        # user with the username not found        
        if not foundUser:
            flash("wrong username")
            return redirect(url_for("login"))

        # password does not match
        if not foundUser.check_password(login_form.password.data):
            flash("wrong password")
            return redirect(url_for("login"))

        
        user = User("","", login_form.username.data, login_form.password.data)
        
        
        users.append(user)

        return redirect(url_for("index"))

            
    return render_template("auth.html", form_for="login", form=login_form)
