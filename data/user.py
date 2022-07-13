from time import time
import uuid
from flask_login import UserMixin
from passlib.hash import sha256_crypt
import jwt
import config
from data.usersdb import UsersDB
from utils import logger

DB = UsersDB()


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

    def reset_password(self, p: str):
        """Resets user's password with the given param, password.

        Args:
            p (str): new password
        """

        # hash password
        hashed_p = sha256_crypt.hash(p)
        # set it
        self.password = hashed_p

    def check_password(self, p: str):
        """Matches and validates the given password with the user's password. The hash verifying is used.

        Args:
            p (str): password

        Returns:
            bool: match result
        """
        # match pwd
        r = sha256_crypt.verify(p, self.password)

        return r

    def get_reset_token(self, expires=500):

        return jwt.encode({'reset_password': self.username,
                           'exp':    time() + expires},
                          key=config.FLASK_SECRET_KEY, algorithm="HS256")

    @staticmethod
    def verify_reset_token(token):
        """
        Verifies user existence based on the given jwt token.

        Returns:
            User : found user that matches the `token`. `None` if not found.
        """
        username = jwt.decode(
            token, key=config.FLASK_SECRET_KEY, algorithms=["HS256"])['reset_password']
        user = User.query(un=username)

        return user

    @staticmethod
    def query(id: str = None, un:  str = None):
        """
        Query `DB`(UserDB) with the given id or username. Must pass in value with keyword.

        Args:
            id (str, optional): id. Defaults to None.
            un (str, optional): username. Defaults to None.
        """

        def map_dict_user(usr_d) -> User:

            return User(usr_d["id"],
                        usr_d["firstname"], usr_d["lastname"], usr_d["username"], usr_d["password"])

        if id:
            usr_d: dict = DB.find_user_by_id(id)

        elif un:
            usr_d: dict = DB.find_user_by_username(un)

        if not usr_d:
            return None

        return map_dict_user(usr_d)

    @staticmethod
    def update(user):
        DB.update_user(user)
        result = DB.save()
        if not result:
            return False
        else:
            return True

    @staticmethod
    def create(f: str, l: str, u: str, p: str):
        """
        Creates `User` instance based off on the given user credentials. The `password` will be hashed in here. The created `User` instance will be saved by the `DB`(UserDB).

        Args:
            f (str): firstname
            l (str): lastname
            u (str): username
            p (str): password

        Returns:
            _type_: _description_
        """
        # create unique id
        id = uuid.uuid1()
        # hash the pw
        hashed_pwd = sha256_crypt.hash(p)

        # if user with the same username exists
        if User.query(un=u):
            return

        # create new User instance
        user = User(id, f.lower(), l.lower(), u, hashed_pwd)

        # save it in db
        DB.add_new_user(user)

        return user

    def __repr__(self):
        return '<User {}>'.format(self.username)
