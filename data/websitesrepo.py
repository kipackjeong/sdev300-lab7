"""A Module that is responsible for managing data which is saved as .json file.

"""

import json

def load_data():
    """
    Opens the .json data file which has all the websites data.

    """
    f = open("./data/websites.json", encoding="UTF-8")
    d = json.load(f)
    f.close()

    return d
