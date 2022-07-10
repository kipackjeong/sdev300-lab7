"""A Module that is responsible for managing data which is saved as .json file.

"""

import json

"""
WebRepo
    .housing_webs = {}
    .recipe_webs = {}
    .weather_webs = {
        
        "some.com" : {
            "name" : "",
            "url" : "",
            "search_url": ""
        }
    }

    
"""
class WebsitesRepo():
    
    def __init__(self) -> None:
        self.__db = WebsitesDB("./data/websites.json")
        
        self.__all_websites  = self.__db.load_data()
        self.__housing_websites = self.__all_websites["housing_websites"]
        self.__recipe_websites = self.__all_websites["recipe_websites"]
        self.__weather_websites = self.__all_websites["weather_websites"]
    
    def get_all_websites(self):
        return self.__all_websites
    
    def get_housing_websites(self):
        return self.__housing_websites
    def get_recipe_websites(self):
        return self.__recipe_websites
    def get_weather_websites(self):
        return self.__weather_websites
    

class WebsitesDB():
    
    def __init__(self,path:str) -> None:
        self.path = path
    
    def load_data(self):
        """
        Opens the .json data file which has all the websites data.

        """
        f = open(self.path, encoding="UTF-8")
        d = json.load(f)
        f.close()

        return d



