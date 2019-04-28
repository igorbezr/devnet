#----------README for pydoc documentation auto generating--------------

"""
Python 2.7 script shows IP routing table of the Cisco network device

Hello everyone ! Thanks for your attention.

This simple program has created to automate routine network checking of
device IP routing table. The routing table is checking to find OSPF, 
BGP, Static and connected routes. In this particular version device 
credentials are provided by user from the keyboard input.
"""

#----------Libraries importing section---------------------------------
#
#Print function as python 3
from __future__ import print_function
#Importing pexpect for handle connections to the device, regular 
#expressions for searching pattern, pretty print for nicely formatting
import pexpect
import re
from pprint import pprint as pp

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
            device['password']=raw_input(
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
    session.close()

    #Processing the routing table by regular expressions
    regex=re.compile('^B.*|^O.*|^C +.*|^S.*')
    search_result=list()

    #Looping through the list and searching matches 
    for line in show_ip_route:
        if regex.search(line):
            search_result.append(regex.search(line).group(0))

    #If matches exists print nicely formatted output
    if search_result:
        pp(search_result)
    else:
        print('No routes found !')
    exit()
