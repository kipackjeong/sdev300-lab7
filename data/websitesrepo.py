"""A Module that is responsible for managing data which is saved as .json file.

"""

from data.websitesdb import WebsitesDB

class WebsitesRepo():
    """A repository that specifically deals with the end point of the data flow , `WebsitesDB`.
    Can fetch all websites, housing websites, recipe websites, and weather websites.
    """
    
    def __init__(self) -> None:
        self.__db = WebsitesDB("./data/websites.json")
        
        self.__all_websites  = self.__db.load_data()
        self.__housing_websites = self.__all_websites["housing_websites"]
        self.__recipe_websites = self.__all_websites["recipe_websites"]
        self.__weather_websites = self.__all_websites["weather_websites"]
    
    def get_all_websites(self):
        """ Returns all the websites in the websites.json. 

        Returns:
            dict: dictionary of the websites, keys are `housing_websites`, `recipe_websites`, and `weather websites`. 
        """
        return self.__all_websites
    def get_housing_websites(self):
        """Returns all the housing websites in websites.json.

        Returns:
            dict : a dict of housing websites keys are websites' names.
        """
        return self.__housing_websites
    def get_recipe_websites(self):
        """Returns all the recipe websites in websites.json.

        Returns:
            dict : a dict of recipe websites, keys are websites' names.
        """
        return self.__recipe_websites
    def get_weather_websites(self):
        """Returns all the weather websites in websites.json.

        Returns:
            dict : a dict of weather websites, keys are websites' names.
        """
        return self.__weather_websites
