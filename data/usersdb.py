import json
from data.user import User
from utils.logger import error

class UsersDB():
    def __init__(self) -> None:
        with open("./data/users.json", "r", encoding="UTF-8") as file:
            self.data: list[User] = json.load(file)
            self.data_str = self.__create_data_str()
        
    def     find_user_by_id(self,id: str):

        found_list: list[dict] = list(
            filter(lambda user: user["id"] == id, self.data))

        if not found_list:

            error(f"The user with the id : {id} not found.")

            return None

        else:

            found_user_dict: dict = found_list[0]
            # map dict -> User class instance


            return found_user_dict

    def find_user_by_username(self,username):
        
        with open("./data/users.json", "r", encoding="UTF-8") as file:
            data: list[User] = json.load(file)
        
        found_list : list[dict] = list(filter(lambda user : user["username"] == username, self.data))
        
        if not found_list:
            
            error(f"The user with the username : {username} not found.")
            
            return None

        else:
            
            found_user_dict : dict = found_list[0]
            
            return found_user_dict

    def add_new_user(self, user: User):
        
        if not user:
            return
        
        self.data.append({"id" : user.id , "firstname" : user.firstname , "lastname" : user.lastname, "username" : user.username, "password" : user.password})
        
        self.__save()
            

    def __save(self):
        
        self.data_str = self.__create_data_str()
        self.data_str.removesuffix("]")

        with open("./data/users.json", "w") as w:
            w.write(self.data_str)
            
        print(self.data)
        

    def __create_data_str(self):

        data_str = "["

        for i, user_dict in enumerate(self.data):
            user_json_str = ("{"  + f"\
    \"id\" : \"{user_dict['id']}\",\n\
    \"firstname\" : \"{user_dict['firstname']}\",\n\
    \"lastname\" : \"{user_dict['lastname']}\",\n\
    \"username\" : \"{user_dict['username']}\",\n\
    \"password\" : \"{user_dict['password']}\"" + "}")

            if i != len(self.data) - 1:
                user_json_str += ","

            data_str += user_json_str

        data_str += "]"

        return data_str

