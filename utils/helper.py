"""A module that contains helper functions.
"""

from functools import reduce
from typing import Tuple
from utils.ehandler import exception_handler
import zipcodes


@exception_handler
def zipcode_lookup(zipcode: str) -> Tuple:
    """ Finds city, state of the given zipcode.

    Args:
        zipcode (str): zipcode to lookup

    Returns:
        Tuple: state, city
    """

    zip_match = zipcodes.matching(zipcode)[0]

    city = zip_match['city']
    state = zip_match["state"]

    return state, city


@exception_handler
def populate_loc_url(url: str, **kwargs):
    """Generates search url from default website's search url with the keyword arguments. 

    Args:
        url (str): a default search url, such as www.google.com/{city},{state}

    Returns:
        str: created url ex) www.google.com/seattle.WA 
    """

    repls = []

    for key, val in kwargs.items():

        # pairing the category with the value
        # {city} , New York City

        repls.append(("{" + key + "}", val))

    result = reduce(
        lambda a, kv: a.replace(*kv), repls, url)

    # print(result)

    return result
