"""A module that has exception handling methods.
"""
from re import A
from colorama import Fore
from flask import flash
from utils.logger import error


def exception_handler(fn):
    """Wrapper function that handles exceptions.

    Args:
        fn (function): function to wrap
    """
    def inner(*args, **kwargs):
        try:
            return fn(*args, **kwargs)

        except Exception as e:
            error(f"Error at {fn.__name__} \n reason: {str(e)}")  
            return None

    return inner

