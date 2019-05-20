# ---------README for pydoc documentation auto generating-------------

"""
This module contains function for reading device information from a file
and for prompting password to user
"""

# ----------Modules importing section---------------------------------
# Importing getpass for password prompt
from getpass import getpass


# ----------Function definition section--------------------------------
#
def reading_ip_from_file(devices):
    """
    Reading IP addresses of devices from .txt file

    Input parameters:
        devices - string, filename for a list of IP addresses
    Returns:
        ip - list that contains IP addresses reading from the file
    """

    ip_addresses = list()
    file = open(devices, 'r')
    ip_addresses = [line.strip() for line in file]
    file.close()
    return ip_addresses


def keyboard_input():
    """
    The keyboard prompt for user to input device credentials

    Input parameters:
        none
    Returns:
        credentials - dictionary contains device's credentials
    """
    credentials = dict()
    while True:
        try:
            credentials['username'] = input(
                'Enter username (or Ctrl-C to exit):')
            credentials['password'] = getpass(
                'Enter password (or Ctrl-C to exit):')
            break
        except KeyboardInterrupt:
            print('\n')
            print('Program is terminating !')
            exit()
    return credentials
