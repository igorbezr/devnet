#----------README for pydoc documentation auto generating--------------

"""
Python 2.7 script shows particular subnets of the Cisco network device

Hello everyone ! Thanks for your attention.

This simple program has created to automate routine network checking of
device subnets and IP routing table. The routing table is checking to 
find OSPF, BGP, Static and connected routes. Then output has been 
processed to find specific subnets.
In this particular version device credentials are provided by user 
from the keyboard input.
"""

#----------Libraries importing section---------------------------------
#
#Print function as python 3
from __future__ import print_function
#Importing pexpect for handle connections to the device, regular 
#expressions for searching pattern, getpass for password prompt
import pexpect
import re
from getpass import getpass

#------------------------Function definition section-------------------
#
def keyboard_input():
    """ 
    The keyboard prompt for user to input device credentials

    Input parameters:
        none
    Returns:
        device - dictionary contains device's credentials
    """
    device=dict()
    while True:
        try:
            device['ip']=raw_input(
                'Enter device IP address (or Ctrl-C to exit):')
            device['username']=raw_input(
                'Enter username (or Ctrl-C to exit):')
            device['password']=getpass(
                'Enter password (or Ctrl-C to exit):')
            break
        except KeyboardInterrupt:
            print('\n')
            print('Program is terminating !')
            exit()
    return device    

def connect_initial(device):
    """
    Handling initial connection to the device.
    
    Input parameters:
        device - dictionary contains device's credentials
    Returns:
        session - pexpect object contains ssh session to the device
    """
    session=pexpect.spawn('ssh '+device['username']+'@'+device['ip'],
        timeout=10)
    output=session.expect(['(yes/no)','Password:',pexpect.TIMEOUT,
        pexpect.EOF])
    if output==0:
        session.sendline('yes')
        session.expect(['Password:'])
        session.sendline(device['password'])
    if output==1:
        session.sendline(device['password'])
    if output==2:
        print(
            'Connection to the device '+device['ip']+' timed out !')
        print(session.before)
        exit()
    if output==3:
        print(
            'Connection to the device '+device['ip']+
            +'received unexpected output :')
        print(session.before)
        exit()

    output=session.expect(['#',pexpect.TIMEOUT,pexpect.EOF])
    if output==0:
        print('Connection to the device '+device['ip']+' successful !')
    if output==1:
        print('Connection to the device '+device['ip']+' timed out !')
        print(session.before)
        exit()
    if output==2:
        print('Connection to the device'+device['ip']+
            +' received unexpected output:')
        print(session.before)
        exit()
 
    session.sendline('terminal length 0')
    output=session.expect(['#',pexpect.TIMEOUT,pexpect.EOF])
    if output!=0:
        print('Connection to the device '+device['ip']+
            +' received unexpected output')
        print(session.before)
        exit()
    return session

def connect(command,session):
    """
    Send 'command' to the device CLI and take care of the received output

    Input parameters:
        command - string contains correct CLI command
        session - pexpect object contains ssh session to the device
    Returns:
        session - pexpect object contains ssh session to the device
    """
    session.sendline(command)
    output=session.expect(['#',pexpect.TIMEOUT,pexpect.EOF])
    if output!=0:
        print('Connection to the device '+device['ip']+
            +' received unexpected output')
        print(session.before)
        exit()
    return session

def search_device_hostname(session):
    """
    Searching the device's hostname in running-config

    Input parameters:
        session - pexpect object contains ssh session to the device
    Returns:
        hostname - string contains the device's hostname
    """
    session=connect('show running-config | in hostname',session)
    config=session.before.splitlines()
    host=re.compile('^hostname +.*')
    for line in config:
        if host.search(line):
            hostname=host.search(line).group(0)[9:]
            print('Device is '+hostname)
            break
        else:
            hostname='Nothing found'
    return hostname

def parsing_ip_route(show_ip_route):
    """
    Collection of regular expressions that processing ip routing table

    Input parameters:
        show_ip_route - dictionary of strings from show ip route output
    Returns:
        none
    """
    #Processing the routing table by regular expressions
    routes=re.compile('^B.*|^O.*|^C +.*|^S.*')
    search_result=list()

    #Looping through the list and searching matches 
    for line in show_ip_route:
        if routes.search(line):
            search_result.append(routes.search(line).group(0))

    #Processing received routes with additional regular expressions 
    loopback=re.compile('^C.* Loopback0$')
    lan=re.compile('^C.* Vlan20$')
    voip=re.compile('^C.* Vlan21$')
    subnet=re.compile(
        '\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/\d{1,3}')
    if search_result:
        for line in search_result:
            if loopback.search(line):
                print('Loopback is '+subnet.search(line).group(0))
            elif lan.search(line):
                print('LAN subnet is '+subnet.search(line).group(0))
            elif voip.search(line):
                print('VoIP subnet is '+subnet.search(line).group(0))
    else:
        print('No routes found !')
    exit()

#----------Main code---------------------------------------------------
#
#Temporary fix for pydoc correct working
if __name__ == '__main__':
    #Connection to the device and execution 'show ip route' command
    device=keyboard_input()
    session=connect_initial(device)
    session=connect('show ip route',session)

    #Printing output and closing the session
    show_ip_route=session.before.splitlines()

    #Search for device hostname
    hostname=search_device_hostname(session)
    session.close()

    #Processing the routing table by regular expressions
    parsing_ip_route(show_ip_route)

    exit()
