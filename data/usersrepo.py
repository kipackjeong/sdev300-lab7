import uuid
from data.usersdb import UsersDB
from passlib.hash import sha256_crypt
from data.user import User


class UsersRepo():    
    
    """
    Responsible for creating User instance and save it in the UserDB and querying user from the UserDB.
    """
    
    def __init__(self) -> None:
        self.db = UsersDB()
        
    def query(self,id : str= None, un :  str=None):
        """
        Query `self.db`(UserDB) with the given id or username.

        Args:
            id (str, optional): id. Defaults to None.
            un (str, optional): username. Defaults to None.
        """
        
        def map_dict_user(usr_d) -> User:
            
            return User(usr_d["id"],
                        usr_d["firstname"], usr_d["lastname"], usr_d["username"], usr_d["password"])
                    
        if id:
            usr_d : dict = self.db.find_user_by_id(id)
            
        elif un:
            usr_d: dict = self.db.find_user_by_username(un)
            
        if not usr_d:
            return None

        return map_dict_user(usr_d)

    def create(self, f: str, l: str, u: str, p: str):
        """
        Creates `User` instance based off on the given user credentials. The `password` will be hashed in here. The created `User` instance will be saved by the `self.db`(UserDB).

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
        if self.query(u):
            return 
        
        # create new User instance
        user = User(id, f.lower(), l.lower(), u, hashed_pwd)
        
        # save it in db
        self.db.add_new_user(user)
        
        return user
    
    
    
