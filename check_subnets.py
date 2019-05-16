# ---------README for pydoc documentation auto generating-------------

"""
Python 3.5 script shows particular subnets of the Cisco network device

Hello everyone ! Thanks for your attention.

This simple program has created to automate routine network checking of
device subnets and IP routing table. The routing table is checking to
find OSPF, BGP, Static and connected routes. Then output has been
processed to find specific subnets.
"""

# ----------Libraries importing section---------------------------------
# Importing pexpect for handle connections to the device, regular
# expressions for searching pattern, getpass for password prompt
import pexpect
import re
from getpass import getpass


# ----------Classes definition section----------------------------------
class GeneralNetworkDevice():
    """
    Class for typical network device

    Attributes:
    self.ip - ip address of the network device
    self.username - username for device's login
    self.password - password for this device
    self.session - pexpect ssh session to the device
    self.error - flag, indicates that an error has occurred

    Methods:
    __init__ - initiation method
    initial_connect - method that is handled initial connection
    send_command - method that is used to send command to the device
    search_device_hostname - Searching the device's hostname
                            in running-config
    parsing_ip_route - parsing the output from 'show ip route'
                            to find subnets
    """

    def __init__(self, ip, username, password):
        self.ip = ip
        self.username = username
        self.password = password
        self.session = None
        self.error = False

    def initial_connect(self):
        self.session = pexpect.spawn(
            'ssh ' + self.username + '@' + self.ip,
            timeout=30)
        output = self.session.expect([
            '(yes/no)',
            'Password:',
            pexpect.TIMEOUT,
            pexpect.EOF])
        if output == 0:
            self.session.sendline('yes')
            output = self.session.expect_exact([
                ')' + '?' + ' yes' +
                '\nWarning: Permanently added \'' + self.ip +
                '\'' + '(RSA) to the list of known hosts.' +
                '\nPassword:',
                pexpect.TIMEOUT,
                pexpect.EOF])
            if output != 0:
                print(
                    'Connection to the device ' + self.ip +
                    ' received unexpected output :')
                print(self.session.before.strip())
                self.error = True
                return self.error
            self.send_command(self.password)
        if output == 1:
            self.send_command(self.password)
        if output == 2:
            print(
                'Connection to the device ' + self.ip + ' timed out !')
            print(self.session.before.strip())
            self.error = True
            return self.error
        if output == 3:
            print(
                'Connection to the device ' + self.ip +
                ' received unexpected output :')
            print(self.session.before.strip())
            self.error = True
            return self.error

    def send_command(self, command):
        self.session.sendline(command)
        output = self.session.expect([
            '#',
            pexpect.TIMEOUT,
            pexpect.EOF])
        if output != 0:
            print(
                'Connection to the device ' + self.ip +
                ' received unexpected output')
            print(self.session.before.strip())
            self.error = True
            return self.error
        return self.session

    def search_device_hostname(self):
        print('Device IP address is ' + self.ip)
        self.session = self.send_command('show running-config | in hostname')
        config = self.session.before.splitlines()
        host = re.compile('^hostname +.*')
        for line in config:
            line = line.strip().decode(encoding="utf-8", errors="strict")
            if host.search(line):
                hostname = host.search(line).group(0)[9:]
                print('Device hostname is ' + hostname)
                break
        else:
                print('Nothing found')
        return 0

    def parsing_ip_route(self):
        # Getting ip routing table from the device
        self.session = self.send_command('show ip route')
        show_ip_route = self.session.before.splitlines()
        # Processing the routing table by regular expressions
        routes = re.compile('^B.*|^O.*|^C +.*|^S.*')
        search_result = list()

        # Looping through the list and searching matches
        for line in show_ip_route:
            line = line.strip().decode(encoding="utf-8", errors="strict")
            if routes.search(line):
                search_result.append(routes.search(line).group(0))

        # Processing received routes with additional regular expressions
        loopback = re.compile('^C.* Loopback0$')
        lan = re.compile('^C.* Vlan20$')
        voip = re.compile('^C.* Vlan21$')
        subnet = re.compile(
            '\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/\d{1,3}')
        if search_result:
            for line in search_result:
                if loopback.search(line):
                    print('Loopback is ' + subnet.search(line).group(0))
                elif lan.search(line):
                    print('LAN subnet is ' + subnet.search(line).group(0))
                elif voip.search(line):
                    print('VoIP subnet is ' + subnet.search(line).group(0))
        else:
            print('No routes found !')
        return 0


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


# ----------Main code---------------------------------------------------
#
# Temporary fix for pydoc correct working
if __name__ == '__main__':
    # Connection to the each device and execution 'show ip route' command
    ip_addresses = reading_ip_from_file('devices.txt')
    credentials = keyboard_input()
    for ip in ip_addresses:
        # Create new instance of the GeneralNetworkDevice class
        device = GeneralNetworkDevice(
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
