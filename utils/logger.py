"""A module responsible for logging error on the console.
"""

from datetime import datetime, timedelta
from colorama import Fore, init

init(convert=True)

today_str = str(datetime.now().date())

def success(msg: str):
    """ Displays success message on the console with green color and on log file which is at ./logs/{today's date}.

    Args:
        msg(str) : message to display
    """

    s_msg = Fore.GREEN + "Success: " + Fore.RESET

    __log_on_file(msg)

    print(s_msg)


def error(msg):
    """ Logs error message on the console and on log file which is at ./logs/{today's date}.

    Args:
        msg (str): error message to log.
    """

    e_msg = Fore.RED + "ERR: " + str(msg) + Fore.RESET

    __log_on_file(msg)

    print(e_msg)

def test_log(msg: str, *args):


    t_msg = Fore.YELLOW + msg + " ".join(args) + Fore.RESET

    print(t_msg)


def __log_on_file(msg: str):

    f = open(f"./logs/{today_str}.txt", "a")

    f.write("\n" + str(datetime.now().time()) + " " + msg)

    f.close()
