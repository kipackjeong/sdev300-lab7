from colorama import Fore


def error(msg):
    """ Logs error message on the console.

    Args:
        msg (_type_): error message to log.
    """
    msg = Fore.RED + "ERR: " + str(msg) + Fore.RESET

    print(msg)
