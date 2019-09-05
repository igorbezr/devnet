# ---------README for pydoc documentation auto generating-------------

"""
This module contains function for I/O information to the program
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
        ip_addresess - list that contains IP addresses reading from the file
    """
    # First we will checking if addresses in list is unique
    uniq = set()
    with open(devices, 'r+') as devices_list:
        non_uniq_ip = devices_list.read().splitlines()
        for address in non_uniq_ip:
            if address not in uniq:
                uniq.add(address)
        ip_addresses = list(uniq)
        ip_addresses.sort()
    return ip_addresses


def keyboard_input():
    """
    The keyboard prompt for user to input device credentials

    Input parameters:
        none
    Returns:
        credentials - dictionary contains device's credentials
    """
    print('Good day to you !' + '\n' + 'Welcome to checking subnets script !')
    credentials = dict()
    while True:
        try:
            credentials['username'] = input(
                'Enter username (or Ctrl-C to exit) > ')
            credentials['password'] = getpass(
                'Enter password (or Ctrl-C to exit) > ')
            return credentials
        except KeyboardInterrupt:
            print('\n', 'Program is terminated due to user request !')
            exit()


def output_to_console(dev):
    """
    Printing content of "dev" class instance attributes to the console

    Input parameters:
        dev - instance of "dev" class
    Returns:
        None
    """
    print('')
    print('Device IP address is', str(dev.ip))
    print('Device hostname is', str(dev.hostname))
    print('Device part number is', str(dev.part_number))
    print('Loopback is', str(dev.loopback))
    print('LAN subnet is', str(dev.lan))
    print('VoIP subnet is', str(dev.voip))
    return None


def output_to_json(dev):
    """
    Function for translating output to json

    Input parameters:
        dev - instance of "dev" class
    Returns:
        dict_for_json - dictionary for printing
    """
    dict_for_json = {}
    dict_for_json['ip'] = str(dev.ip)
    dict_for_json['hostname'] = str(dev.hostname)
    dict_for_json['part_number'] = str(dev.part_number)
    dict_for_json['loopback'] = str(dev.loopback)
    dict_for_json['lan'] = str(dev.lan)
    dict_for_json['voip'] = str(dev.voip)
    return dict_for_json
