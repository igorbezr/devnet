# ---------README for pydoc documentation auto generating-------------

"""
This module contains network devices classes code
"""

# ----------Modules importing section---------------------------------
# Importing pexpect for handle connections to the device, regular
# expressions for searching patterns in the CLI output
import pexpect as ssh
from pexpect import TIMEOUT, EOF
import re


# ----------Classes definition section----------------------------------
class GeneralNetworkDevice():
    """
    Class for typical network device

    Main attributes:
    self.ip - ip address of the network device
    self.username - username for device's login
    self.password - password for this device
    self.session - pexpect ssh session to the device
    self.hostname - logical name of the network device

    Strings attributes:
    self.credentials - pexpect ssh credentials
    self.timeout_message - for situation when the TIMEOUT exception raises
    self.unexpected_message - for situation when the device produces
                                unexpected output

    Methods:
    __init__ - initiation method
    initial_connect - method that is handled initial connection
    send_command - method that is used to send command to the device
    search_device_hostname - Searching the device's hostname
                            in running-config
    """

    def __init__(self, ip, username, password):
        self.ip = ip
        self.username = username
        self.password = password
        self.session = None
        self.hostname = None
        # String for credentials and user alerting
        self.credentials = (
            'ssh ' + self.username + '@' + self.ip)
        self.timeout_message = ' '.join([
            'Connection to the device', self.ip, 'timed out:'])
        self.unexpected_message = ' '.join([
            'Connection to the device', self.ip,
            'received unexpected output :'])

    def initial_connect(self):
        try:
            self.session = ssh.spawn(self.credentials, timeout=30)
            # Only new host needs to be put in known_host
            new_host = bool(self.session.expect(['rd:', 'no']))
            if new_host is True:
                self.session.sendline('yes')
                self.session.expect('rd:')
            self.session.sendline(self.password)
            self.session.expect('#')
            return True
        except TIMEOUT:
            print(self.timeout_message)
            print(self.session.before.decode('utf-8').strip())
            return False
        except EOF:
            print(self.unexpected_message)
            print(self.session.before.decode('utf-8').strip())
            return False

    def send_command(self, command):
        try:
            self.session.sendline(command)
            self.session.expect('#')
            return True
        except TIMEOUT:
            print(self.timeout_message)
            return False
        except EOF:
            print(self.unexpected_message)
            print(self.session.before.strip())
            return False

    def search_device_hostname(self):
        self.send_command('show running-config | in hostname')
        config = self.session.before.decode('utf-8').splitlines()
        host = re.compile('^hostname +.*')
        for line in config:
            line = line.strip()
            if host.search(line):
                self.hostname = host.search(line).group(0)[9:]
                break
        return None


# ----------Child class for ISR 881 in regions-------------------------------
class ISR881(GeneralNetworkDevice):
    """
    Purpose of this class is handling data from ISR 881 in branches

    Attributes:
    self.loopback - loopback ip address of the device
    self.lan - branch subnet for LAN devices
    self.voip - branch subnet for VoIP phones

    Methods:
    __init__ - initiation method
    parsing_ip_route - parsing the output from 'show ip route'
                            to find subnets
    """
    def __init__(
            self, ip, username, password,
            session, hostname):
        GeneralNetworkDevice.__init__(self, ip, username, password)
        self.session = session
        self.hostname = hostname
        self.loopback = None
        self.lan = None
        self.voip = None

    def parsing_ip_route(self):
        # Getting ip routing table from the device
        self.send_command('show ip route')
        show_ip_route = self.session.before.decode('utf-8').splitlines()
        # Processing the routing table by regular expressions
        routes = re.compile('^B.*|^O.*|^C +.*|^S.*')
        search_result = list()
        # Looping through the list and searching matches
        for line in show_ip_route:
            line = line.strip()
            if routes.search(line):
                search_result.append(routes.search(line).group(0))
        # Processing founded routes to watch particular subnets
        loopback = re.compile('^C.* Loopback0$')
        lan = re.compile('^C.* Vlan20$')
        voip = re.compile('^C.* Vlan21$')
        subnet = re.compile(
            '\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/\d{1,3}')
        if search_result:
            for line in search_result:
                if loopback.search(line):
                    self.loopback = subnet.search(line).group(0)
                elif lan.search(line):
                    self.lan = subnet.search(line).group(0)
                elif voip.search(line):
                    self.voip = subnet.search(line).group(0)
        return None
