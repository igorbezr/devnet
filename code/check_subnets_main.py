# ---------README for pydoc documentation auto generating-------------

"""
This simple program written in Python 3.5 has created to automate routine
 network tasks such as checking devices hostnames, LAN and VoIP subnets
"""

# ----------Modules importing section---------------------------------
# Importing custom modules
import devices_classes as dev
import input_output_function as func
# Import regular expression module
import re
# Import os library for operation with files
import os

# ----------Main code---------------------------------------------------
#
# Clear existing JSON log file
if os.path.isfile('/home/cisco/repo/code/log.json') is True:
    os.remove('/home/cisco/repo/code/log.json')

# Fix for pydoc correct working
if __name__ == '__main__':

    # Read device ip addresses from the file and get password prompting
    ip_addresses = func.reading_ip_from_file('devices.txt')
    credentials = func.keyboard_input()

    # Connection to the each device and execution 'show ip route' command
    for ip in ip_addresses:

        # Create new instance of the GeneralNetworkDevice class
        device = dev.GeneralNetworkDevice(
            ip,
            credentials['username'],
            credentials['password'])

        # Trying to initially connect to the device
        device.initial_connect()
        if device.error is False:
            device.send_command('terminal length 0')
            device.search_device_hostname()

        # Checking if this device is branch router
        branch_hostname = re.compile('R881')
        if branch_hostname.search(str(device.hostname)):
            branch_router = dev.ISR881(
                device.ip,
                device.username,
                device.password,
                device.session,
                device.hostname)
            branch_router.parsing_ip_route()
            func.output_to_console(branch_router)
            func.output_to_json(branch_router, 'log.json')
            branch_router.session.close()
        device.session.close()

    exit()
