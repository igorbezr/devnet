#Importing libraries for handle connections to the device, regular expressions
#for searching pattern, pretty print for nice output formatting
import pexpect
import re
from pprint import pprint as pp

#Storage for device information
device=dict()

#Input device credentials from keyboard
while True:
    try:
        device['ip']=raw_input('Enter device IP address (or Ctrl-C to exit):')
        device['username']=raw_input('Enter username (or Ctrl-C to exit):')
        device['password']=raw_input('Enter password (or Ctrl-C to exit):')
        break
    except KeyboardInterrupt:
        print '\n'
        print 'Programm is terminating !'
        exit()

#Connection to the device
session=pexpect.spawn('ssh '+device['username']+'@'+device['ip'], timeout=10)

output=session.expect(['Password:', pexpect.TIMEOUT, pexpect.EOF])
if output==1:
    print 'Connection to the device '+device['ip']+' timed out !'
    print session.before
    exit()
if output==2:
    print 'Connection to the device '+device['ip']+'recived unexpected output :'
    print session.before
    exit()
session.sendline(device['password'])

output=session.expect(['#',pexpect.TIMEOUT,pexpect.EOF])
if output==0:
    print 'Connection to the device '+device['ip']+' successful !'
if output==1:
    print 'Connection to the device '+device['ip']+' timed out !'
    print session.before
    exit()
if output==2:
    print 'Connection to the device'+device['ip']+' recived unexpected output:'
    print session.before
    exit()

#Send commands to the device
session.sendline('term le 0')
output=session.expect(['#',pexpect.TIMEOUT,pexpect.EOF])
if output==1:
    print 'Connection to the device '+device['ip']+' timed out !'
    print session.before
    exit()
if output==2:
    print 'Connection to the device'+device['ip']+' recived unexpected output:'
    print session.before
    exit()

session.sendline('show ip route')
output=session.expect(['#',pexpect.TIMEOUT,pexpect.EOF])
if output==1:
    print 'Connection to the device '+device['ip']+' timed out !'
    print session.before
    exit()
if output==2:
    print 'Connection to the device'+device['ip']+' recived unexpected output:'
    print session.before
    exit()

#Printing output and closing the session
show_ip_route=session.before.splitlines()
session.close()

#Processing the routing table with regex
regex=re.compile('^B.*|^C +.*|^S.*')
search_result=list()

#Looping through the list and searching matches 
for line in show_ip_route:
    if regex.search(line):
        search_result.append(regex.search(line).group(0))

if search_result:
    pp(search_result)

exit()