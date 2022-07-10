from crypt import methods
from datetime import timedelta
from functools import reduce
from colorama import Fore
from flask import Blueprint, Flask, session, flash, redirect, render_template, request, url_for
from flask_login import LoginManager, login_required, login_user
from utils import exception_handler, zipcode_lookup, populate_loc_url
from passlib.hash import sha256_crypt

from data.usersrepo import User, UsersRepo
from data.websitesrepo import WebsitesRepo

CATEGORIES = ["housing", "food", "weather"]

def create_app(users_repo):
    app = Flask(__name__)
    app.secret_key = "session1"   
    

    with app.app_context():
        from views import auth_bp
        from views import main_bp
        app.register_blueprint(auth_bp)
        app.register_blueprint(main_bp)

        login_manager = LoginManager()
        login_manager.login_view = 'auth.login'
        login_manager.init_app(app)
        
        @login_manager.user_loader
        def load_user(user_id):
            """Check if user is logged-in on every page load."""
            if user_id is not None:
                return users_repo.query(user_id)

            return None


        @login_manager.unauthorized_handler
        def unauthorized():
            """Redirect unauthorized users to Login page."""
            flash('You must be logged in to view that page.')
            return redirect(url_for('auth_bp.login'))
        
    

    return app

users_repo = UsersRepo()
app = create_app(users_repo)

if __name__ == "__main__":
    app.config["ENV"] = "development"
    app.run()