"""A application module for search website.

Author:
    Kipack Jeong
Date:
    2022-07-10

"""

from flask import Flask, redirect, url_for
from flask_login import LoginManager
from data.usersrepo import UsersRepo
from data.websitesrepo import WebsitesRepo

import config

CATEGORIES = ["housing", "food", "weather"]


class App(Flask):
    """Customized Flask class, which can have attributes `users_repo` and `websites_repo`.

    Inherits:
        Flask
    """
    users_repo = UsersRepo()
    websites_repo = WebsitesRepo()



def create_app():
    """Creates the Flask.app with required blueprints and loginmanger.

    Args:
        users_repo (_type_): user repo to user.
    """
    def create_login_manager(app: App):
        login_manager = LoginManager()
        login_manager.login_view = 'auth.login'
        login_manager.init_app(app)

        @login_manager.user_loader
        def load_user(user_id):
            # Check if user is logged-in on every page load.
            if user_id is not None:
                return app.users_repo.query(user_id)

            return None

        @login_manager.unauthorized_handler
        def unauthorized():
            # Redirect unauthorized users to Login page.
            return redirect(url_for('auth_bp.login'))

    app = App(__name__)
    app.secret_key = config.FLASK_SECRET_KEY

    with app.app_context():
        
        from views import auth_bp, main_bp
        
        # Register blueprints
        app.register_blueprint(auth_bp)
        app.register_blueprint(main_bp)

        create_login_manager(app)

    return app


# create app
app = create_app()

# when cmd executed: python app.py
if __name__ == "__main__":
    app.config["ENV"] = config.ENV
    app.run()
