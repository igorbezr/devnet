Help on module show_ip_route:

NAME
    show_ip_route - Python 2.7 script shows IP routing table of the Cisco network device

FILE
    /home/cisco/repo/show_ip_route.py

DESCRIPTION
    Hello everyone ! Thanks for your attention.
    
    This simple program has created to automate routine network checking of
    device IP routing table. The routing table is checking to find OSPF, 
    BGP, Static and connected routes. In this particular version device 
    credentials are provided by user from the keyboard input.

FUNCTIONS
    connect(command, session)
        Send 'command' to the device CLI and take care of the received output
        
        Input parameters:
            command - string contains correct CLI command
            session - pexpect object contains ssh session to the device
        Returns:
            session - pexpect object contains ssh session to the device
    
    connect_initial(device)
        Handling initial connection to the device.
        
        Input parameters:
            device - dictionary contains device's credentials
        Returns:
            session - pexpect object contains ssh session to the device
    
    keyboard_input()
        The keyboard prompt for user to input device credentials
        
        Input parameters:
            none
        Returns:
            device - dictionary contains device's credentials

DATA
    print_function = _Feature((2, 6, 0, 'alpha', 2), (3, 0, 0, 'alpha', 0)...


