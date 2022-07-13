from flask import current_app, render_template, url_for
from flask_mail import Message

from data.user import User


def send_email(user_email: str, user: User, token):
    """Sends email to `user_email` that has link to the password reset route with token attached.
    """
    msg = Message()

    msg.subject = f"Hello {user.firstname}, here is the password reset link."
    msg.recipients = [user_email]
    msg.sender = 'raphilo92@gmail.com'
    msg.html = render_template("reset-pw-email.html", token=token)

    current_app.mail.send(msg)
