"""Authorization/Authentication view.
"""

from functools import wraps
from unittest.util import three_way_cmp
from flask import Blueprint, current_app as app, flash, redirect, render_template, url_for
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from data import User
from utils import logger
from form.forms import EmailForm, LoginForm, RegisterForm, ResetForm


from utils.email import send_email


auth_bp = Blueprint(
    'auth_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    # Check if user is logged-in on every page load.
    if user_id is not None:
        return User.query(id=user_id)

    return None


@login_manager.unauthorized_handler
def unauthorized():
    # Redirect unauthorized users to Login page.
    return redirect(url_for('auth_bp.login'))


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
        User.create(
            reg_form.firstname.data, reg_form.lastname.data, reg_form.username.data, reg_form.password.data
        )
        
        logger.success(f"The user {reg_form.username.data} is registered.")
        return redirect(url_for("auth_bp.login"))
    return render_template("auth.html", form_for="register", form=reg_form)


@auth_bp.route("/login", methods=["GET", "POST"])
@not_logged_in_required
def login():

    login_form = LoginForm()

    if login_form.validate_on_submit():

        # find user from db
        foundUser: User = User.query(un=login_form.username.data)

        login_user(foundUser)

        logger.success(f"The user {foundUser.username} is logged in.")

        return redirect(url_for("main_bp.index"))

    return render_template("auth.html", form_for="login", form=login_form)


@auth_bp.route("/logout")
@login_required
def logout():

    try:
        logout_user()
    except Exception as e:
        logger.error("Failed to log out : " + str(e))

    return redirect(url_for("auth_bp.login"))


@auth_bp.route("/resetpassword/request", methods=["GET", "POST"])
@login_required
def reset_pw_request():
    print(current_user.is_authenticated)

    email_form = EmailForm()
    logger.test_log("email_form ")

    # if the form is validated
    if email_form.validate_on_submit():
        logger.test_log("email validated")

        token = current_user.get_reset_token()
        # send user email with jwt token in it
        send_email(user_email=email_form.email.data,
                   user=current_user, token=token)
        logger.success("email was sent successfully.")

        # after sending link email, log user out so when user comes back with the
        # password reset email, there is no existing user's data on the session.

        logout_user()

        return render_template("reset-pw.html", step="after", email=email_form.email.data)

    # when user enters this page at first
    return render_template("reset-pw.html",  step="before", form=email_form,)


@auth_bp.route("/resetpassword/reset/<token>", methods=["GET", "POST"])
def reset_pw(token):
    """ Verifies the token from the url, then redirects to reset form.
    If not verified returns to login page.
    """
    # if current_user.is_authenticated:
    #     return redirect(url_for("main_bp.index"))

    # user verified with token from url
    user = User.verify_reset_token(token)

    logger.test_log("reset_pw()")

    if not user:
        return redirect(url_for("auth_bp.login"))

    logger.success("User verified token.")

    reset_form = ResetForm()

    # valid pw reset form
    if reset_form.validate_on_submit():

        pw = reset_form.password.data

        # reset pw
        user.reset_password(pw)
        User.update(user)

        flash("Your password has been reset. Please login.")

        return redirect(url_for("auth_bp.login"))

    return render_template("reset-pw.html", form=reset_form, step="reset")
