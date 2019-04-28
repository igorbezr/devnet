Help on module show_ip_route:

NAME
    show_ip_route - Python 2.7 script shows particular subnets of the Cisco network device

FILE
    /home/cisco/repo/show_ip_route.py

DESCRIPTION
    Hello everyone ! Thanks for your attention.
    
    This simple program has created to automate routine network checking of
    device subnets and IP routing table. The routing table is checking to 
    find OSPF, BGP, Static and connected routes. Then output has been 
    processed to find specific subnets.
    In this particular version device credentials are provided by user 
    from the keyboard input.

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
    
    parsing_ip_route(show_ip_route)
        Collection of regular expressions that processing ip routing table
        
        Input parameters:
            show_ip_route - dictionary of strings from show ip route output
        Returns:
            none
    
    search_device_hostname(session)
        Searching the device's hostname in running-config
        
        Input parameters:
            session - pexpect object contains ssh session to the device
        Returns:
            hostname - string contains the device's hostname

DATA
    print_function = _Feature((2, 6, 0, 'alpha', 2), (3, 0, 0, 'alpha', 0)...


