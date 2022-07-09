import uuid
from flask_login import UserMixin
from passlib.hash import sha256_crypt

class User(UserMixin):
    """
    Representational class for the user.
    
    Inherits:
        `UserMixin`
    """
    def __init__(self, id, firstname, lastname, username, password=None, **kwargs) -> None:

        super().__init__()
        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.username = username

        if password:
            self.password = password

        id = kwargs.get("id")
        if id:
            self.id = id
        else:
            self.id = uuid.uuid1()


    def reset_password(self, p:str):
        """Resets user's password with the given param, password.

        Args:
            p (str): new password
        """

        # hash password
        hashed_p = sha256_crypt.hash(p)
        # set it
        self.password = hashed_p

    def check_password(self, p:str):
        """Matches and validates the given password with the user's password. The hash verifying is used.

        Args:
            p (str): password

        Returns:
            bool: match result
        """
        # match pwd
        r = sha256_crypt.verify(p, self.password)

        return r

    def __repr__(self):
        return '<User {}>'.format(self.username)
