

import json


class WebsitesDB():
    """An end point of the websites data flow. It does logic directly with the websites.json file. 
    """

    def __init__(self, path: str) -> None:
        self.path = path

    def load_data(self):
        """
        Opens the .json data file which has all the websites data.

        """
        f = open(self.path, encoding="UTF-8")
        d = json.load(f)
        f.close()

        return d
