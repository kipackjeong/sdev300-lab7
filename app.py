"""A application module for search website.

Author:
    Kipack Jeong
Date:
    2022-07-10

"""

import config
from flask import Flask
from data import WebsitesRepo
from flask_mail import Mail

from utils import logger
from utils.email import send_email


CATEGORIES = ["housing", "food", "weather"]


class App(Flask):
    """Customized Flask class, which can have attributes `users_repo` and `websites_repo`.

    Inherits:
        Flask
    """

    def __init__(self, import_name: str, static_url_path=None, static_folder="static", static_host=None, host_matching: bool = False, subdomain_matching: bool = False, template_folder="templates", instance_path=None, instance_relative_config: bool = False, root_path=None):
        super().__init__(import_name, static_url_path, static_folder, static_host, host_matching,
                         subdomain_matching, template_folder, instance_path, instance_relative_config, root_path)
        self.websites_repo = WebsitesRepo()
        self.mail = None


def create_app():
    """Creates the Flask.app with required blueprints and loginmanger.

    Args:
        users_repo (_type_): user repo to user.
    """

    app = App(__name__)
    app.secret_key = config.FLASK_SECRET_KEY

    with app.app_context():

        from views import auth_bp, main_bp

        # Register blueprints
        app.register_blueprint(auth_bp)
        app.register_blueprint(main_bp)

        logger.test_log("added isinstance")

        app.config['MAIL_SERVER'] = config.MAIL_SERVER
        app.config['MAIL_PORT'] = config.MAIL_PORT
        app.config['MAIL_USE_SSL'] = config.MAIL_USE_SSL
        app.config['MAIL_USERNAME'] = config.MAIL_USERNAME
        app.config['MAIL_PASSWORD'] = config.MAIL_PASSWORD

        mail = Mail(app)
        app.mail = mail

    return app


# create app
app = create_app()
# when cmd executed: python app.py
if __name__ == "__main__":
    app.config["ENV"] = config.ENV
    app.run()
