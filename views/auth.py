from functools import wraps
from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import LoginManager, current_user, login_user
from data import User, UsersRepo
from form.forms import LoginForm, RegisterForm

users_repo = UsersRepo()

auth_bp = Blueprint(
    'auth_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

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
    print(reg_form.__getattribute__("_fields")["username"])
    for i in reg_form.__getattribute__("_fields").values():
        print(i)
    
    
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
            flash("wrong username")
            return redirect(url_for("auth_bp.login"))

        # password does not match
        if not foundUser.check_password(login_form.password.data):
            flash("wrong password")
            return redirect(url_for("auth_bp.login"))

        login_user(foundUser)
        print("login successful")

        return redirect(url_for("main_bp.index"))

    return render_template("auth.html", form_for="login", form=login_form)
