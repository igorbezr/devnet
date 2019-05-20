# ---------README for pydoc documentation auto generating-------------

"""
This simple program written in Python 3.5 has created to automate routine
 network tasks such as checking devices hostnames, LAN and VoIP subnets
"""

# ----------Modules importing section---------------------------------
# Importing custom modules
import devices_classes as dev
import input_output_function as func


# ----------Main code---------------------------------------------------
#
# Temporary fix for pydoc correct working
if __name__ == '__main__':
    # Connection to the each device and execution 'show ip route' command
    ip_addresses = func.reading_ip_from_file('devices.txt')
    credentials = func.keyboard_input()
    for ip in ip_addresses:
        # Create new instance of the GeneralNetworkDevice class
        device = dev.GeneralNetworkDevice(
            ip,
            credentials['username'],
            credentials['password'])
        # Trying to initially connect to the device
        device.initial_connect()
        # If error code was not returned in initial connect
        if device.error is False:
            device.send_command('terminal length 0')
            device.search_device_hostname()
            device.parsing_ip_route()
            device.session.close()
            print('\n')
        else:
            print('\n')
    exit()
