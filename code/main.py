# ---------README for pydoc documentation auto generating-------------

"""
This simple program has written in Python 3.5 for purpose to automate boring
network tasks such as checking devices hostnames, LAN and VoIP subnets.
"""

# ----------Modules importing section---------------------------------
# Importing custom modules
import devices_classes as dev
from input_output_function import (
    reading_ip_from_file, keyboard_input,
    output_to_console, output_to_json)
# Importing json for output in .json file
from json import dumps

# ----------Main code---------------------------------------------------

# Fix for pydoc correct working
if __name__ == '__main__':
    try:
        # Read device ip addresses from the file and get password prompting
        ip_addresses = reading_ip_from_file('devices.txt')
        credentials = keyboard_input()
        # New log file for JSON
        json_log = open('log.json', 'w')
        # Connection to the each device and execution 'show ip route' command
        for ip in ip_addresses:
            # Create new instance of the GeneralNetworkDevice class
            device = dev.GeneralNetworkDevice(
                ip,
                credentials['username'],
                credentials['password'])
            # Trying to initially connect to the device
            if device.initial_connect() is True:
                device.send_command('terminal length 0')
                device.search_device_hostname()
                # Message for user if device is not a branch router
                is_not_a_branch_message = ' '.join([
                    device.hostname, 'with address',
                    device.ip, 'is not a branch router !'])
                # Checking if this device is branch router
                device.search_device_part_number()
                branch_routers = set([
                    'C881', 'CISCO881', 'C2911', 'CISCO2911'])
                if device.part_number in branch_routers:
                    branch_router = dev.BRANCH_ISR(
                        device.ip,
                        device.username,
                        device.password,
                        device.session,
                        device.hostname,
                        device.part_number)
                    # Getting information about subnets
                    branch_router.parsing_ip_route()
                    # Printing output to the console
                    output_to_console(branch_router)
                    # Writing output to the JSON log
                    json_log.write(dumps(
                        output_to_json(branch_router), sort_keys=True,
                        indent=4, separators=(', ', ': ')))
                    branch_router.session.close()
                else:
                    print(is_not_a_branch_message)
            device.session.close()
        json_log.close()
    except KeyboardInterrupt:
        print('\n', 'Program is terminated due to user request !')
    exit()
