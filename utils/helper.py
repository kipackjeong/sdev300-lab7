
from functools import reduce
from typing import Tuple
import requests
from utils import exception_handler
import zipcodes

@exception_handler
def zipcode_lookup(zipcode: str) -> Tuple:

    zip_match = zipcodes.matching(zipcode)[0]
    
    city = zip_match['city']    
    state = zip_match["state"]

    return state, city

@exception_handler
def populate_loc_url(url: str, **kwargs):
    
    repls = []

    for key, val in kwargs.items():

        # pairing the category with the value
        # {city} , New York City

        repls.append(("{" + key + "}", val))

    result = reduce(
        lambda a, kv: a.replace(*kv), repls, url)

    # print(result)

    return result


@exception_handler
def validate_input(usr_input, input_for):

    pass


# @exception_handler
# def __get_geocode(city: str, state: str, zipcode: str):
#     """ Make GET request via Geocode API to get the geocode of the given parameter location.

#     Args:
#         city (str): city name
#         state (str): state name
#         zipcode (str): zipcode

#     Returns:
#         lat (str) : latitude
#         lon (str) : longitude
#     """

#     try:

#         url = "https://forward-reverse-geocoding.p.rapidapi.com/v1/forward"

#         querystring = {"city": city, "state": state,
#                        "postalcode": zipcode, "country": "USA", "accept-language": "en", "polygon_threshold": "0.0"}

#         headers = {
#             "X-RapidAPI-Key": "bb7c540eafmsh899ae8ebf5b34fbp14f87bjsn2c5edbb60724",
#             "X-RapidAPI-Host": "forward-reverse-geocoding.p.rapidapi.com"
#         }

#         response = requests.request(
#             "GET", url, headers=headers, params=querystring)

#         data = response.json()[0]

#         lat = data["lat"]
#         lon = data["lon"]

#         return lat, lon

#     except Exception as exc:
#         print(exc)

#     return None
