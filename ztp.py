"""Core Zero Touch Provisioning script

This script runs in Guest Shell on a Cisco device running IOS 
XE 16 for the purpose of auto-provisioning the device.

The script is stored in the content service directory of the web 
server used for Zero Touch Provisioning. The network device
retrieves the script from the web server upon initial boot.

The script performs the following functions

    * Bootstraps the device for initial communication
    * Retrieves the serial number from the device
    * Makes a REST call to Node.js to obtain Device Attributes
    * Configures the device with retrieved attributes
    * Copies IBNS2.cfg template into running config
"""

from cli import configure,execute,cli
from xml.dom import minidom
import re
import json
import urllib2

# Define script variables
CONFIG_SERVER='192.168.1.100'
USER="cisco"
PASSWORD="cisco"
ENABLE="cisco"

def base_config():
   # Configure items for bootstrap config
    configure(['username {} privilege 15 password {}'.format(USER,PASSWORD)])
    configure(['enable secret {}'.format(ENABLE)])
    configure(['line vty 0 4', 'login local'])

def get_serials():
    # Grab device inventory in XML format
    inventory = cli('show inventory | format')
    # skip leading newline
    doc = minidom.parseString(inventory[1:])
    serials =[]
    for node in doc.getElementsByTagName('InventoryEntry'):
        # Look for Chassis
        chassis = node.getElementsByTagName('ChassisName')[0]
        if chassis.firstChild.data == "Chassis":
            serials.append(node.getElementsByTagName('SN')[0].firstChild.data)

        # Determine Switch number
        match = re.match('"Switch ([0-9])"', chassis.firstChild.data)
        if match:
            serials.append(node.getElementsByTagName('SN')[0].firstChild.data)

    return serials

def get_my_config(serials):
    # REST call to obtain device attributes
    base = 'http://{}:3000/device?serial='.format(CONFIG_SERVER)
    url =  base + '&serial='.join(serials)
    print '\n\n\n\n****************************************\n'
    print 'REST Call:    {}'.format(url) + '\n'
    configs = json.load(urllib2.urlopen(url))
    for info in configs:
        print 'REST Response (JSON):    {}'.format(info)
    return info

def configure_network(**kwargs):
    # Display results and configure the device with returned attributes
    if 'ip' in kwargs and kwargs['ip'] is not None:
        print '\nZTP-provisioned hostname:      {}'.format(kwargs['hostname'])
        print 'ZTP-provisioned IP address:    {}'.format(kwargs['ip'])
        print '\n****************************************\n\n'
        configure(['hostname {}'.format(kwargs['hostname'])])
        configure(['int g0/0','ip address {} {}'.format(kwargs['ip'], kwargs['netmask'])])
        configure(['ip route vrf Mgmt-vrf 0.0.0.0 0.0.0.0 {}'.format(kwargs['gw'])])

def configure_IBNS2():
    # Copy and merge IBNS 2.0 template into running-config
    configure('file prompt quiet')
    execute('copy http://192.168.1.100/IBNS2.cfg running-config')
    print '\n\n\n\n****************************************\n'
    print 'IBNS 2.0 template applied...'
    print '\n****************************************\n\n'

base_config()
serials = get_serials()
config = get_my_config(serials)
configure_network(**config)
configure_IBNS2()
