from functools import wraps
from flask import Blueprint, current_app as app, flash, redirect, render_template, url_for
from flask_login import  current_user, login_remembered, login_required, login_user, logout_user
from data import User
from form.forms import LoginForm, RegisterForm

auth_bp = Blueprint(
    'auth_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

users_repo = app.users_repo

def not_logged_in_required(fn):

    @wraps(fn)
    def decorated_view(*args, **kwargs):
        
        # if user is already logged in, redirect to main_bp.index
        if current_user and current_user.is_authenticated:
            return redirect(url_for('main_bp.index'))

        
        return fn(*args, **kwargs)

    return decorated_view

@auth_bp.route("/register", methods=["GET", "POST"])
@not_logged_in_required
def register():
    
    reg_form = RegisterForm()
    
    if reg_form.validate_on_submit():

        # create user
        new_user: User = users_repo.create(
            reg_form.firstname.data, reg_form.lastname.data, reg_form.username.data, reg_form.password.data
            ) 
        

        return redirect(url_for("main_bp.index"))

        

    return render_template("auth.html", form_for="register", form=reg_form)

@auth_bp.route("/login", methods=["GET", "POST"])
@not_logged_in_required
def login():
    
    login_form = LoginForm()

    if login_form.validate_on_submit():

        # find user from db
        foundUser: User = users_repo.query(un=login_form.username.data)
        
        # user with the username not found
        if not foundUser:
            flash("The user with the given username not found.")
            return render_template("auth.html", form_for="login", form=login_form)

        # password does not match
        if not foundUser.check_password(login_form.password.data):
            flash("The password does not match.")
            return render_template("auth.html", form_for="login", form=login_form)

        login_user(foundUser)
        print("login successful")

        return redirect(url_for("main_bp.index"))

    return render_template("auth.html", form_for="login", form=login_form)


@auth_bp.route("/logout")
@login_required
def logout():
    
    logout_user()

    return redirect(url_for("auth_bp.login"))