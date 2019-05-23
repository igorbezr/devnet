# ---------README for pydoc documentation auto generating-------------

"""
This module contains network devices classes code

The code has created to automate the routine network checking of
devices hostnames, LAN and VoIP subnets
"""

# ----------Modules importing section---------------------------------
# Importing pexpect for handle connections to the device, regular
# expressions for searching pattern
import pexpect
import re


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
    self.hostname - logical name of the network device

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
        self.error = False
        self.hostname = None

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
        self.session = self.send_command('show running-config | in hostname')
        config = self.session.before.splitlines()
        host = re.compile('^hostname +.*')
        for line in config:
            line = line.strip().decode(encoding="utf-8", errors="strict")
            if host.search(line):
                self.hostname = host.search(line).group(0)[9:]
                break
        return 0


# ----------Child class for ISR 881 in regions-------------------------------
class ISR881(GeneralNetworkDevice):
    """
    This class create to handle data from ISR881 in branches

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

        # Processing finding routes to see particular subnets
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
        return 0