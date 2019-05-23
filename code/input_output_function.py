# ---------README for pydoc documentation auto generating-------------

"""
This module contains function for I/O information to the program
"""

# ----------Modules importing section---------------------------------
# Importing getpass for password prompt
from getpass import getpass
# Importing json for output in .json file
import json


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


def output_to_console(dev):
    """
    Printing content of "dev" class instance attributes to the console

    Input parameters:
        dev - instance of "dev" class
    Returns:
        0
    """
    print('')
    print('Device IP address is ' + dev.ip)
    print('Device hostname is ' + dev.hostname)
    print('Loopback is ' + dev.loopback)
    print('LAN subnet is ' + dev.lan)
    print('VoIP subnet is ' + dev.voip)
    return 0


def output_to_json(dev, file):
    """
    Function for translating output to json

    Input parameters:
        dev - instance of "dev" class
        file - string, filename for output .json file
    Returns:
        0
    """
    dict_for_json = {}
    dict_for_json['ip'] = str(dev.ip)
    dict_for_json['hostname'] = str(dev.hostname)
    dict_for_json['loopback'] = str(dev.loopback)
    dict_for_json['lan'] = str(dev.lan)
    dict_for_json['voip'] = str(dev.voip)
    with open(file, 'a') as json_file:
        json_file.write(json.dumps(dict_for_json, sort_keys=True))
    return 0
